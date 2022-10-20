import datetime
import time

from list_thing import *
from delete_thing import *
from create_thing import *

list_request = List_request()
delete_request = Delete_request()
create_request = Create_request()


# 清空仓库下库位
def del_location_from_storagename(storagename, locationname=None):
    locationresult = list_request.get_cangkutree(storagename)
    storageid = locationresult['id']
    while True:
        locationlist = []
        page = 1
        location = list_request.get_location(storageid=storageid, page=page, size=100)
        if locationname:
            for i in location['data']['records']:
                if locationname in i['storageLocationName']:
                    locationlist.append(i['id'])
        else:
            for i in location['data']['records']:
                locationlist.append(i['id'])
        for l in locationlist:
            delete_request.delete_location(l)
        if len(location['data']['records']) < 100:
            break


def del_gys_from_gystype(typename):
    listresult = list_request.get_suppliertree(typename)
    gystypeid = listresult['id']
    while True:
        gyslist = []
        page = 1
        gys = list_request.Supplier_List(supid=gystypeid, page=page, size=100)
        for i in gys['data']['records']:
            gyslist.append(i['id'])
        for l in gyslist:
            delete_request.delete_gys(l)
        if len(gys['data']['records']) < 100:
            break


# 清理子级仓库
def del_ck_from_ck(storagename):
    a = list_request.get_cangkutree(storagename)
    names = jsonpath.jsonpath(a, '$...storageName')
    ids = jsonpath.jsonpath(a, '$...id')
    for name in names:
        del_location_from_storagename(name)
    while len(ids) >= 1:
        for i in ids:
            code = delete_request.delete_ck(i)
            if code == 200:
                ids.remove(i)


# 清理子级供应商类别
def del_gysty_from_gysty(gystypename):
    a = list_request.get_suppliertree(gystypename)
    names = jsonpath.jsonpath(a, '$...typeName')
    ids = jsonpath.jsonpath(a, '$...id')
    for name in names:
        del_gys_from_gystype(name)
    while len(ids) >= 1:
        for i in ids:
            code = delete_request.delete_gystype(i)
            if code == 200:
                ids.remove(i)


def add_kw_from_ck(storagename):
    a = list_request.get_cangkutree(storagename)
    create_request.create_kw(a['id'], a['ids'])
    for i in a['children']:
        create_request.create_kw(i['id'], i['ids'])
        for j in i['children']:
            create_request.create_kw(j['id'], j['ids'])


def create_appeal_quickly(appealtypename, customerName, appeallabelname="一般"):
    typelist = list_request.appealtype_list().json()
    typeresult = list_request.find_from_result(typelist, "typeName", appealtypename)
    labellist = list_request.dict_list("appealLabel", "true")
    labelresult = list_request.find_from_result(labellist, "dictKey", appeallabelname)
    customerlist = list_request.customer_list(customerName).json()
    customerresult = list_request.find_from_result(customerlist, "fullName", customerName)
    appealcode = create_request.get_code("SQ")
    result = create_request.create_appeal(appealTypeName=appealtypename, appealType=typeresult['id'],
                                          appealLabel=appeallabelname, appealLabelId=labelresult['id'],
                                          customerId=customerresult['id'], customerName=customerresult['fullName'],
                                          labelId=labelresult['id'], contactName=customerresult['contactName'],
                                          phone=customerresult['phone'], country=customerresult['country'],
                                          city=customerresult['city'], area=customerresult['area'],
                                          address=customerresult['address'], deptId=customerresult['organizationId'],
                                          deptName=customerresult['organization'], appealCode=appealcode)
    return result


def create_orderquickly(ordertypename, customerName, orderlabel="紧急工单"):
    nowday = datetime.datetime.now().strftime('%Y-%m-%d')
    typelist = list_request.ordertype_list().json()
    typeresult = list_request.find_from_result(typelist, "typeName", ordertypename)
    labellist = list_request.dict_list("orderLabel", "true")
    labelresult = list_request.find_from_result(labellist, "dictKey", orderlabel)
    customerlist = list_request.customer_list(customerName).json()
    customerresult = list_request.find_from_result(customerlist, "fullName", customerName)
    ordercode = create_request.get_code("GD")
    result = create_request.create_order(orderType=ordertypename, orderTypeId=typeresult['id'], label=orderlabel,
                                         labelId=labelresult['id'], customerId=customerresult['id'],
                                         customerName=customerresult['fullName'],
                                         contactName=customerresult['contactName'], phone=customerresult['phone'],
                                         country=customerresult['country'], city=customerresult['city'],
                                         area=customerresult['area'], address=customerresult['address'],
                                         deptId=customerresult['organizationId'],
                                         deptName=customerresult['organization'], orderNo=ordercode,
                                         expectedStartTime=nowday, expectedEndTime=nowday,rootId=typeresult['rootId'])
    return result


print(create_orderquickly("调试工单", "1", "紧急工单").text)
# 仓库及子仓库加库位
# add_kw_from_ck('一层0')
# del_ck_from_ck("一层%s" % i)
# del_location_from_storagename('浮')
# 新建仓库
# for i in range(3):
#     create_ck( name='一层%s' % i, managename='郑俊鹏')
#     for j in range(3):
#         create_ck( name='二层%s-%s' % (i, j), managename='郑俊鹏', parentName='一层%s' % i)
#         for z in range(3):
#             create_ck( name='三层%s-%s-%s' % (i, j, z), managename='郑俊鹏', parentName='二层%s-%s' % (i, j))
# create_ck( name='增加层级3', managename='郑俊鹏', parentName='增加')
# del_ck_from_ck("一层0")
# 新建供应商
# for i in range(3):
#     create_sup_type( name='一层%s' % i, code='一层%s' % i)
#     for j in range(3):
#         create_sup_type( name='二层%s-%s' % (i, j), code='二层%s-%s' % (i, j), typename='一层%s' % i)
#         for z in range(3):
#             create_sup_type( name='三层%s-%s-%s' % (i, j, z), code='三层%s-%s-%s' % (i, j, z), typename='二层%s-%s' % (i, j))
