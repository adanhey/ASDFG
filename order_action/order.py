from ASDFG.depart.create_thing import *
import requests


class order_request(Create_request):
    def order_detail(self, order_id):
        url = '%s/es/order/detail/%s' % (self.host, order_id)
        result = requests.Session().get(url=url, cookies=self.cookie)
        return result

