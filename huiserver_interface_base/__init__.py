import hashlib
import requests
from ASDFG import setting

host = setting.host

class Huiserver_interface():
    def __init__(self):
        self.host = host
        self.cookie = self.get_cookie("sysadmin","hc300124")
    def get_cookie(self,name, password):
        url = '%s/itas-app/userLogin' % host
        md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
        data = {"userName": name, "password": md5_pd}
        login = requests.post(url=url, data=data)
        assert login.status_code == 200
        return login.cookies