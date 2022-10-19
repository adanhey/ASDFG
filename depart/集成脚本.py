from alllist import *
from delete_thing import *
from create_thing import *
import hashlib
import setting

host = setting.host


def get_cookie(name, password):
    url = '%s/itas-app/userLogin' % host
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('sysadmin', 'hc300124')


# 清空仓库下库位
def del_location_from_storagename(storagename, locationname=None):
    a = get_cangkutree(cookie, storagename)
    storageid = a['id']
    while True:
        locationlist = []
        page = 1
        location = get_kuwei(cookie=cookie, storageid=storageid, page=page, size=100)
        if locationname:
            for i in location['data']['records']:
                if locationname in i['storageLocationName']:
                    locationlist.append(i['id'])
        else:
            for i in location['data']['records']:
                locationlist.append(i['id'])
        for l in locationlist:
            delete_location(cookie, l)
        if len(location['data']['records']) < 100:
            break

def del_gys_from_gystype(typename):
    a = get_suppliertree(cookie, typename)
    gystypeid = a['id']
    while True:
        gyslist = []
        page = 1
        gys = sup_list(cookie=cookie, supid=gystypeid, page=page, size=100)
        for i in gys['data']['records']:
            gyslist.append(i['id'])
        for l in gyslist:
            delete_gys(cookie, l)
        if len(gys['data']['records']) < 100:
            break

# 清理子级仓库
def del_ck_from_ck(storagename):
    a = get_cangkutree(cookie, storagename)
    print(a)
    names = jsonpath.jsonpath(a, '$...storageName')
    ids = jsonpath.jsonpath(a, '$...id')
    for name in names:
        del_location_from_storagename(name)
    while len(ids) >= 1:
        print(ids)
        for i in ids:
            code = delete_ck(cookie, i)
            if code == 200:
                ids.remove(i)

# 清理子级供应商类别
def del_gysty_from_gysty(gystypename):
    a = get_suppliertree(cookie, gystypename)
    names = jsonpath.jsonpath(a, '$...typeName')
    ids = jsonpath.jsonpath(a, '$...id')
    for name in names:
        del_gys_from_gystype(name)
    while len(ids) >= 1:
        for i in ids:
            code = delete_gystype(cookie, i)
            if code == 200:
                ids.remove(i)

def add_kw_from_ck(storagename):
    a = get_cangkutree(cookie, storagename)
    print(a)
    create_kw(cookie, a['id'], a['ids'])
    for i in a['children']:
        create_kw(cookie, i['id'], i['ids'])
        for j in i['children']:
            create_kw(cookie, j['id'], j['ids'])


# 仓库及子仓库加库位
# add_kw_from_ck('一层0')
# del_ck_from_ck("一层%s" % i)
# del_location_from_storagename('浮')
# 新建仓库
# for i in range(3):
#     create_ck(cookie=cookie, name='一层%s' % i, managename='郑俊鹏')
#     for j in range(3):
#         create_ck(cookie=cookie, name='二层%s-%s' % (i, j), managename='郑俊鹏', parentName='一层%s' % i)
#         for z in range(3):
#             create_ck(cookie=cookie, name='三层%s-%s-%s' % (i, j, z), managename='郑俊鹏', parentName='二层%s-%s' % (i, j))
# create_ck(cookie=cookie, name='增加层级3', managename='郑俊鹏', parentName='增加')
del_ck_from_ck("一层0")
#新建供应商
# for i in range(3):
#     create_sup_type(cookie=cookie, name='一层%s' % i, code='一层%s' % i)
#     for j in range(3):
#         create_sup_type(cookie=cookie, name='二层%s-%s' % (i, j), code='二层%s-%s' % (i, j), typename='一层%s' % i)
#         for z in range(3):
#             create_sup_type(cookie=cookie, name='三层%s-%s-%s' % (i, j, z), code='三层%s-%s-%s' % (i, j, z), typename='二层%s-%s' % (i, j))

