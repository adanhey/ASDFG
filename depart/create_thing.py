from ASDFG.depart.get_code import *
from ASDFG.depart.alllist import *


class Create_request(code_request, List_request):
    def create_ck(self, name, managename, parentName=None, cktype="备件仓库"):
        url = '%s/es/storage/saveOrUpdate' % self.host
        ck = self.ck_code()
        emp_info = self.emp_list(managename)
        types = self.dict_list("storageType", 1)['data']['records']
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
            ck_info = self.get_cangkutree(parentName)
            data['parentName'] = ck_info['storageName']
            data['parentId'] = ck_info['id']
            data['ids'] = ck_info['ids']
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def create_kw(self, storageid, storageids, name="库位", oneBatch=2, generrateRule=1, generateNum="10", kwtype="库位1"):
        url = '%s/es/storagelocation/save' % self.host
        types = self.dict_list("storageLocationType", 1)['data']['records']
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
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def create_sup_type(self, name, code, typename=None):
        url = '%s/es/supplierType/saveOrUpdate' % self.host
        data = {
            "typeName": name,
            "typeCode": code,
            "remark": "",
            "id": "",
            "ids": ""
        }
        if typename:
            parentid = self.get_suppliertree(typename)['id']
            ids = self.get_suppliertree(typename)['ids']
            data['parentId'] = parentid
            data['parentName'] = typename
            data['ids'] = ids
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def create_gys(self, code, name, typename, contactName="noone", phone='15652222222'):
        url = '%s/es/supplier/save' % self.host
        gyscode = self.gys_code()
        type = self.get_suppliertree(typename)
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
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def create_sparepartstype(self, name, code, parentname=None):
        url = '%s/es/sparePartsType/saveOrUpdate' % self.host
        data = {
            "typeName": name,
            "typeCode": code,
            "remark": "",
            "parentName": "类别1",
            "id": "",
        }
        if parentname:
            parentid = self.get_sparePartstree(parentname)['id']
            parentids = self.get_sparePartstree(parentname)['ids']
            data['parentName'] = parentname
            data['parentId'] = parentid
            data['ids'] = parentids
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        print(result.text)

    def create_bj(self, typename, name, code):
        bjcode = self.bj_code()
        typeids = self.get_sparePartstree(typename)['ids']
        typeid = self.get_sparePartstree(typename)['id']
        url = '%s/es/spareParts/saveSpareParts' % self.host
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
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def save_bj_gys(self, typename, bjname, **kwargs):
        url = '%s/es/supplierSparePart/save' % self.host
        bjid = self.bj_list(1, typename, 100, bjname)
        data = {
            "id": bjid,
            "supplierEntities": [
                {
                    "id": "1580092636393418753"
                }
            ]
        }
        for suptype, sup in kwargs.items():
            supid = self.get_suppliertree(suptype)
            data['supplierEntities'].append({"id": supid})
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result
