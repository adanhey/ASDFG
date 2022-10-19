import json
from ASDFG.interface_ability.list_base import *
import requests
import jsonpath
from ASDFG import setting

host = setting.host


class List_request(Interface_list):
    def get_suppliertree(self, typeName):
        url = '%s/es/supplierType/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        jsonresult = self.find_listresult(result.json(), "typeName", typeName)
        return jsonresult

    def get_cangkutree(self, storagetypename):
        url = '%s/es/storage/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        jsonresult = self.find_listresult(result.json(), "storageName", storagetypename)
        return jsonresult

    def get_sparePartstree(self, sparePartsname):
        url = '%s/es/sparePartsType/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        jsonresult = self.find_listresult(result.json(), "typeName" % sparePartsname)
        return jsonresult

    def get_location(self, storageid, page=1, size=20, used="", storagelocationname=""):
        url = '%s/es/storagelocation/list' % self.host
        data = {
            "storageLocationName": storagelocationname,
            "used": used,
            "storageLocationTypeIds": [],
            "storageId": storageid,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result.json()

    def emp_list(self, jobnumber=None, name=None):
        url = '%s/es/employee/list' % self.host
        data = {
            "used": 1,
            "size": 10,
            "current": 1
        }
        if jobnumber:
            data['jobNumber'] = jobnumber
        elif name:
            data['name'] = name
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        try:
            emp_info = result.json()['data']['records'][0]
        except:
            raise ValueError("未找到员工信息")
        return emp_info

    def dict_list(self, dictcode, children):
        url = '%s/es/dict/list' % self.host
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
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result.json()

    def sup_list(self, supid, page, size=100):
        url = '%s/es/supplier/list' % self.host
        data = {
            "supplierCode": "",
            "supplierName": "",
            "contactName": "",
            "phone": "",
            "typeId": supid,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result.json()

    def bj_list(self, page, typename, size=100, name=None):
        url = '%s/es/spareParts/list' % self.host
        typeid = self.get_sparePartstree(typename)['id']
        data = {
            "brands": [],
            "sparePartsName": name,
            "typeId": typeid,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result.json()

    def list_storage_spareparts(self,storageId,sparePartsName="",sparePartsCode=""):
        url = '%s/es/storageSpareParts/list' % self.host
        data = {
            "sparePartsName": sparePartsName,
            "sparePartsCode": sparePartsCode,
            "typeIds": [],
            "safetyStatus": [],
            "storageId": storageId,
            "current": 1,
            "size": 20
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result.json()

interface = List_request()
result = interface.list_storage_spareparts("777237194550185984")
print(result)
