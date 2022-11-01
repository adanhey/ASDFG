import datetime
import threading
import time

from list_thing import *
from delete_thing import *
from create_thing import *
from detail_thing import *
from other_use import *

list_request = List_request()
delete_request = Delete_request()
create_request = Create_request()
other_request = Other_request()
detail_request = Detail_request()


# 清空仓库下库位
def del_location_from_storagename(storagename, locationname=None):
    locationresult = list_request.get_storagetree(storagename)
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
    a = list_request.get_storagetree(storagename)
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
    a = list_request.get_storagetree(storagename)
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
                                         expectedStartTime=nowday, expectedEndTime=nowday, rootId=typeresult['rootId'])
    return result


def storage_in_applyquickly(codetype, storagename, *args):
    inoutcode = create_request.get_code(codetype)
    storageid = list_request.get_storagetree(storagename)['id']
    # 备件类别---备件名称---仓位名称---数量
    sparklist = []
    for i in args:
        detail = i.split('---')
        locationresult = list_request.get_location(storageid, storagelocationname=detail[2])
        locationid = locationresult['data']['records'][0]['id']
        spareresult = list_request.list_spares(detail[0], name=str(detail[1]))
        sparedetail = spareresult['data']['records'][0]
        data = {
            "storageLocationName": detail[2],
            "storageLocationId": locationid,
            "storageInOutNum": int(detail[3]),
            "sparePartsName": detail[1],
            "sparePartsId": sparedetail['id'],
            "sparePartsCode": sparedetail['sparePartsCode'],
            "typeName": sparedetail['typeName'],
            "sparePartsModel": sparedetail['sparePartsModel'],
            "brand": sparedetail['brand'],
            "unitName": sparedetail['unitName'],
            "storageName": storagename
        }
        print(data)
        sparklist.append(data)
    result = other_request.storage_in_apply(inoutcode, storagename, storageid, sparklist)
    return result


def storage_out_applyquickly(codetype, storagename, recipientName=None, targetstoragename=None, outype=11, *args):
    inoutcode = create_request.get_code(codetype)
    storageid = list_request.get_storagetree(storagename)['id']
    targetstorageid = None
    recipientid = None
    if targetstoragename:
        targetstorageid = list_request.get_storagetree(storagename)['id']
    if recipientName:
        recipientid = list_request.emp_list(name=recipientName)['id']
    # 备件类别---备件名称---仓位名称---数量
    sparklist = []
    for i in args:
        detail = i.split('---')
        locationresult = list_request.get_location(storageid, storagelocationname=detail[2])
        locationid = locationresult['data']['records'][0]['id']
        spareresult = list_request.list_spares(detail[0], name=str(detail[1]))
        sparedetail = spareresult['data']['records'][0]
        data = {
            "storageLocationName": detail[2],
            "storageLocationId": locationid,
            "storageInOutNum": int(detail[3]),
            "sparePartsName": detail[1],
            "sparePartsId": sparedetail['id'],
            "sparePartsCode": sparedetail['sparePartsCode'],
            "typeName": sparedetail['typeName'],
            "sparePartsModel": sparedetail['sparePartsModel'],
            "brand": sparedetail['brand'],
            "unitName": sparedetail['unitName'],
            "storageName": storagename
        }
        sparklist.append(data)
    result = other_request.storage_out_apply(outcode=inoutcode, storagename=storagename, storageid=storageid,
                                             detaillist=sparklist, recipientId=recipientid, recipientName=recipientName,
                                             targetStorageId=targetstorageid, targetStorageName=targetstoragename,
                                             storageInOutType=outype)
    return result


def personaldb_quickly(empname, receivername, *args):
    dbcode = create_request.get_code("DB")
    empnameid = list_request.emp_list(name=empname)['id']
    receiverid = list_request.emp_list(name=receivername)['id']
    # 备件类别---备件名称---数量
    sparklist = []
    for i in args:
        detail = i.split('---')
        personaldb = list_request.personallsrare_list(empnameid)
        personaldbid = list_request.find_from_result(personaldb.json(), "sparePartsName", detail[1])['id']
        spareresult = list_request.list_spares(detail[0], name=str(detail[1]))
        sparedetail = spareresult['data']['records'][0]
        data = {
            "allocationNum": int(detail[2]),
            "sparePartsName": detail[1],
            "sparePartsId": sparedetail['id'],
            "sparePartsCode": sparedetail['sparePartsCode'],
            "typeName": sparedetail['typeName'],
            "sparePartsModel": sparedetail['sparePartsModel'],
            "brand": sparedetail['brand'],
            "unitName": sparedetail['unitName'],
            "storageNum": 1,
            "type": 2,
            "personalSparePartsId": personaldbid
        }
        sparklist.append(data)
    result = other_request.emp_diaobo(dbcode, empnameid, empname, receiverid, receivername, sparklist)
    return result


def approve_lots(size):
    result = list_request.approval_in_list(size=size).json()
    time.sleep(3)
    nowtime = time.time()
    for i in result['data']['records']:
        detail_result = detail_request.storageInOut_info(i['storageInId']).json()
        storageInOutDetails = detail_result['data']['storageInOutDetailVoList']
        print('%s:  %s' % (nowtime, other_request.storage_in_Approval(siid=i['id'], storageInId=i['storageInId'],
                                                                      storageInCode=i['storageInCode'],
                                                                      storageInOutDetails=storageInOutDetails).text))
        result2 = list_request.approval_in_list(storageInCode=i['storageInCode'], size=1).json()
        record = result2['data']['records'][0]
        print('%s:  %s' % (nowtime, other_request.storage_in_Approval(siid=record['id'],
                                                                      storageInId=record['storageInId'],
                                                                      storageInCode=record['storageInCode'],
                                                                      storageInOutDetails=storageInOutDetails,
                                                                      approvalLevel=2).text))


def approve_out_lots(size):
    result = list_request.approval_out_list(size=size).json()
    for i in result['data']['records']:
        detail_result = detail_request.storageInOut_info(i['storageOutId']).json()
        storageInOutDetails = detail_result['data']['storageInOutDetailVoList']
        print(other_request.storage_out_Approval(siid=i['id'], storageInId=i['storageOutId'],
                                                 storageInCode=i['storageOutCode'],
                                                 storageInOutDetails=storageInOutDetails).text)


def cre_bj(typename):
    result = list_request.get_sparePartstree(typename)
    result = create_request.find_from_result(result, "typeName", None, 1)
    print(result)
    for i in result:
        name = i
        for j in range(100):
            bjcode = create_request.get_code("BJ")
            print("%s: %s" % (typename, create_request.create_bj(name, "bj_%s" % j, bjcode).text))


def st_in(typename):
    for i in range(100):
        storage_in_applyquickly("CG", "00000000", "%s---bj_%s---kukuwei-10---100" % (typename, i))


def st_out(bjname):
    for i in range(100):
        print(storage_out_applyquickly("SL", "00000000", "admin", None, 11,
                                       "晶体管0-0-2---%s---kukuwei-10---1" % bjname).text)


thread1 = threading.Thread(name='t1', target=approve_lots, args=(1,))
thread2 = threading.Thread(name='t2', target=approve_lots, args=(1,))
thread3 = threading.Thread(name='t3', target=approve_lots, args=(1,))
thread4 = threading.Thread(name='t4', target=approve_lots, args=(1,))
thread5 = threading.Thread(name='t5', target=approve_lots, args=(1,))
thread6 = threading.Thread(name='t6', target=approve_lots, args=(1,))
thread7 = threading.Thread(name='t7', target=approve_lots, args=(1,))
thread8 = threading.Thread(name='t8', target=approve_lots, args=(1,))
thread9 = threading.Thread(name='t9', target=approve_lots, args=(1,))
thread1.start()  # 启动线程1
thread2.start()  # 启动线程2
thread3.start()  # 启动线程3
thread4.start()  # 启动线程4
thread5.start()  # 启动线程5
thread6.start()  # 启动线程6
thread7.start()  # 启动线程7
thread8.start()  # 启动线程8
thread9.start()  # 启动线程9


# thread1 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread2 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread3 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread4 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread5 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread6 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread7 = threading.Thread(name='t1', target=approve_lots, args=(1,))
# thread8 = threading.Thread(name='t8', target=approve_lots, args=(1,))
# thread9 = threading.Thread(name='t9', target=approve_lots, args=(1,))
# thread1.start()  # 启动线程1
# thread2.start()  # 启动线程2
# thread3.start()  # 启动线程2
# thread4.start()  # 启动线程2
# thread5.start()  # 启动线程2
# thread6.start()  # 启动线程2
# thread7.start()  # 启动线程2
# thread8.start()  # 启动线程2
# thread9.start()  # 启动线程2
