import hashlib
import time
import requests
import json


def get_cookie(name, password):
    url = 'https://huiserver.dataserver.cn/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


# cookie = get_cookie('sysadmin', 'hc300124')
cookie = get_cookie('zheng1', 'abcd123456')


def get_setting(ordername='默认工单类型'):
    url = 'https://huiserver.dataserver.cn/es/orderType/list'
    result = requests.post(url=url, cookies=cookie)
    print("工单类型列表：%s" % result.text)
    for data in result.json()['data']:
        if data['typeName'] == ordername:
            return data['id']


def get_support_exec(ordertypeid):
    url = 'https://huiserver.dataserver.cn/es/orderNodeConfig/list'
    data = {
        "orderTypeId": "%s" % ordertypeid
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    print("工单支持操作结果：%s" % result.text)
    used = {}
    for i in result.json()['data']:
        jcccc = str(i['configDetailInfo'])
        jcccc.replace('\\', '')
        usedstauts = i['used']
        used['%s状态' % i['nodeName']] = usedstauts
        used['%s' % i['nodeName']] = jcccc
    for j, k in used.items():
        print('%s : %s' % (j, k))
    return str(used)


def create_order(ordertypeid, describe, ordertype):
    url = 'https://huiserver.dataserver.cn/es/order/save'
    if ordertype:
        pass
    else:
        ordertype = "默认工单类型"
    orderno = get_orderno()
    # data = {
    #     "customerName": "z客户",
    #     "customerId": "772098199931826176",
    #     "contactName": "con",
    #     "phone": "13333333333",
    #     "country": "中国",
    #     "province": "山西省",
    #     "city": "太原市",
    #     "area": "杏花岭区",
    #     "address": "12345678901234567890123456789012345678901234567890",
    #     "deptId": "771790531383828480",
    #     "deptName": "汇服务测试环境",
    #     "orderNo": orderno,
    #     "orderType": ordertype,
    #     "orderTypeId": ordertypeid,
    #     "poolIds": [],
    #     "rootId": "0",
    #     "maintenanceType": "保内免费",
    #     "maintenanceTypeId": "754052018886316032",
    #     "label": "紧急工单",
    #     "labelId": "754066338659602432",
    #     "expectedStartTime": "2022-09-01",
    #     "expectedEndTime": "2022-09-03",
    #     "picture": "",
    #     "describe": "%s" % describe,
    #     "serviceItems": [],
    #     "fieldExtensions": "{\"col2\":\"111\"}"
    # }
    data = {
        "customerName": "z客户",
        "customerId": "773229154207465472",
        "contactName": "kk1",
        "phone": "13333333333",
        "country": "中国",
        "province": "北京市",
        "city": "市辖区",
        "area": "东城区",
        "address": "30",
        "deptId": "773227650851471360",
        "describe": "%s" % describe,
        "deptName": "江苏维达",
        "orderNo": orderno,
        "orderType": ordertype,
        "orderTypeId": ordertypeid,
        "poolIds": [],
        "rootId": "3",
        "label": "紧急工单",
        "labelId": "754066338659602432",
        "expectedStartTime": "2022-09-01",
        "expectedEndTime": "2022-09-24",
        "picture": "",
        "serviceItems": [],
        "fieldExtensions": "{\"col1\":\"111\"}"
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("创建结果: %s" % result.text)
    return result.json()['data']['orderNo'], result.json()['data']['orderId']


def search_order(orderNo):
    url = 'https://huiserver.dataserver.cn/es/order/list'
    data = {
        "orderNo": orderNo,
        "current": 1,
        "size": 20
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    return result.json()


def operate_order(orderNo):
    url = 'https://huiserver.dataserver.cn/es/order/operate'
    orderdata = search_order(orderNo)
    orderid = orderdata['data']['records'][0]['_id']
    data = {
        "servicePerson": "z服务工程师",
        "servicePersonId": "772098483265449984",
        "servicePersonPhone": "13997707166",
        "assistPerson": [],
        "assistPersonId": [],
        "operate": "DISPATCH",
        "_id": "%s" % orderid
    }
    if int(orderdata['data']['records'][0]['status']) == 2:
        result = requests.Session().post(url=url, cookies=cookie, json=data)
        print('派工结果：%s' % result.text)
    else:
        print('派单失败,工单状态非待派工')
        raise

def get_orderno():
    url = 'https://huiserver.dataserver.cn/es/common/getCode/GD'
    result = requests.get(url=url,cookies=cookie)
    return result.json()['data']

def get_approve_id(orderNo):
    url = 'https://huiserver.dataserver.cn/es/orderAppro/list'
    data = {
        "orderView": 4,
        "orderNo": "%s" % orderNo,
        "current": 1,
        "size": 20
    }
    idlist = []
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    for record in result.json()['data']['records']:
        if record['approStatus'] == 1:
            idlist.append(record['_id'])
    return idlist


def approve_order(orderNo, approStatus=4):
    idlist = get_approve_id(orderNo)
    url = 'https://huiserver.dataserver.cn/es/orderAppro/operate'
    data = {
        "approStatus": int('%i' % approStatus),
    }
    for approveid in idlist:
        data['id'] = "%s" % approveid
        result = requests.Session().post(url=url, cookies=cookie, json=data)
        print("审批结果：%s" % result.text)


def order_accept(orderNo):
    url = 'https://huiserver.dataserver.cn/es/order/operate'
    orderdata = search_order(orderNo)
    orderid = orderdata['data']['records'][0]['_id']
    data = {
        "_id": "%s" % orderid,
        "status": 3,
        "operate": "ACCEPT"
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("接收结果：%s" % result.text)


def start_order(orderid):
    url = 'https://huiserver.dataserver.cn/es/order/operate'
    data = {
        "_id": "%s" % orderid,
        "status": 4,
        "operate": "START"
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("开始工单：%s" % result.text)


def wangonghuizhi(orderNo):
    url = 'https://huiserver.dataserver.cn/es/serviceRecord/saveOrUpdate'
    data = {
        "orderId": orderNo,
        "staging": 0,
        "totalOriginPrice": 0,
        "totalRealPrice": 0,
        "historyRemainingProblems": [],
        "remainingProblems": []
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("提交验收： %s" % result.text)


def kehuyanshou(orderNo):
    url = 'https://huiserver.dataserver.cn/es/customerSignature/save'
    data = {
        "acceptanceComments": "验收意见",
        "orderId": orderNo,
        "originPrice": 100,
        "photo": [{"id": "772498448424873984", "url": "0000102089/customerSignature/16643444480628549.png", "name": "signature.png"}],
        "realPrice": 100,
        "serviceIds": [],
        "sparePartIds": []
    }
    print(data)
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("验收结果： %s" % result.text)


def guanbi(orderNo):
    url = 'https://huiserver.dataserver.cn/es/order/operate'
    data = {
        "id": "",
        "operate": "CLOSE",
        "closeCase": "1",
        "closeDes": "11",
        "status": 2,
        "_id": orderNo
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("关闭结果： %s" % result.text)


status = {
    "待派工": 2,
    "已派工": 3,
    "已接收": 4,
    "进行中": 5,
    "待验收": 6,
    "已完成": 7,
    "已关闭": 8,
    "已取消": -1,
}


def run_order_to(orderNo, zhipaishenpi, runtostatus=None):
    if isinstance(runtostatus, str):
        runtostatus = int(runtostatus)
    if isinstance(zhipaishenpi, str):
        zhipaishenpi = int(zhipaishenpi)
    orderdata = search_order(orderNo)
    orderid = orderdata['data']['records'][0]['_id']
    describe = str(orderdata['data']['records'][0]['describe'])
    describe = describe.replace('null', '""')
    describe = eval(describe)
    print(describe['指派工单'])
    if runtostatus == 8:
        guanbi(orderNo)
    if runtostatus >= 3:
        operate_order(orderNo)
        describe['指派工单'] = eval(describe['指派工单'])
        if int(describe['指派工单']['assignApproval']) == 0:
            pass
        elif zhipaishenpi in [3, 4]:
            approve_order(orderNo, zhipaishenpi)
        if int(describe['指派工单']['assignApproval']) == 2 and zhipaishenpi == 4:
            approve_order(orderNo, zhipaishenpi)
        if runtostatus >= 4:
            if int(describe['接收工单状态']) != 0:
                order_accept(orderNo)
            if runtostatus >= 5:
                start_order(orderid)
                if runtostatus >= 6:
                    wangonghuizhi(orderid)
                    if runtostatus >= 7:
                        if int(describe['客户验收状态']) != 0:
                            kehuyanshou(orderid)


# print("默认为'默认工单类型'")
name = '节点全开'
print(status)
statu = int(input("请输入需要的状态："))
print("指派审批状态: 3不通过，4通过，其他数字不执行审批并且")
zhipaishenpi = input("指派审批状态")
if name:
    a = get_setting(name)
else:
    a = get_setting("默认工单类型")
b = get_support_exec(a)
orderNo, orderid = create_order(ordertypeid=a, describe=b, ordertype=name)
run_order_to(orderNo, zhipaishenpi, statu)
