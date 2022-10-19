import hashlib
import json
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


def get_kh():
    url = 'https://huiservertest1.iotdataserver.net/es/common/getCode/KH'
    result = requests.get(url=url, cookies=cookie)
    return result.json()['data']


def Extension_list(moduleTypeId):
    # 获取自定义字段，moduleTypeId为模块id，例如客户为6
    url = 'https://huiservertest1.iotdataserver.net/es/fieldExtension/list'
    data = {
        "current": 1,
        "moduleTypeId": moduleTypeId,
        "systemField": 0,
        "used": 1,
        "size": 100
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    return result.json()['data']['records']


def get_dict(dictCode):
    url = 'https://huiservertest1.iotdataserver.net/es/dict/list'
    data = {
        "dictCode": dictCode,
        "current": 1,
        "size": 100,
        "queryChildren": 'true'
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    return result.json()['data']['records']


def get_department():
    url = 'https://huiservertest1.iotdataserver.net/es/department/getList'
    data = {}
    result = requests.post(url=url, cookies=cookie, json=data)
    return result.json()['data']


def get_employee(name=None):
    url = 'https://huiservertest1.iotdataserver.net/es/employee/list'
    data = {
        "size": 50,
        "current": 1,
    }
    result = requests.post(url=url, cookies=cookie, json=data)
    data['size'] = result.json()['data']['total']
    result = requests.post(url=url, cookies=cookie, json=data)
    if name:
        for record in result.json()['data']['records']:
            if record['name'] == name:
                return record
    else:
        return result.json()['data']['records']


def create_costume(name,nickname,labelnames,contactName,phone,address,organization,employeeName,customerManager,remark):
    url = 'https://huiservertest1.iotdataserver.net/es/customer/save'
    kh =get_kh()
    data = {
        "id": "",
        "companyId": "",
        "customerCode": "",
        "customerNumber": kh,
        "fullName": name,
        "nickName": nickname,
        "labelList": [
            # {
            #     "labelId": "746865462582005760",
            #     "labelName": "VIP客户"
            # }
        ],
        "contactName": contactName,
        "phone": "13663322110",
        "country": "中国",
        "province": "北京市",
        "city": "市辖区",
        "area": "东城区",
        "address": "111",
        "organization": "部门3cc",
        "organizationId": "751431020651720704",
        "employeeId": "750495222359957505",
        "employeeName": "员工1",
        "customerManagerId": "750495222359957505",
        "customerManager": "员工1",
        "remark": "11010",
        "logoUrl": "",
        "fieldExtensions": "{\"col1\":\"222\",\"col2\":\"111\"}"
    }
    labeldict = get_dict('customerLabel')
    for i in labelnames:
        for j in labeldict:
            if j['dictKey'] == i:
                ddd = {}
                ddd['labelId'] = j['id']
                ddd['labelName'] = j['dictKey']
                data['labelList'].append(ddd)



a = get_employee("测试派工19")
print(a)
