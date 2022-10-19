import hashlib
import random
import jsonpath
import requests
import logging
import datetime

# {
#     "address": "/es/productModel/delete/",        #url中的uri部分
#     "method": "get",#请求方法
#     "id": "765216192442179584",   #url中的id，默认为None，由其他接口写入
#     "describetion": "删除产品型号", #接口描述，必须正确，作为来源依据，以及日志名称
#     "params": {                   #param，如果没有，则设值为None
#             "param1": {           #第一个参数
#                   "nes":          #是否必填，如果非必填，则不写
#                   "type":         #类型，枚举，str，int   其他接口来源字段则不填
#                   "length":       #长度，字段长度范围      其他接口来源字段则不填
#             },
#             "param2": {
#                   "from":         #由哪个接口返回，填接口的describetion字段值，非其他接口来源字段不填
#                   “fromkey”:      #结果jsonpath
#             },
#     },
#     "data": {
#             "param1": {},
#             "param2": {},
#     },
host = 'https://huiservertest1.iotdataserver.net'

interfaces = [
    # 客户编号
    # {
    #     "address": "/es/common/getCode/GD",
    #     "method": "get",
    #     "id": None,
    #     "describetion": "获取客户编号",
    #     "params": None,
    #     "data": None
    # },
    {
        "times": 1,
        "address": "/es/sparePartsType/getTreeList",
        "method": "post",
        "id": None,
        "describetion": "getsparepartstype",
        "params": None,
        "data": None
    },
    {
        "times": 10,
        "address": "/es/spareParts/list",
        "method": "post",
        "id": None,
        "describetion": "sparepartslist",
        "params": None,
        "data": {
            "brands": {
                'nes': 1,
                'value': []
            },
            "sparePartsName": {
                'nes': 1,
                'value': ""
            },
            "typeId": {
                'nes': 1,
                'from': 'getsparepartstype',
                'fromkey': '$..id'
            },
            "current": {
                'nes': 1,
                'value': 1
            },
            "size": {
                'nes': 1,
                'value': 20
            }
        }
    }
]

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)


def get_cookie(name, password):
    url = 'https://huiservertest1.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies


cookie = get_cookie('sysadmin', 'hc300124')


# cookie = get_cookie('zhengjunpeng', 'abcd123456')

def random_str(lengths):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(lengths):
        random_str += base_str[random.randint(0, length)]
    return random_str


def random_int(lengths):
    random_int = ''
    base_int = '0123456789'
    length = len(base_int) - 1
    for i in range(lengths):
        random_int += base_int[random.randint(0, length)]
    return int(random_int)


def randc(type, length):
    ranlength = random.randint(1, length)
    if type == 'str':
        return random_str(ranlength)
    if type == 'int':
        return random_int(ranlength)


def make_params(dic=None):
    params = {}
    if dic == None:
        pass
    else:
        for key, value in dic.items():
            if 'from' in value:
                ran = ''
                for i in interfaces:
                    if i['describetion'] == value['from']:
                        fromre = run_interface(i)
                        ran = jsonpath.jsonpath(fromre, '%s' % value['fromkey'])
                        ran = ran[0]
                    else:
                        raise "无该接口"
            elif 'type' in value:
                ran = randc(value['type'], value['length'])
            else:
                ran = value['value']
            if 'nes' in value:
                params['%s' % key] = ran
            else:
                if random.randint(1, 2) == 1:
                    params['%s' % key] = ran
    return params


def make_data(dic=None):
    data = {}
    if dic == None:
        return None
    else:
        for key, value in dic.items():
            if 'from' in value:
                ran = ''
                for i in interfaces:
                    if i['describetion'] == value['from']:
                        fromre = run_interface(i)
                        ran = jsonpath.jsonpath(fromre, '%s' % value['fromkey'])
                        ran = ran[0]
                    else:
                        ran = None
            elif 'type' in value:
                ran = randc(value['type'], value['length'])
            else:
                ran = value['value']
            if 'nes' in value:
                data['%s' % key] = ran
            else:
                if random.randint(1, 2) == 1:
                    data['%s' % key] = ran
        return data


def make_url(uri, lid=None):
    if lid == None:
        url = '%s%s' % (host, uri)
    else:
        url = '%s%s%s' % (host, uri, lid)
    return url


def run_interface(interface):
    url = make_url(interface['address'], interface['id'])
    data = make_data(interface['data'])
    params = make_params(interface['params'])
    if interface['method'] == 'get':
        result = requests.get(url=url, cookies=cookie)
        print(result.text)
    elif interface['method'] == 'post':
        result = requests.post(url=url, cookies=cookie, params=params, json=data)
        print(result.text)
    elif interface['method'] == 'put':
        result = requests.put(url=url, cookies=cookie, params=params, json=data)
        print(result.text)
    else:
        result = requests.delete(url=url, cookies=cookie, params=params, json=data)
    file_handler = logging.FileHandler(filename='%s.log' % (interface['describetion']), encoding='UTF-8')
    logger.addHandler(file_handler)
    nowtime = datetime.datetime.now()
    if result.status_code != 200:
        logger.info('%s: %s' % (str(nowtime), result.text))
        logger.info('      url: %s' % url)
        logger.info('      data: %s' % data)
        logger.info('      params: %s' % params)
    logger.removeHandler(file_handler)
    return result.json()


for interface in interfaces:
    for i in range(interface['times']):
        run_interface(interface)
