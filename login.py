import hashlib
import threading
import time
import pymysql
import requests
from requests_toolbelt import MultipartEncoder


def get_cookie(name, password):
    url = 'https://huiservertest1.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('sysadmin', 'hc300124')


def create_order():
    url = 'https://huiservertest1.iotdataserver.net/es/order/save'
    nowtime = time.time()

    nowtime = str(nowtime).split('.')[0][0:9]
    data = {
        "orderNo": "GD20220829%s" % nowtime,
        "orderType": "调试工单",
        "customerName": "群武的公司（勿动）",
        "contactName": "范大海",
        "phone": "18606279845",
        "country": "中国",
        "province": "湖南省",
        "city": "长沙市",
        "area": "天心区",
        "address": "沙县",
        "deptId": "759149174878351360",
        "deptName": "群武的二级组织",
        "label": "紧急工单",
        "labelId": "754066338659602432",
        "expectedStartTime": "2022-08-31",
        "expectedEndTime": "2022-09-21",
        "productInfo": [
            {
                "id": "759052525107654656",
                "name": "test_052",
                "typeId": "750031402572271616",
                "typeName": "四边封制袋机",
                "code": "test_052",
                "modelId": "1557982893239799810",
                "modelName": "1234567890“1234567890“1234567890“"
            }
        ],
        "describe": "create_for_test",
        "orderTypeId": "3",
        "rootId": "3",
        "customerId": "755414014491926528"
    }
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("创建结果: %s" % result.text)
    return result.json()['data']['orderNo'], result.json()['data']['orderId']


def distribute_order(orderId):
    data = {
        "servicePerson": "郑俊鹏",
        "servicePersonId": "1559727011062153218",
        "servicePersonPhone": "13997707177",
        "assistPerson": [],
        "assistPersonId": [],
        "operate": "DISPATCH",
        "_id": "%s" % orderId
    }
    url = 'https://huiservertest1.iotdataserver.net/es/order/operate'
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("派单结果: %s" % result.text)


def start_order(orderId):
    data = {
        "_id": "%s" % orderId,
        "status": 4,
        "operate": "START"
    }
    url = 'https://huiservertest1.iotdataserver.net/es/order/operate'
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    print("开始结果: %s" % result.text)


# for i in range(10):
#     a, orderId = create_order()
#     time.sleep(1)
# distribute_order(orderId)
# start_order(orderId)
# data = {
#   "systemCode": "BJ20220830160838001",
#   "sparePartsCode": "1",
#   "sparePartsName": "bj_01",
#   "typeName": "类别1",
#   "typeIds": "_752531773667651584",
#   "typeId": "752531773667651584",
#   "sparePartsModel": "",
#   "criticalityName": "",
#   "criticalityId": "",
#   "brand": "",
#   "unitName": "",
#   "unitId": "",
#   "sparePartsDesc": ""
# }
# url = 'https://huiservertest1.iotdataserver.net/es/spareParts/saveSpareParts'
# for i in range(100):
#     nowtime = time.time()
#     nowtime = str(nowtime).split('.')[0][0:9]
#     data['sparePartsName'] = "bj_%s"%str(i)
#     data['systemCode'] = "BJ20220830%s"%nowtime
#     data['sparePartsCode'] = "bj_%s"%str(i)
#     result = requests.Session().post(url=url, cookies=cookie, json=data)
#     print(result.text)
url = 'https://huiservertest1.iotdataserver.net/es/spareParts/list'
data = {
    "brands": [],
    "sparePartsName": "",
    "typeId": "752531773667651584",
    "current": 1,
    "size": 20
}
db = pymysql.connect(host='10.44.219.250', port=23306,
                     user='root', passwd='inovance321', db='equipment_service_test', charset='utf8')
cursor = db.cursor()
ids = []
while True:
    result = requests.Session().post(url=url, cookies=cookie, json=data)
    resulttext = result.json()
    if len(resulttext['data']['records']) > 0:
        for record in resulttext['data']['records']:
            id = record['id']
            if id not in ids:
                sql = "INSERT INTO `t_product_model_spare` (`id`, `product_model_id`, `spare_parts_id`, `update_time`, `update_user`, `update_user_id`, `num`) VALUES (1, 752925000799133696, '%s', '2022-08-30', 'sysadmin', NULL, 1);"%id
                cursor.execute(sql)
                datas = cursor.fetchall()
                for data in datas:
                    print(data)
                db.commit()
                ids.append(id)
    else:
        break
    data['current'] += 1
# 批量加诉求类型
# url = 'https://huiservertest1.iotdataserver.net/es/appealType/copy'
# data = {
#     "typeName": "num_test",
#     "srcId": "3"
# }
# for i in range(50):
#     data['typeName'] = 'num_test%s'%i
#     result = requests.Session().post(url=url, cookies=cookie,json=data)
#     print(result.text)
# 批量删诉求类型
# listurl = 'https://huiservertest1.iotdataserver.net/es/appealType/list'
# data= {}
# result = requests.Session().post(url=listurl, cookies=cookie,json=data)
# url = 'https://huiservertest1.iotdataserver.net/es/appealType/delete/'
# for da in result.json()['data']:
#     if 'num' in da['typeName']:
#         numurl = '%s%s'%(url,da['id'])
#         print(numurl)
#         result = requests.delete(url=numurl, cookies=cookie)
#         print(result.text)
# 批量创建诉求
url = 'https://huiservertest1.iotdataserver.net/es/appeal/save'
data = {
    "appealCode": "SQ20220905134345001",
    "fullName": "群武的公司（勿动）",
    "contactName": "范大海",
    "phone": "18606279845",
    "country": "中国",
    "addressData": [
        "430000",
        "430100",
        "430103"
    ],
    "province": "湖南省",
    "city": "长沙市",
    "area": "天心区",
    "address": "沙县",
    "deptId": "759149174878351360",
    "deptName": "群武的二级组织",
    "labelId": "761594155119190016",
    "expectedStartTime": "2022-09-30 00:00:00",
    "expectedEndTime": "2022-09-30 00:00:00",
    "describe": 'for test',
    "appealType": "767075889235603456",
    "customerId": "755414014491926528",
    # "appealLabel": "一般",
    # "appealLabelId": "761594155119190016",
    "contactUserId": "755414014491926528",
    "customerName": "群武的公司（勿动）",
    "appealTypeName": "群武的默认诉求类型",
    "productInfo": []
}

data2 = {
    "appealCode": "SQ20220908153338001",
    "fullName": "群武的公司（勿动）",
    "contactName": "范大海",
    "phone": "18606279845",
    "country": "中国",
    "province": "湖南省",
    "city": "长沙市",
    "area": "天心区",
    "address": "沙县",
    "deptId": "759149174878351360",
    "deptName": "群武的二级组织",
    "labelId": "765275584923676672",
    "expectedStartTime": "2022-09-15 00:00:00",
    "expectedEndTime": "2022-09-16 00:00:00",
    "describe": "for_test1",
    "appealType": "767075889235603456",
    "customerId": "755414014491926528",
    "appealLabelId": "765275584923676672",
    "contactUserId": "755414014491926528",
    "customerName": "群武的公司（勿动）",
    "appealTypeName": "群武的默认诉求类型",
    "productInfo": []
}

def run_test():
    geturl = 'https://huiservertest1.iotdataserver.net/es/common/getCode/SQ'
    for i in range(10):
        result = requests.get(url=geturl, cookies=cookie)
        print(result.text)
        sqno = result.json()['data']
        data['appealCode']=sqno
        data['describe'] = 'for_test%s'%i
        result2 = requests.post(url=url, cookies=cookie, json=data)
        print(i)
        print(result2.text)
def run_test2():
    geturl = 'https://huiservertest1.iotdataserver.net/es/common/getCode/SQ'
    for i in range(10000):
        result = requests.get(url=geturl, cookies=cookie)
        print(result.text)
        sqno = result.json()['data']
        data['appealCode']=sqno
        data['describe'] = 'for_test%s'%i
        result2 = requests.post(url=url, cookies=cookie, json=data)
        print(i)
        print(result2.text)
thread1 = threading.Thread(name='t1',target= run_test())
# thread2 = threading.Thread(name='t2',target= run_test2())
# thread3 = threading.Thread(name='t2',target= run_test())
# thread4 = threading.Thread(name='t2',target= run_test())
# thread5 = threading.Thread(name='t2',target= run_test())
thread1.start()   #启动线程1
# thread2.start()   #启动线程2
# thread3.start()   #启动线程2
# thread4.start()   #启动线程2
# thread5.start()   #启动线程2
# urlfff = 'https://huiservertest1.iotdataserver.net/es/orderType/list'
# datafff = {}
# result2 = requests.post(url=urlfff, cookies=cookie, json=datafff)
# print(result2.text)
# for i in result2.json()['data']:
#     if 'test' in i['typeName']:
#         url2 = 'https://huiservertest1.iotdataserver.net/es/orderType/delete/%s'%i['id']
#         result2 = requests.delete(url=url2, cookies=cookie)
#         print(result2.text)
