import json
from ASDFG.interface_ability.list_base import *
import requests


class List_request(Interface_list):
    def get_suppliertree(self, typeName):
        url = '%s/es/supplierType/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie, json={})
        jsonresult = self.find_from_result(result.json(), "typeName", typeName)
        return jsonresult

    def get_storagetree(self, storagetypename):
        url = '%s/es/storage/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie, json={})
        jsonresult = self.find_from_result(result.json(), "storageName", storagetypename)
        return jsonresult

    def get_sparePartstree(self, sparePartsname):
        url = '%s/es/sparePartsType/getTreeList' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        jsonresult = self.find_from_result(result.json(), "typeName", sparePartsname)
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

    def dict_list(self, dictcode, children=None):
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

    def Supplier_List(self, supid, page, size=100):
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

    def list_spares(self, typename, size=100, page=1, name=None):
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

    def list_storage_spareparts(self, storageId, sparePartsName="", sparePartsCode=""):
        '''
        查询仓库备件库存
        :param storageId: 仓库id
        :param sparePartsName: 备件名称筛选
        :param sparePartsCode: 备件编码
        :return:
        '''
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

    def spare_listbystorage(self, depart_id, storageName=None, page=1, size=100):
        '''
        根据备件id查询所有仓库下该备件库存
        :param depart_id: 备件id
        :param storageName: 筛选仓库名称
        '''
        url = '%s/es/storageSpareParts/getListBySpareParts' % self.host
        data = {
            "storageName": storageName,
            "id": depart_id,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def spare_listbypersonal(self, depart_id, employeeName=None, page=1, size=100):
        '''
        根据备件id查询所有个人仓库下该备件库存
        :param depart_id: 备件id
        :param storageName: 筛选员工名称
        '''
        url = '%s/es/personalSpareParts/getListBySpareParts' % self.host
        data = {
            "employeeName": employeeName,
            "id": depart_id,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def SupplierList_byspare(self, spare_id, page=1, size=100):
        url = '%s/es/spareParts/getSupplierList' % self.host
        data = {
            "id": spare_id,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def appeal_list(self, page=1, size=100, appealView=None, customerId=None, contactName=None, appealCode=None,
                    orderId=None, startTime=None, endTime=None, appealTypes=None, *args):
        url = '%s/es/appeal/list' % self.host
        data = {
            "appealView": appealView,
            "customerId": customerId,
            "contactName": contactName,
            "appealCode": appealCode,
            "orderId": orderId,
            "startTime": startTime,
            "endTime": endTime,
            "appealTypes": appealTypes,
            "status": args,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def appealtype_list(self):
        url = '%s/es/appealType/list' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        return result

    def customer_list(self, fullName=None, page=1, size=100):
        url = '%s/es/customer/list' % self.host
        data = {
            "size": size,
            "current": page,
            "fullName": fullName
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def ordertype_list(self):
        url = '%s/es/orderType/list' % self.host
        result = requests.session().post(url=url, cookies=self.cookie)
        return result

    def order_list(self, status=None, orderView=None, orderTypes=None, orderNo=None, creatorId=None,
                   servicePersonId=None, assistPersonId=None, customerId=None, startTime=None, endTime=None, all=None,
                   page=1, size=100):
        url = '%s/es/order/list' % self.host
        data = {
            "status": status,
            "orderView": orderView,
            "orderTypes": orderTypes,
            "orderNo": orderNo,
            "creatorId": creatorId,
            "servicePersonId": servicePersonId,
            "assistPersonId": assistPersonId,
            "customerId": customerId,
            "startTime": startTime,
            "endTime": endTime,
            "all": all,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def employee_list_by_query(self, deptIds=None, name=None, page=1, size=100):
        url = '%s/es/workOrderStaffStatistics/queryStaff' % self.host
        data = {
            "deptIds": deptIds,
            "name": name,
            "current": page,
            "size": size
        }
        if data['deptIds'] == None:
            data['deptIds'] = []
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def employee_SparePart_list(self, visualAngleType=1, allocationNo="", personalParam="", applyEndTime=None,
                                applyStartTime=None, status=None, page=1, size=100):
        if status is None:
            status = []
        url = '%s/es/employeeSparePart/queryAllocation' % self.host
        data = {
            "visualAngleType": visualAngleType,
            "allocationNo": allocationNo,
            "personalParam": personalParam,
            "applyStartTime": applyStartTime,
            "applyEndTime": applyEndTime,
            "status": status,
            "current": page,
            "size": size
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

rarr = List_request()
# print(rarr.employee_SparePart_list().text)
