import hashlib
import json
import math
import time

import requests


def get_cookie(name, password):
    url = 'https://huiservertest1.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('sysadmin', 'hc300124')

url = 'https://huiservertest1.iotdataserver.net/es/appeal/list'
data = {
    "appealView": "0",
    "status": [],
    "current": 1,
    "size": 100
}
size = 100
result = requests.post(url=url, json=data, cookies=cookie)
total = result.json()['data']['total']
ids = []
page = math.ceil(total / size)
print(page)
for i in range(1, page + 1):
    data['current'] = i
    result = requests.post(url=url, json=data, cookies=cookie)
    for j in result.json()['data']['records']:
        ids.append(j['_id'])
    print(i)
    if len(ids) > 10000:
        break
# ids = str(ids)
# ids = ids.replace("'", '"')
# print(ids)
url = 'https://huiservertest1.iotdataserver.net/es/appeal/export'
data = {
    "ids": ids
}
result = requests.post(url=url, json=data, cookies=cookie,timeout=5000)
now = int(time.time())
file_name = "%s.xlsx" % now
with open(file_name, 'wb') as f:
    f.write(result.content)
print(result.text)
