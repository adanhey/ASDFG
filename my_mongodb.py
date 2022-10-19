#!/usr/bin/python3

import pymongo

# 定位连接本地mongo服务
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 定位db
mydb = myclient["mydb"]
# 如果db需要信息认证，则需要加如下行
# db.authenticate("account", "password")
# 定位表
mycol = mydb["mytb"]
# 构造数据
mydict = {"what": "what", "num": 100}
# 执行操作（此处为插入数据）
# x = mycol.insert_one(mydict)
mycol.delete_one({"what": {"$regex": "^s"}})

# x = mycol.update_many({"what": "what"}, {"$set": {"num": 10, "new": "n"}})

# print(x.modified_count, "文档已修改")
