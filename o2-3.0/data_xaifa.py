import hashlib
import json
import math
import random
import time
import requests
import websocket


def get_cookie(name, password):
    url = 'https://pastest.iotdataserver.net/itas-app/userLogin'
    md5_pd = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    data = {"userName": name, "password": md5_pd}
    login = requests.post(url=url, data=data)
    assert login.status_code == 200
    return login.cookies
cookie = get_cookie("","")

def get_MonitorDeviceManage(devicename):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceMonitor/getAppMonitorDeviceManageList'
    data = {
        "searchName": "",
        "companyId": "",
        "deviceStatus": "",
        "productId": "",
        "current": 1,
        "size": 10
    }
    size = 10
    result = requests.post(url=url, json=data, cookies=cookie)
    total = int(result.json()['data']['total'])
    page = math.ceil(total / size) + 1
    for i in range(1, page + 1):
        data['current'] = i
        result = requests.post(url=url, json=data, cookies=cookie)
        for record in result.json()['data']['records']:
            if record['deviceName'] == devicename:
                return record


def get_module_data(deviceid, name):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/deviceManage/getDataSourecListByDeviceId?deviceId=%s' % deviceid
    result = requests.get(url=url, cookies=cookie)
    for source in result.json()['data']:
        if source['sourceName'] == name:
            return source


def get_grouplist(protocolid):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/elementBusinessGroup/getGroupListByProtocolId?protocolId=%s' % protocolid
    result = requests.get(url=url, cookies=cookie)
    return result.json()['data']


def get_data(groupid, protocolid, regCode):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/elementItemGroup/getRealTimeData'
    data = {
        "current": "1",
        "size": "1000",
        "protocolId": "%s" % protocolid,
        "regCode": "%s" % regCode,
        "businessGroupId": "%s" % groupid
    }
    result = requests.post(url=url, json=data, cookies=cookie)
    return result.json()


def get_single_data(groupdata, protocolid, name, regcode):
    for obj in groupdata:
        groupid = obj['id']
        groupname = obj['groupName']
        b = get_data(groupid, protocolid, regcode)
        for i in b['data']['records']:
            if i['name'] == name:
                return i, groupname


def get_td(vitid):
    url = 'https://pastest.iotdataserver.net/uweb-monitor/targetDevice/getTdTagInfoByDeviceId?deviceId=%s' % vitid
    result = requests.get(url=url, cookies=cookie)
    return result.json()


def xiafa(tdserial, deviceserial, virtualdeviceid, address, itemid, value):
    sid = cookie['sid']
    data = {
        "deviceSerial": deviceserial,
        "tdSerial": tdserial,
        "sid": sid,
        "msgType": "SEND_REAL_TIME_COMMAND_REQ",
        "Command": {
            "sid": sid,
            "elementCount": 1,
            "valueType": 1,
            "elementType": 1,
            "operateType": 2,
            "address": address,
            "name": "实时数据页面下发",
            "deviceId": virtualdeviceid,
            "itemId": itemid,
            "value": value
        }
    }
    ws = websocket.create_connection("wss://uwebsockettest.iotdataserver.net/uwebsocket")
    ws.send(str(data))
    result = ws.recv()
    print(str(result))
    ws.close()


def get_value(deviceserial, tdserial, tadatatags, rollname):
    sid = cookie['sid']
    data = {
        "msgType": "SERVER_AUTH_REQ",
        "sid": sid
    }
    ws = websocket.create_connection("wss://uwebsockettest.iotdataserver.net/uwebsocket")
    ws.send(str(data))
    result = ws.recv()
    print(result)
    sessionid = json.loads(result)['sessionId']
    data = {
        "deviceSerial": deviceserial,
        "tdSerial": tdserial,
        "tdDataTags": tadatatags,
        "sid": sid,
        "dnss": "false",
        "msgType": "GET_TD_REALTIME_DATA_REQ",
        "rdtsHost": "rdts.iotdataserver.net",
        "from": "gdhs_002@inovance",
        "to": "evdhs_033_test",
        "version": "1.0",
        "proxy": "",
        "sessionId": sessionid
    }
    ws.send(str(data))
    result = ws.recv()
    print(result)
    securityCode = json.loads(result)['data']['securityCode']
    data = {
        "deviceSerial": deviceserial,
        "tdSerial": tdserial,
        "tdDataTags": tadatatags,
        "sid": sid,
        "dnss": "false",
        "msgType": "TD_REALTIME_DATA_ESTABLISH_REQ",
        "rdtsHost": "rdts.iotdataserver.net",
        "from": "gdhs_002@inovance",
        "to": "evdhs_033_test",
        "version": "1.0",
        "proxy": "",
        "sessionId": sessionid,
        "securityCode": securityCode
    }
    ws.send(str(data))
    value = None
    C=1
    while True:
        result = ws.recv()
        print(result)
        C+=1
        time.sleep(2)
        if 'data' in json.loads(result):
            print(result)
            for i in json.loads(result)['data']:
                if i['name'] == rollname:
                    value = i['value']
                    break
        elif C>10:
            time.sleep(2)
            break
        else:
            ws.send(str(data))
        if value:
            ws.close()
            return value


def mission_xiafa(devicename, connectname, rollname, value):
    # 设备名称输入点
    try:
        devicedata = get_MonitorDeviceManage(devicename)
        deviceid = devicedata['id']
        regcode = devicedata['regCode']
        # 连接输入点
        moduledata = get_module_data(deviceid, connectname)
        protocolid = moduledata['protocolId']
        groupdata = get_grouplist(protocolid)
        virtualdeviceid = moduledata['virtualDeviceId']
        td = get_td(virtualdeviceid)
        # 变量名称输入点
        single_data, groupname = get_single_data(groupdata, protocolid, rollname, regcode=regcode)
        print(single_data)
        # wsdata构造
        tdserial = td['data']['tdSerial']
        deviceserial = td['data']['deviceSerial']
        itemid = single_data['id']
        address = single_data['elementAddress']
        # 下发数据
        xiafa(tdserial=tdserial, deviceserial=deviceserial, virtualdeviceid=virtualdeviceid, address=address, itemid=itemid,
              value=value)
    except:
        print('下发失败')



def mission_run(devicename, connectname, minvalue, maxvalue, lis):
    if isinstance(lis,str):
        lis = lis.split(',')
    value = random.randint(minvalue, maxvalue)
    devicedata = get_MonitorDeviceManage(devicename)
    deviceid = devicedata['id']
    regcode = devicedata['regCode']
    # 连接输入点
    moduledata = get_module_data(deviceid, connectname)
    protocolid = moduledata['protocolId']
    groupdata = get_grouplist(protocolid)
    virtualdeviceid = moduledata['virtualDeviceId']
    td = get_td(virtualdeviceid)
    tdserial = td['data']['tdSerial']
    tdtags = td['data']['tdDataTags']
    deviceserial = td['data']['deviceSerial']
    while True:
        for i in lis:
            single_data, groupname = get_single_data(groupdata, protocolid, i, regcode=regcode)
            if groupname == "气电比":
                start_value = get_value(deviceserial, tdserial, tdtags, i)
                valuel = value + int(float(start_value))
                mission_xiafa(devicename, connectname, i, valuel)
                print("%s: %s" % (i, valuel))
            else:
                mission_xiafa(devicename, connectname, i, value)
                print("%s: %s" % (i, value))
        time.sleep(300)


# cookie = get_cookie("gfAdmin", "abcd123456")
# shebei=input("输入设备名称")
# lianjie=input("连接名称")
# nyn=int(input("最小值"))
# max=int(input("最大值"))
# b=[]
# while True:
#     a=input('是否继续输入变量名称')
#     if a:
#         b.append(a)
#     else:
#         break
# mission_run(shebei, lianjie, nyn, max, b)
