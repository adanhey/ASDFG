import requests
from ASDFG.interface_ability.list_base import *


class Other_request(Interface_list):
    def set_things_used(self, thing, things_id, used=1):
        '''
        启停用对象
        :param thing: 启停用类型uri的识别部分，支持“storagelocation”，“spareParts”
        :param things_id: 启停用对象的id
        :param used: 启停用，0停用，1启用
        :return: 返回请求结果
        '''
        url = '%s/es/%s/setUsed?id=%s&used=%s' % (self.host, thing, things_id, used)
        result = requests.session().post(url=url, cookies=self.cookie)
        return result

    def supplierSparePart_connect(self, spare_id, *args):
        '''
        备件绑定供应商
        :param spare_id: 备件id
        :param args: 供应商id
        '''
        url = '%s/es/supplierSparePart/save' % self.host
        data = {
            "id": spare_id,
            "supplierEntities": []
        }
        for supplier in args:
            data['supplierEntities'].append({"id": supplier})
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def businesslog(self, businessType, commonId):
        '''
        查询日志
        :param businessType: 查询类型
        :param commonId: 对象id
        '''
        url = '%s/es/common/getBusinessLog' % self.host
        data = {
            "businessType": businessType,
            "commonId": commonId
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def storage_in_apply(self, incode, storagename, storageid, detaillist, inouttype=1, remark=""):
        '''
        创建入库申请
        :param incode:
        :param storagename:
        :param storageid:
        :param detaillist:
        :param inouttype:
        :param remark:
        :return:
        '''
        url = '%s/es/storageinoutdetails/storageInApply' % self.host
        data = {
            "storageInOutCode": incode,
            "storageInOutRemark": remark,
            "storageInOutType": inouttype,
            "storageName": storagename,
            "storageId": storageid,
            "storageInApplyDetailVoList": detaillist
            #     [
            #     {
            #         "storageLocationName": "货架添加测试1-1-1-3",
            #         "storageLocationId": "1579794771600867332",
            #         "storageInOutNum": 1,
            #         "sparePartsName": "3333333",
            #         "sparePartsId": "779436331660120064",
            #         "sparePartsCode": "33333333333",
            #         "typeName": "类别AA01",
            #         "sparePartsModel": "333",
            #         "brand": "",
            #         "unitName": "批",
            #         "storageName": "test1"
            #     }
            # ]
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def storage_in_Approval(self, siid, storageInId, storageInCode, storageInOutDetails, storageInType=1,
                            approvalLevel=1, sparePartsTypeNum=1, approvalStatus=1, status=4, remark=None):
        url = '%s/es/storageInApproval/handle' % self.host
        data = {
            "storageInApprovalEntity": {
                "id": siid,
                "storageInId": storageInId,
                "storageInCode": storageInCode,
                "storageInType": storageInType,
                "approvalLevel": approvalLevel,
                "approverId": "771797340555354112",
                "approver": "22.2",
                "status": status,
                "approvalStatus": approvalStatus,
                "sparePartsTypeNum": sparePartsTypeNum,
                "remark": remark,
                "updateTime": "2022-10-27 14:36:31",
                "proposeTime":"2022-10-27 14:36:31"
            },
            "storageInOutDetails": storageInOutDetails
        }
        print(data)
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def storage_out_Approval(self, siid, storageInId, storageInCode, storageInOutDetails, storageInType=1,
                             approvalLevel=1, sparePartsTypeNum=1, approvalStatus=1, status=4, remark=None):
        url = '%s/es/storageOutApproval/approval' % self.host
        data = {
            "storageOutApprovalEntity": {
                "id": siid,
                "storageOutId": storageInId,
                "storageOutCode": storageInCode,
                "storageOutType": storageInType,
                "approvalLevel": approvalLevel,
                "approverId": "771797340555354112",
                "approver": "22.2",
                "status": status,
                "approvalStatus": approvalStatus,
                "sparePartsTypeNum": sparePartsTypeNum,
                "remark": remark,
                "updateTime": "2022-10-27 14:36:31",
                "proposeTime": "2022-10-27 14:36:31"
            },
            "storageInOutDetails": storageInOutDetails
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def storage_out_apply(self, outcode, storagename, storageid, detaillist, recipientId=None, recipientName=None,
                          targetStorageId=None, targetStorageName=None, remark="", storageInOutType=11, type=2):
        '''
        出库申请
        :param outcode: 出库编号
        :param storagename: 仓库名称
        :param storageid: 仓库id
        :param detaillist: 备件列表
        :param recipientId: 接受人id
        :param recipientName: 接受人姓名
        :param targetStorageId: 目标仓库id
        :param targetStorageName: 目标仓库名称
        :param remark: 备注
        :param storageInOutType: 进出类型，11为申领，12为调拨
        :param type:
        :return:
        '''
        url = '%s/es/storageinoutdetails/storageOutApply' % self.host
        data = {
            "type": type,
            "storageInOutType": storageInOutType,
            "storageInOutCode": outcode,
            "storageInOutRemark": remark,
            "storageName": storagename,
            "storageId": storageid,
            "targetStorageId": targetStorageId,
            "targetStorageName": targetStorageName,
            "recipientId": recipientId,
            "recipientName": recipientName,
            "storageOutDetails": detaillist
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def emp_diaobo(self,allocationNo,transfereeId,transfereeName,recipientId,recipientName,detaillist,allocationType=1,remark=None):
        url = '%s/es/employeeSparePart/createAllocation' % self.host
        data = {
            "allocationType": allocationType,
            "allocationNo": allocationNo,
            "remark": remark,
            "recipientId": recipientId,
            "recipientName": recipientName,
            "personalAllocationDetailList": detaillist,
            "transfereeId": transfereeId,
            "transfereeName": transfereeName
        }
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

    def employeeSparePart_approvalAllocation(self, allocation_id, status=1, personalAllocationDetailList=None,
                                             remark=None):
        '''
        个人调拨记录操作
        :param allocation_id:
        :param status:
        :param personalAllocationDetailList:
        :return:
        '''
        url = '%s/es/employeeSparePart/approvalAllocation' % self.host
        data = {
            "id": allocation_id,
            "status": status
        }
        if personalAllocationDetailList is not None:
            data['personalAllocationDetailList'] = personalAllocationDetailList
        if remark is not None:
            data['remark'] = remark
        result = requests.session().post(url=url, cookies=self.cookie, json=data)
        return result

# jj = Other_request()
# print(jj.businesslog("spareParts", '779436331660120064').text)
