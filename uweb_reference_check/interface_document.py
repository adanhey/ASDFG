from ASDFG.interface_ability.for_all_interface import *
import time

t = time.gmtime()
nowtime = time.strftime("%Y-%m-%d %H:%M:%S", t)
nowdate = time.strftime("%Y%m%d")
date = time.strftime("%Y-%m-%d")


class Uweb_reference(Huiserver_interface):
    def product_saveorupdate(self, type, companyId="2cde0a43-cd9c-47e8-b76e-6e2cdf2fda6e", productCode="uweb联通测试",
                             productName="uweb联通测试", status=1, systemCode="CP%s025" % nowdate, createUser="sysadmin",
                             createTime=nowtime,
                             proid="790659899362619392"):
        url = '%s/es/product/saveOrUpdate' % self.host
        save = {
            "systemCode": systemCode,
            "companyId": companyId,
            "productCode": nowtime,
            "productName": nowtime,
            "productModel": "751433232324997120",
            "nickName": "群武的小公司（勿动）",
            "customerId": "755464488561713152",
            "picUrl": "",
        }
        data = {
            "id": proid,
            "createTime": createTime,
            "createUser": createUser,
            "systemCode": systemCode,
            "productCode": "uweb联通测试",
            "productName": "uweb联通测试",
            "modelName": "uweb联通测试",
            "modelCode": "uweb联通测试",
            "productModel": "751433232324997120",
            "productType": "750031334284808192",
            "productTypeName": "三边封制袋机",
            "nickName": "群武的小公司（勿动）",
            "address": "沙县",
            "customerId": "755464488561713152",
            "buyTime": date,
            "installTime": date,
            "checkTime": date,
            "defendEndTime": date,
            "fieldExtensions": "{\"col2\":\"1\"}",
            "uwebDeviceId": "1042841863913406464",
            "picUrl": "[{\"id\":\"790565655872516096\",\"url\":\"0000102074/appeal/16636617955272757.png\",\"name\":\"QQ浏览器截图20220613165958.png\"}]",
            "iotData": {
                "bindIotNum": 0,
                "dataSourceNum": 3,
                "detailList": [
                    {
                        "regCode": "",
                        "sourceName": "第三个数据源"
                    },
                    {
                        "regCode": "",
                        "sourceName": "第二个数据源"
                    },
                    {
                        "regCode": "",
                        "sourceName": "群武的数据源"
                    }
                ],
                "id": "1029801475262840832",
                "status": status
            }
        }
        if type == "save":
            result = self.post_request(url=url, json=save)
        else:
            result = self.post_request(url=url, json=data)
        return result

    def product_delete(self, proid):
        url = '%s/es/product/delete/%s' % (self.host, proid)
        result = self.get_request(url=url)
        return result

    def getDeviceStatusForApp(self):
        pass

    def model_saveorupdate(self, modelCode="uweb联通测试", modelName="uweb联通测试", createTime=nowtime, updateTime=nowtime,
                           createUser="sysadmin", updateUser="sysadmin"):
        url = '%s/es/productModel/saveOrUpdate' % self.host
        data = {
            "id": "790563245556801536",
            "createTime": createTime,
            "updateTime": updateTime,
            "createUser": createUser,
            "updateUser": updateUser,
            "customerCode": "0000102074",
            "companyId": "70048941-e07c-4605-8447-2eea1a800573",
            "sysNo": "XH20221117101711379",
            "modelName": modelName,
            "modelCode": modelCode,
            "productType": "750031334284808192",
            "productTypeName": "三边封制袋机",
            "workVoltage": "750031729438576640",
            "workVoltageName": "220V/50HZ",
            "machinePower": "110",
            "modelDesc": "1234",
            "modelPic": "",
            "used": 1,
            "uwebModelId": "1593065683814400001",
            "uwebSourceName": "",
            "deleted": 0,
            "fieldExtensions": "{\"col2\":[[\"3\"]],\"col1\":\"2022-01\",\"col5\":\"225\",\"col4\":\"\",\"col3\":\"\"}"
        }
        result = self.post_request(url=url, json=data)
        return result

    def model_update_batch(self, modellist):
        # 型号列表页修改
        url = '%s/es/productModel/batchUpdate' % self.host
        data = {
            "productType": "750031334284808192",
            "productTypeName": "三边封制袋机",
            "workVoltage": "750031782576214016",
            "workVoltageName": "380V/50HZ",
            "machinePower": "1",
            "modelDesc": nowtime,
            "ids": modellist,
            "systemField": 1
        }
        result = self.post_request(url=url, json=data)
        return result

    def model_import_Excel(self):
        # 型号列表页导入excel
        file = open("model.xlsx", 'rb')
        url = '%s/es/productModel/importExcel' % self.host
        data = {
            "file": file
        }
        result = self.post_request(url=url, files=data)
        return result

    def product_import_Excel(self):
        # 产品列表页导入excel
        file = open("excel.xlsx", 'rb')
        url = '%s/es/productModel/importExcel' % self.host
        data = {
            "file": file
        }
        result = self.post_request(url=url, files=data)
        return result

    def customer_update(self, cusid):
        # 客户列表编辑
        url = '%s/es/customer/update' % self.host
        phone = str(int(time.time()) * 100)[:11]
        data = {
            "id": cusid,
            "companyId": "70048941-e07c-4605-8447-2eea1a800573",
            "customerCode": "0000102074",
            "fullName": '%schangge' % nowtime,
            "nickName": nowtime,
            "labelList": [
                {
                    "id": "789954044564381696",
                    "createTime": "2022-11-15 17:56:26",
                    "updateTime": "2022-11-15 17:56:26",
                    "createUser": "yangqunwu",
                    "updateUser": "yangqunwu",
                    "customerCode": "0000102074",
                    "companyId": "70048941-e07c-4605-8447-2eea1a800573",
                    "customerId": "755414014491926528",
                    "labelName": "小型客户",
                    "labelId": "746865615250477056"
                },
                {
                    "id": "789954044564381697",
                    "createTime": "2022-11-15 17:56:26",
                    "updateTime": "2022-11-15 17:56:26",
                    "createUser": "yangqunwu",
                    "updateUser": "yangqunwu",
                    "customerCode": "0000102074",
                    "companyId": "70048941-e07c-4605-8447-2eea1a800573",
                    "customerId": "755414014491926528",
                    "labelName": "重点客户",
                    "labelId": "746865491669504000"
                },
                {
                    "id": "789954044564381698",
                    "createTime": "2022-11-15 17:56:26",
                    "updateTime": "2022-11-15 17:56:26",
                    "createUser": "yangqunwu",
                    "updateUser": "yangqunwu",
                    "customerCode": "0000102074",
                    "companyId": "70048941-e07c-4605-8447-2eea1a800573",
                    "customerId": "755414014491926528",
                    "labelName": "普通客户",
                    "labelId": "746865521834938368"
                },
                {
                    "id": "789954044564381699",
                    "createTime": "2022-11-15 17:56:26",
                    "updateTime": "2022-11-15 17:56:26",
                    "createUser": "yangqunwu",
                    "updateUser": "yangqunwu",
                    "customerCode": "0000102074",
                    "companyId": "70048941-e07c-4605-8447-2eea1a800573",
                    "customerId": "755414014491926528",
                    "labelName": "大型客户",
                    "labelId": "746865550452674560"
                }
            ],
            "contactName": "范大海",
            "phone": phone,
            "country": "中国",
            "province": "湖南省",
            "city": "长沙市",
            "area": "天心区",
            "address": "沙县",
            "organization": "群武的二级组织",
            "organizationId": "759149174878351360",
            "employeeId": "1559727011062153218",
            "employeeName": "郑俊鹏",
            "employeePhone": "17688539166",
            "customerManagerId": "755413422017126401",
            "customerManager": "杨群武",
            "customerManagerPhone": "15348612485",
            "remark": "这是备注信息",
            "logoUrl": "[{\"id\":\"789954029200646144\",\"name\":\"龙猫.gif\",\"url\":\"0000102074/customer/16685061608142491.gif\",\"uid\":1668506182845,\"status\":\"success\"}]",
            "fieldExtensions": "{\"col10\":\"[{\\\"id\\\":\\\"789953936867237888\\\",\\\"url\\\":\\\"0000102074/customer/16685061608142491.gif\\\",\\\"name\\\":\\\"龙猫.gif\\\"}]\",\"col3\":\"\",\"col1\":\"11111\",\"col4\":\"21\"}"
        }
        result = self.post_request(url=url, json=data)
        return result

    def get_code(self, codetype):
        url = '%s/es/common/getCode/%s' % (self.host, codetype)
        result = self.get_request(url=url)
        return result.json()['data']

    def customer_save(self):
        url = '%s/es/customer/save' % self.host
        phone = str(int(time.time()) * 10)[:11]
        code = self.get_code("KH")
        data = {
            "id": "",
            "companyId": "",
            "customerCode": "",
            "customerNumber": code,
            "fullName": nowtime,
            "nickName": nowtime,
            "labelList": [
                {
                    "labelId": "746865462582005760",
                    "labelName": "VIP客户"
                }
            ],
            "contactName": nowtime,
            "phone": phone,
            "country": "中国",
            "province": "天津市",
            "city": "市辖区",
            "area": "和平区",
            "address": nowtime,
            "industry": "",
            "organization": "测试环境1",
            "organizationId": "750492929296211968",
            "employeeId": "",
            "employeeName": "",
            "employeePhone": "",
            "customerManagerId": "",
            "customerManager": "",
            "customerManagerPhone": "",
            "remark": "",
            "logoUrl": "",
            "fieldExtensions": "{\"col10\":\"\",\"col9\":\"\",\"col3\":\"\",\"col8\":\"\",\"col7\":\"\",\"col1\":\"101\",\"col5\":\"\",\"col2\":\"\",\"col4\":\"452523wer\"}"
        }
        result = self.post_request(url=url, json=data)
        return result

    def customer_import_excel(self):
        file = open("customer.xlsx", 'rb')
        url = '%s/es/customer/importExcel' % self.host
        data = {
            "file": file
        }
        result = self.post_request(url=url, files=data)
        return result

    def customer_delete(self, cstid):
        url = '%s/es/customer/delete/%s' % (self.host, cstid)
        result = self.get_request(url=url)
        return result

    def employee_save(self):
        url = '%s/es/employee/saveUser' % self.host
        phone = str(int(time.time()) * 10)[:11]
        data = {
            "id": "790629780094754816",
            "fullName": "uwebreference",
            "userName": nowtime.split(" ")[1],
            "password": "abcd123456",
            "password1": "abcd123456",
            "linkPhone": phone,
            "email": "",
            "openService": 1,
            "roleIds": "0b4dbb90-f579-4dca-93a0-e4a37b83167b"
        }
        result = self.post_request(url=url, json=data)
        return result

    def employee_update(self, empid):
        url = '%s/es/employee/update' % self.host
        data = {
            "id": empid,
            "createTime": "2022-11-17 07:00:59",
            "createUser": "sysadmin",
            "updateUser": "sysadmin",
            "customerCode": "0000102074",
            "companyId": "70048941-e07c-4605-8447-2eea1a800573",
            "name": "uwebreference",
            "userName": "",
            "userId": "",
            "jobNumber": "12002312",
            "birthday": "",
            "sex": 1,
            "phone": "",
            "deptId": "755413422017126400",
            "deptName": "测试环境1",
            "deptIds": "_750492929296211968",
            "used": 1,
            "openService": 1,
            "jobKey": "4",
            "jobName": "普通职员",
            "serverOrderNum": 0,
            "assistOrderNum": 0,
            "email": "",
            "supervisor": 0
        }
        result = self.post_request(url=url, json=data)
        return result

    def employee_delete(self,data):
        url = '%s/es/employee/deleteUser' % self.host
        result = self.post_request(url=url, json=data)
        return result

    def role_list(self):
        url = '%s/es/employee/getRoleListByCompanyId' % self.host
        result = self.get_request(url=url)
        return result

    def event_config(self):
        # iot保养提醒
        url = '%s/es/eventPageConfig/getConfig' % self.host
        result = self.get_request(url=url)
        return result

    def warn_batch_status(self):
        url = '%s/es/warn/batchUpdateStatus' % self.host
        data = {
            "eventIds": [
                "6374a65bc26a9b59989dbefa"
            ],
            "ids": [
                "1042483972044554240"
            ],
            "eventType": 2,
            "handleStatus": 2,
            "handleRemark": "123"
        }
        result = self.post_request(url=url, json=data)
        return result

    def get_product(self, name):
        url = '%s/es/product/getPage' % self.host
        data = {
            "productName": name,
            "current": 1,
            "size": 20
        }
        result = self.post_request(url=url, json=data)
        return result

    def get_productmodel(self, name=None, current=1, size=10):
        url = '%s/es/productModel/getPage' % self.host
        data = {
            "modelName": name,
            "current": current,
            "size": size
        }
        result = self.post_request(url=url, json=data)
        return result

    def delete_model(self, modelid):
        url = '%s/es/productModel/delete/%s' % (self.host, modelid)
        result = self.get_request(url=url)
        return result

    def get_customer(self, name=None):
        url = '%s/es/customer/list' % self.host
        data = {
            "customerNumber": "",
            "fullName": name,
            "contactName": "",
            "employeeId": "",
            "customerManagerId": "",
            "organizationIds": [],
            "labelIds": [],
            "current": 1,
            "size": 20
        }
        result = self.post_request(url=url, json=data)
        return result

    def get_emp(self,name="reference"):
        url = '%s/es/employee/list' % self.host
        data = {
            "jobNumber": "",
            "name": name,
            "jobKey": "",
            "deptId": "750492929296211968",
            "current": 1,
            "size": 20
        }
        result = self.post_request(url=url, json=data)
        return result


b = Uweb_reference()
# print(b.product_saveorupdate(type="update").text)
uwebdeviceid = b.product_saveorupdate(type="save").json()['data']['uwebDeviceId']
deviceid = b.get_product(nowtime).json()['data']['records'][0]['id']
print(b.product_delete(deviceid).text)
# print(b.model_saveorupdate().text)
# update_batch model
# modelresult = b.get_productmodel(current=5,size=5).json()
# modelidlist = []
# for i in modelresult['data']['records']:
#     modelidlist.append(i['id'])
# print(b.model_update_batch(modelidlist).text)
# excel导入model
# print(b.model_import_Excel().text)
# modelid = b.get_productmodel("uweb_reference").json()['data']['records'][0]['id']
# print(b.delete_model(modelid).text)
# 客户创建、编辑及删除
# print(b.customer_save().text)
# cus_id = b.get_customer(nowtime).json()['data']['records'][0]['id']
# print(b.customer_update(cus_id).text)
# print(b.customer_delete(cus_id).text)
# excel导入
# print(b.customer_import_excel().text)
# cus_id = b.get_customer("uweb_reference").json()['data']['records'][0]['id']
# print(b.customer_delete(cus_id).text)
# 用户
# print(b.employee_save().text)
# empid = b.get_emp().json()['data']['records'][0]['id']
# data = b.get_emp().json()['data']['records'][0]
# print(b.employee_delete(data).text)
# print(b.employee_update(empid).text)



