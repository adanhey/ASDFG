import requests
from ASDFG.interface_ability.code_base import *


class code_request(Interface_code):
    def gys_code(self):
        url = '%s/es/common/getCode/GYS' % self.host
        result = requests.session().get(url=url, cookies=self.cookie)
        return result.json()['data']

    def ck_code(self):
        url = '%s/es/common/getCode/ck' % self.host
        result = requests.session().get(url=url, cookies=self.cookie)
        return result.json()['data']

    def bj_code(self):
        url = '%s/es/common/getCode/BJ' % self.host
        result = requests.session().get(url=url, cookies=self.cookie)
        return result.json()['data']
