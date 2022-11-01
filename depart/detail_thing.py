import requests
from ASDFG.interface_ability.list_base import *

class Detail_request(Interface_list):
    def sad(self):
        pass

    def storageInOut_info(self,inoutid):
        url = '%s/es/storageInOut/info/%s'%(self.host,inoutid)
        result = requests.session().get(url=url, cookies=self.cookie)
        return result