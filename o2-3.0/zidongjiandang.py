import hashlib
import math
import requests
from urllib3 import encode_multipart_formdata


def get_cookie(name, password):
    url = 'https://pastest.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('gfAdmin', 'abcd123456')


def get_hardwaretype():
    url = 'https://pastest.iotdataserver.net/uweb-monitor/intellgentHardwareType/getAllIntellgentHardwareType'
    result = requests.Session().get(url=url, cookies=cookie)
    d = []
    for i in result.json()['data']:
        d.append(i['typeName'])
    return d


def moban_chachong():
    url = 'https://pastest.iotdataserver.net/uweb-monitor/collectTemplate/getCollectTemplateList'
    data = {
        "templateName": "",
        "current": 1,
        "size": 10,
        "sort": "",
        "order": ""
    }
    size = 10
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    total = result.json()['data']['total']
    page = math.ceil((int(total) / size))
    namelist = []
    for i in range(1, page + 1):
        data['current'] = i
        result = requests.Session().post(url=url, cookies=cookie, json=data)
        for record in result.json()['data']['records']:
            namelist.append(record['templateName'])
    return namelist


def create_Template(productModel, templateName):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/collectTemplate/addOrUpdateCollectTemplate'
    data = {
        "templateName": "%s" % templateName,
        "id": "",
        "productModel": "%s" % productModel
    }
    namelist = moban_chachong()
    hwtype = get_hardwaretype()
    if productModel not in hwtype:
        print("模块类型输入错误")
        return None
    elif templateName in namelist:
        print("名称重复")
        return None
    else:
        result = requests.Session().post(url=url, cookies=cookie, json=data)
        print(result.text)
        return result.json()['data']['id']


def add_target(tp_id, ip, targetName, plcBrand="通用协议", plcType='Modbus_RTU_NEW'):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/collectTemplateTarget/addTemplateTarget'
    data = {
        "interfaceType": 1,
        "physicAddress": "%s" % ip,
        "port": 502,
        "targetName": "%s" % targetName,
        "plcBrand": "%s" % plcBrand,
        "plcType": "%s" % plcType,
        "collectTemplateId": "%s" % tp_id
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    assert result.status_code == 200
    print(result.text)


def get_protocolid(tp_id, targetName):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/collectTemplateTarget/getTargetListByCollectTemplateId?collectTemplateId=%s' % tp_id
    result = requests.Session().get(url=url, cookies=cookie)
    protocolid = ''
    targetid = ''
    for data in result.json()['data']:
        if data['targetName'] == targetName:
            protocolid = data['protocolId']
            targetid = data['id']
    return protocolid, targetid


def daoru(protocolid):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/excel/importExcel?excelType=protocol&id=%s' % protocolid
    data = {"files": ("moban.xls", open('./moban.xls', 'rb').read())}
    encode_data = encode_multipart_formdata(data)
    data = encode_data[0]
    header = {'Content-Type': encode_data[1]}
    result = requests.post(url=url, cookies=cookie, headers=header, data=data)


def addmanage(productName="nnnnn", remark="自动建档"):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/productManage/addOrUpdateProductManage'
    data = {
        "productName": productName,
        "remark": remark
    }
    result = requests.post(url=url, cookies=cookie, json=data)


def getproductid(productName='nnnnn'):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/productManage/getProductList'
    data = {
        "productName": "",
        "current": 1,
        "size": 10
    }
    size = 10
    result = requests.post(url=url, cookies=cookie, json=data)
    total = result.json()['data']['total']
    page = math.ceil((int(total) / size))
    namelist = []
    id = ''
    for i in range(1, page + 1):
        data['current'] = i
        result = requests.Session().post(url=url, cookies=cookie, json=data)
        for record in result.json()['data']['records']:
            if record['productName'] == productName:
                id = record['id']
                break
    return id


def addOrUpdateProductTemplate(template_id, targetid, productName='nnnnn', sourceName='jjj'):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/productTemplateRelation/addOrUpdateProductTemplate'
    productid = getproductid(productName=productName)
    print(productid)
    data = {
        "collectTemplateId": template_id,
        "sourceName": sourceName,
        "productId": productid,
        "templateTargetIds": [
            targetid
        ]
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    print("warning%s" % result.text)


def get_deviceno():
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceManage/generateDeviceNo'
    result = requests.get(url=url, cookies=cookie)
    return result.json()['data']


def get_companyid(companyname=None):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/company/getAllCompanyTree'
    result = requests.get(url=url, cookies=cookie)
    if companyname:
        for cp in result.json()['data']['childList']:
            if cp['companyName'] == companyname:
                return cp['id']
        print('未查询到对应机构')
        return None
    else:
        return result.json()['data']['id']


def add_device(companyid, deviceno, productName='nnnnn', deviceName='cccc'):
    productid = getproductid()
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceManage/addOrUpdateDeviceManage'
    print(productid)
    data = {
        "deviceNo": "%s" % deviceno,
        "deviceName": "%s" % deviceName,
        "companyId": "%s" % companyid,
        "productId": "%s" % productid
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    print(result.text)
    return result.json()['data']['id']


def bindcollet(regCode, templateid, targetid):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/collectDevice/bindCollectTemplate'
    data = {
        "collectTemplateId": "%s" % templateid,
        "regCode": "%s" % regCode,
        "templateTargetIdList": [
            "%s" % targetid
        ]
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    print(result.text)


def bindiot(deviceid, templateid, regCode):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceManage/deviceBindIot'
    data = {
        "deviceId": "%s" % deviceid,
        "relationParamList": [
            {
                "productTemplateId": "%s" % templateid,
                "regCode": "%s" % regCode
            }
        ]
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    print(result.text)

def getsourceid(deviceid):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceManage/getProductSourceListByDeviceId?deviceId=%s'%deviceid
    result = requests.get(url=url, cookies=cookie)
    return result.json()['data'][0]['id']

# template_id = create_Template("IOT-WL430DE", "auto_create2")
# add_target(template_id, "192.168.1.78", "rrr", plcType='Modbus_TCP_NEW')
# proid, targetid = get_protocolid(template_id, 'rrr')
# print(proid)
# daoru(proid)
# addmanage()
# addOrUpdateProductTemplate(template_id=template_id, targetid=targetid)
# deviceno = get_deviceno()
# companyid = get_companyid()
# deviceid = add_device(companyid, deviceno)
# bindcollet('QN004QD9AA', template_id, targetid)
# print(deviceid,template_id)
# gourceid = getsourceid(deviceid)
# bindiot(deviceid, gourceid, 'QN004QD9AA')
