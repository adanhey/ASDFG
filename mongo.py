#!/usr/bin/python3
import json
import math
import random
import time
from dateutil import parser
import pymongo


def db_connect(dbname, tabname):
    myclient = pymongo.MongoClient("mongodb://10.44.219.251:27017/")
    mydb = myclient["%s" % dbname]
    mycol = mydb["%s" % tabname]
    mycol.find()
    return mycol


def db_insert(col, data):
    col.insert_one(data)


def timechange(time_str):
    c_time = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(c_time)
    return int(timestamp) * 1000


data = {
    # "_id": {
    #     "$oid": "614addd50d007112653f6262"
    # },
    "deviceId": "24c62db7-2c81-4bac-8abc-b60981d59386",
    "regCode": "7488656886Z00VN88SA000000000",
    "address": "01",
    "mark": "dddd",
    "protocolId": "3b2f19bd-8980-4624-81a7-c85bb009f4d6",
    "originData": "006800650000005537454B315A343649433531554B45380103001E0001000200FB0082000F07D000000000000000000000000000000096000001000C000000640000000A000000000400066700000000000200140031002E0032002F00330023006E006200000000",
    "updateTime": {
        "$date": {
            "$numberLong": "1632362408273"
        }
    },
    "createTime": {
        "$date": {
            "$numberLong": "1632362408273"
        }
    },
    "data": {
        "加卸载状态": "卸载",
        "前轴承温度高预警": "无故障",
        "排气压力传感器故障": "无故障",
        "主机排气压力高停机": "无故障",
        "油分压差开关报警": "无故障",
        "主机温度高预警": "无故障",
        "测试枚举": "测试2",
        "机头齿轮保养时间到": "无故障",
        "累计运行时间": "10",
        "主机过载": "无故障",
        "主机频率": "15.0",
        "排气温度传感器故障": "无故障",
        "机头轴承保养时间到": "无故障",
        "主机排气压力高预警": "无故障",
        "排气压力高停机": "无故障",
        "排气温度高停机": "无故障",
        "一级排气温度传感器故障": "无故障",
        "主机温度": "20.00",
        "测试32位有符号整数": "100",
        "测试字符串": "1.2/3#nb",
        "供气温度高停机": "无故障",
        "主机排气压力": "25.1",
        "供气温度高预警": "预警",
        "主机风叶保养时间到": "保养提醒",
        "润滑油运行时间": "0",
        "润滑脂运行时间": "0",
        "前轴承温度传感器故障": "无故障",
        "空滤压差开关报警": "无故障",
        "前轴承温度高停机": "无故障",
        "最小压力阀保养时间到": "无故障",
        "空气过滤器使用时间": "0",
        "润滑脂保养时间到": "保养提醒",
        "油气分离器运行时间": "0",
        "供气压力": "13.0",
        "相序错误": "无故障",
        "一级排气温度高停机": "故障",
        "风机过载": "无故障",
        "油滤压差开关报警": "无故障",
        "电机轴承保养时间到": "无故障",
        "供气压力高预警": "无故障",
        "前轴承温度": "0",
        "风机频率": "0.00",
        "高压柜故障": "无故障",
        "喷油温度高预警": "无故障",
        "级间压力传感器故障": "无故障",
        "安全阀保养时间到": "无故障",
        "油过滤器使用时间": "0",
        "供气温度传感器故障": "无故障",
        "润滑油保养时间到": "无故障",
        "累计加载时间": "0",
        "供气温度": "15",
        "主机电流": "0",
        "运行状态": "1-故障停机",
        "油过滤器保养时间到": "保养提醒",
        "主机排气压力传感器故障": "无故障",
        "喷油压力传感器故障": "无故障",
        "排气管保养时间到": "无故障",
        "油气分离器保养时间到": "无故障",
        "预警": "无",
        "空久停机": "无",
        "故障": "无",
        "主机绝缘保养时间到": "无故障"
    },
    "buzId": "1632296405719",
    "_class": "cn.inovance.ems.job.domain.HistoryTdRunDataMongo"
}


def insert_creation_data(col, deviceId, regCode, protocolId, times, startstamp, ags):
    data['deviceId'] = deviceId
    data['regCode'] = regCode
    data['protocolId'] = protocolId
    for i in ags:
        if i['name'] in data['data']:
            data['data'][i['name']] = str(i['startnum'])
    db_insert(col, data)
    for j in range(times):
        del(data['_id'])
        data['updateTime']['$date']['$numberLong'] = str(startstamp)
        data['createTime']['$date']['$numberLong'] = str(startstamp)
        for i in ags:
            rad = random.randint(0, i['randint'])
            if i['name'] in data['data']:
                data['data'][i['name']] = str(int(data['data'][i['name']]) + rad)
        startstamp += 300000
        print(data)
        col.insert_one(data)
        print(startstamp)
        time.sleep(1)


col = db_connect("ems", "HistoryTdRunData")
# deviceid = input("输入deviceid：")
deviceid = '24c62db7-2c81-4bac-8abc-b60981d59386'
# regCode = input("输入regCode：")
regCode = '7488656886Z00VN88SA000000000'
# protocolId = input("输入protocolId：")
protocolId = '3b2f19bd-8980-4624-81a7-c85bb009f4d6'
# startdate = input("输入开始时间（格式YYYY-mm-dd HH:MM:SS)")
startdate = '2021-02-01 12:00:00'
# enddate = input("输入结束时间（格式YYYY-mm-dd HH:MM:SS)")
enddate = '2021-02-20 12:00:00'
ti = 1
startstamp = timechange(startdate)
endstamp = timechange(enddate)
times = math.ceil((endstamp - startstamp) / 300000)
ags = []
while True:
    a = {}
    a['name'] = input("输入第%s个需要的递增的变量：" % ti)
    if not a['name']:
        break
    a['startnum'] = input("输入第%s个递增的开始值：" % ti)
    a['randint'] = int(input("输入第%s个递增的步长：" % ti))
    ti += 1
    ags.append(a)

insert_creation_data(col, deviceid, regCode, protocolId, times, startstamp,ags)
