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


jj = Other_request()
print(jj.businesslog("spareParts", '779436331660120064').text)
