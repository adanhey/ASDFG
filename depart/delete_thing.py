import requests
import setting

host = setting.host


def delete_location(cookie, locationid):
    url = '%s/es/storagelocation/delete/%s' % (host, locationid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)


def delete_ck(cookie, ckid):
    url = '%s/es/storage/delete/%s' % (host, ckid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)
    return result.json()['code']


def delete_gystype(cookie, gystypeid):
    url = '%s/es/supplierType/delete/%s' % (host, gystypeid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)
    return result.json()['code']

def delete_gys(cookie,gysid):
    url = '%s/es/supplier/delete/%s' % (host, gysid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)
    return result.json()['code']

def delete_spareparts(cookie,bjid):
    url = '%s/es/sparePartsType/delete/%s'%(host,bjid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)

def delete_bj(cookie,bjid):
    url = '%s/es/spareParts/delete/%s'%(host,bjid)
    result = requests.session().delete(url=url, cookies=cookie)
    print(result.text)
