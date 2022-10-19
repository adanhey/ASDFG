import requests
from ASDFG import setting
from ASDFG.interface_ability.delete_base import *
host = setting.host

class Delete_request(Interface_delete):
    def delete_location(self, locationid):
        url = '%s/es/storagelocation/delete/%s' % (host, locationid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result
    
    
    def delete_ck(self, ckid):
        url = '%s/es/storage/delete/%s' % (host, ckid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result.json()['code']
    
    
    def delete_gystype(self, gystypeid):
        url = '%s/es/supplierType/delete/%s' % (host, gystypeid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result.json()['code']
    
    def delete_gys(self,gysid):
        url = '%s/es/supplier/delete/%s' % (host, gysid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result.json()['code']
    
    def delete_spareparts(self,bjid):
        url = '%s/es/sparePartsType/delete/%s'%(host,bjid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result
    
    def delete_bj(self,bjid):
        url = '%s/es/spareParts/delete/%s'%(host,bjid)
        result = requests.session().delete(url=url, cookies=self.cookie)
        return result
