import json

import requests
import jsonpath
import setting

host = setting.host


def get_suppliertree(cookie, typeName):
    url = '%s/es/supplierType/getTreeList' % host
    result = requests.session().post(url=url, cookies=cookie)
    jsonresult = jsonpath.jsonpath(result.json(), "$..*[?(@.typeName=='%s')]" % typeName)
    return jsonresult[0]


def get_cangkutree(cookie, storagetypename):
    url = '%s/es/storage/getTreeList' % host
    result = requests.session().post(url=url, cookies=cookie)
    jsonresult = jsonpath.jsonpath(result.json(), "$..*[?(@.storageName=='%s')]" % storagetypename)
    return jsonresult[0]


def get_sparePartstree(cookie, sparePartsname):
    url = '%s/es/sparePartsType/getTreeList' % host
    result = requests.session().post(url=url, cookies=cookie)
    jsonresult = jsonpath.jsonpath(result.json(), "$..*[?(@.typeName=='%s')]" % sparePartsname)
    return jsonresult[0]


def get_kuwei(cookie, storageid, page=1, size=20, used="", storagelocationname=""):
    url = '%s/es/storagelocation/list' % host
    data = {
        "storageLocationName": storagelocationname,
        "used": used,
        "storageLocationTypeIds": [],
        "storageId": storageid,
        "current": page,
        "size": size
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    return result.json()


def emp_list(cookie, jobnumber=None, name=None):
    url = '%s/es/employee/list' % host
    data = {
        "used": 1,
        "size": 10,
        "current": 1
    }
    if jobnumber:
        data['jobNumber'] = jobnumber
    elif name:
        data['name'] = name
    result = requests.session().post(url=url, cookies=cookie, json=data)
    try:
        emp_info = result.json()['data']['records'][0]
    except:
        raise ValueError("未找到员工信息")
    return emp_info


def dict_list(cookie, dictcode, children):
    url = '%s/es/dict/list' % host
    data = {
        "dictCode": dictcode,
        "current": 1,
        "size": 100,
        # "queryChildren": true
    }
    if children:
        data['queryChildren'] = 'true'
        a = str(data).replace("'true'", 'true')
        a = a.replace("'", '"')
        data = json.loads(a)
    result = requests.session().post(url=url, cookies=cookie, json=data)
    return result.json()


def sup_list(cookie, supid, page, size=100):
    url = '%s/es/supplier/list' % host
    data = {
        "supplierCode": "",
        "supplierName": "",
        "contactName": "",
        "phone": "",
        "typeId": supid,
        "current": page,
        "size": size
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    return result.json()


def bj_list(cookie, page, typename, size=100, name=None):
    url = '%s/es/spareParts/list' % host
    typeid = get_sparePartstree(cookie,typename)['id']
    data = {
        "brands": [],
        "sparePartsName": name,
        "typeId": typeid,
        "current": page,
        "size": size
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    return result.json()
