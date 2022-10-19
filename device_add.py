import hashlib
import threading
import time
import pymysql
import requests


def get_cookie(name, password):
    url = 'https://huiservertest1.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('sysadmin', 'hc300124')


def get_cp():
    url = 'https://huiservertest1.iotdataserver.net/es/product/getProductCode'
    result = requests.post(url=url, cookies=cookie)
    print(result.text)
    return result.json()['msg']


def get_xh(xhname):
    url = 'https://huiservertest1.iotdataserver.net/es/productModel/getList'
    result = requests.post(url=url, cookies=cookie)
    print(result.text)
    for da in result.json()['data']:
        if da['modelName'] == xhname:
            return da['id']


def save_cp(modelid,productname, productcode, cpno, buytime="2022-09-01", installTime="2022-09-01", checkTime="2022-10-30",
            defendEndTime="2022-10-30"):
    url = 'https://huiservertest1.iotdataserver.net/es/product/saveOrUpdate'
    data = {
        "systemCode": cpno,
        "companyId": "cad3fca1-d608-48b3-82fc-28b5f8c9a5ec",
        "productCode": productcode,
        "productName": productname,
        "productModel": modelid,
        "nickName": "群武的公司（勿动）",
        "customerId": "755414014491926528",
        "buyTime": buytime,
        "installTime": installTime,
        "checkTime": checkTime,
        "defendEndTime": defendEndTime,
        "picUrl": "",
        "fieldExtensions": "{\"col1\":\"\"}"
    }
    result = requests.post(url=url, cookies=cookie,json=data)
    print(result.text)

def create_weibao(name):
    url = 'https://huiservertest1.iotdataserver.net/es/deviceMaintainConfig/saveOrUpdate'
    data = {
        "name": name,
        "isInCycle": 1,
        "inCycleBeginType": 1,
        "inFirstMaintainDays": 30,
        "inCycleType": 0,
        "inCycleDays1": 30,
        "inCycleDays2": 30,
        "isOutCycle": 0,
        "outFirstMaintainDays": 30,
        "outCycleType": 0,
        "outCycleDays1": 30,
        "outCycleDays2": 30,
        "beforeRemindDays": 10,
        "remindWay": "",
        "addWay": 1,
        "remindCheck1": "false",
        "remindRole": "",
        "remindCheck2": "false",
        "remindInput2": "",
        "isOpenInCycle": 0,
        "isOpenOutCycle": 0,
        "inCycleDays": 30,
        "outCycleDays": 30,
        "remindUsers": "",
        "productModelIds": [
            "1562321315819499522"
        ]
    }



modelid = get_xh("维保测试")
for i in range(1,10):
    cpno = get_cp()
    Code = time.strftime('%Y年%m月%d日%H：%M：%S')
    print(Code)
    name = '%s安装日期%s号'%(int(time.time()),i)
    print(name)
    if i <10:
        buytime = "2022-10-0%s"%i
        installTime = "2022-10-0%s"%i
    else:
        buytime = "2022-10-%s"%i
        installTime = "2022-10-%s"%i
    save_cp(modelid,name,Code,cpno,buytime,installTime)
    time.sleep(2)