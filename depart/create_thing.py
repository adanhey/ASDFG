import requests
import jsonpath
from get_code import *
from alllist import *
import setting

host = setting.host


def create_ck(cookie, name, managename, parentName=None, cktype="备件仓库"):
    url = '%s/es/storage/saveOrUpdate' % host
    ck = ck_code(cookie)
    emp_info = emp_list(cookie=cookie, name=managename)
    types = dict_list(cookie, "storageType", 1)['data']['records']
    storagetypeid = ''
    for type in types:
        if type['dictKey'] == cktype:
            storagetypeid = type['id']
    data = {
        "storageCode": ck,
        "storageName": name,
        "managerId": emp_info['id'],
        "managerName": emp_info['name'],
        "country": "",
        "address": "",
        "storageDesc": "",
        "storageTypeId": storagetypeid,
        "storageTypeName": cktype,
    }
    if parentName:
        ck_info = get_cangkutree(cookie, parentName)
        data['parentName'] = ck_info['storageName']
        data['parentId'] = ck_info['id']
        data['ids'] = ck_info['ids']
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def create_kw(cookie, storageid, storageids, name="库位", oneBatch=2, generrateRule=1, generateNum="10", kwtype="库位1"):
    url = '%s/es/storagelocation/save' % host
    types = dict_list(cookie, "storageLocationType", 1)['data']['records']
    storagelocationtypeid = ''
    for type in types:
        if type['dictKey'] == kwtype:
            storagelocationtypeid = type['id']
    data = {
        "storageLocationCode": "",
        "storageLocationName": name,
        "oneBatch": oneBatch,
        "generateRule": generrateRule,
        "generateNum": generateNum,
        "rackNum": "",
        "floorsNum": "",
        "positionNum": "",
        "storageLocationTypeName": kwtype,
        "storageLocationTypeId": storagelocationtypeid,
        "storageLocationDesc": "",
        "storageId": storageid,
        "storageIds": storageids
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def create_sup_type(cookie, name, code, typename=None):
    url = '%s/es/supplierType/saveOrUpdate' % host
    data = {
        "typeName": name,
        "typeCode": code,
        "remark": "",
        "id": "",
        "ids": ""
    }
    if typename:
        parentid = get_suppliertree(cookie, typename)['id']
        ids = get_suppliertree(cookie, typename)['ids']
        data['parentId'] = parentid
        data['parentName'] = typename
        data['ids'] = ids
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def create_gys(cookie, code, name, typename, contactName="noone", phone='15652222222'):
    url = '%s/es/supplier/save' % host
    gyscode = gys_code(cookie)
    type = get_suppliertree(cookie, typename)
    data = {
        "systemCode": gyscode,
        "supplierCode": code,
        "supplierName": name,
        "nickName": "",
        "contactName": contactName,
        "phone": phone,
        "email": "",
        "addressData": [],
        "typeId": type['id'],
        "typeIds": type['ids'],
        "typeName": typename,
        "supplierDesc": ""
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def create_sparepartstype(cookie, name, code, parentname=None):
    url = '%s/es/sparePartsType/saveOrUpdate' % host
    data = {
        "typeName": name,
        "typeCode": code,
        "remark": "",
        "parentName": "类别1",
        "id": "",
    }
    if parentname:
        parentid = get_sparePartstree(cookie, parentname)['id']
        parentids = get_sparePartstree(cookie, parentname)['ids']
        data['parentName'] = parentname
        data['parentId'] = parentid
        data['ids'] = parentids
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def create_bj(cookie, typename, name, code):
    bjcode = bj_code(cookie)
    typeids = get_sparePartstree(cookie, typename)['ids']
    typeid = get_sparePartstree(cookie, typename)['id']
    url = '%s/es/spareParts/saveSpareParts' % host
    data = {
        "systemCode": bjcode,
        "sparePartsCode": code,
        "sparePartsName": name,
        "typeName": typename,
        "typeIds": typeids,
        "typeId": typeid,
        "sparePartsModel": "",
        "criticalityName": "",
        "criticalityId": "",
        "brand": "",
        "unitName": "",
        "unitId": "",
        "sparePartsDesc": "",
        "photo": ""
    }
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)


def save_bj_gys(cookie, typename, bjname, **kwargs):
    url = '%s/es/supplierSparePart/save' % host
    bjid = bj_list(cookie, 1, typename, 100, bjname)
    data = {
        "id": bjid,
        "supplierEntities": [
            {
                "id": "1580092636393418753"
            }
        ]
    }
    for suptype,sup in kwargs.items():
        supid = get_suppliertree(cookie,suptype)

        data['supplierEntities'].append({"id": supid})
    result = requests.session().post(url=url, cookies=cookie, json=data)
    print(result.text)