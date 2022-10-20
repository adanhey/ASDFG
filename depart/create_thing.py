from ASDFG.depart.get_code import *
from ASDFG.depart.list_thing import *


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

    def create_appeal(self, appealTypeName, appealLabelId, appealLabel, customerName, customerId, contactName, phone,
                      deptId, deptName, appealCode, appealType, labelId, country, city, area, address, province="",
                      productInfo=None, picture="", fieldExtensions=None, label=None, expectedStartTime=None,
                      expectedEndTime=None, describe=None):
        url = '%s/es/appeal/save' % self.host
        data = {
            "customerName": customerName,
            "customerId": customerId,
            "contactName": contactName,
            "phone": phone,
            "country": country,
            "province": province,
            "city": city,
            "area": area,
            "address": address,
            "deptId": deptId,
            "deptName": deptName,
            "appealCode": appealCode,
            "appealType": appealType,
            "label": label,
            "labelId": labelId,
            "expectedStartTime": expectedStartTime,
            "expectedEndTime": expectedEndTime,
            "describe": describe,
            "picture": picture,
            "productInfo": productInfo,
            "appealTypeName": appealTypeName,
            "fieldExtensions": fieldExtensions,
            "appealLabelId": appealLabelId,
            "appealLabel": appealLabel
        }
        if data['productInfo'] == None:
            data['productInfo'] = []
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def create_order(self, orderNo, rootId, customerName, customerId, contactName, phone,
                     deptId, deptName, orderTypeId, orderType, labelId, country, city, area, address, province="",
                     expectedStartTime=None, expectedEndTime=None, productInfo=None, picture="", fieldExtensions="{}",
                     describe=None, dispatchType=None, servicePerson=None, servicePersonId=None,
                     servicePersonPhone=None, assistPerson=None, assistPersonId=None, poolIds=None,
                     maintenanceType=None, maintenanceTypeId=None, label="紧急工单", serviceItems=None):
        url = 'https://huiserver1.iotdataserver.net/es/order/save'
        data = {
            "customerName": customerName,
            "customerId": customerId,
            "contactName": contactName,
            "phone": phone,
            "country": country,
            "province": province,
            "city": city,
            "area": area,
            "address": address,
            "deptId": deptId,
            "deptName": deptName,
            "orderNo": orderNo,
            "orderType": orderType,
            "orderTypeId": orderTypeId,
            "dispatchType": dispatchType,
            "servicePerson": servicePerson,
            "servicePersonId": servicePersonId,
            "servicePersonPhone": servicePersonPhone,
            "assistPerson": assistPerson,
            "assistPersonId": assistPersonId,
            "poolIds": poolIds,
            "describe": describe,
            "productInfo": productInfo,
            "rootId": rootId,
            "maintenanceType": maintenanceType,
            "maintenanceTypeId": maintenanceTypeId,
            "label": label,
            "labelId": labelId,
            "expectedStartTime": expectedStartTime,
            "expectedEndTime": expectedEndTime,
            "picture": picture,
            "serviceItems": serviceItems,
            "fieldExtensions": fieldExtensions
        }
        if data['productInfo'] == None:
            data['productInfo'] = []
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result
