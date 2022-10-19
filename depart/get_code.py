import requests
import jsonpath
import setting

host = setting.host


def gys_code(cookie):
    url = '%s/es/common/getCode/GYS' % host
    result = requests.session().get(url=url, cookies=cookie)
    return result.json()['data']


def ck_code(cookie):
    url = '%s/es/common/getCode/ck' % host
    result = requests.session().get(url=url, cookies=cookie)
    return result.json()['data']

def bj_code(cookie):
    url = '%s/es/common/getCode/BJ'%host
    result = requests.session().get(url=url, cookies=cookie)
    return result.json()['data']