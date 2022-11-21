import os
import sys

import allure
import pytest

from ASDFG.uweb_reference_check.interface_document import *


class TestClass:
    def test_one(self):
        with allure.step("test"):
            result = b.product_saveorupdate(type="update")
            print(result.text)

    def test_two(self):
        uwebdeviceid = b.product_saveorupdate(type="save").json()['data']['uwebDeviceId']
        deviceid = b.get_product(nowtime).json()['data']['records'][0]['id']
        result = b.product_delete(deviceid)
        print(result.text)

    def test_three(self):
        result = b.model_saveorupdate()
        print(result.text)

    def test_four(self):
        modelresult = b.get_productmodel(current=5, size=5).json()
        modelidlist = []
        for i in modelresult['data']['records']:
            modelidlist.append(i['id'])
        result = b.model_update_batch(modelidlist)
        print(result.text)

    def test_five(self):
        # excel导入model
        importresult = b.model_import_Excel()
        modelid = b.get_productmodel("uweb_reference").json()['data']['records'][0]['id']
        result = b.delete_model(modelid)
        print(result.text)

    def test_six(self):
        result = b.customer_save()
        cus_id = b.get_customer(nowtime).json()['data']['records'][0]['id']
        updateresult = b.customer_update(cus_id)
        delete_result = b.customer_delete(cus_id)
        print(result.text, updateresult.text, delete_result.text)

    def test_seven(self):
        print(b.customer_import_excel().text)
        cus_id = b.get_customer("uweb_reference").json()['data']['records'][0]['id']
        print(b.customer_delete(cus_id).text)

    def test_eight(self):
        print(b.employee_save().text)
        empid = b.get_emp().json()['data']['records'][0]['id']
        data = b.get_emp().json()['data']['records'][0]
        print(b.employee_delete(data).text)
        print(b.employee_update(empid).text)

    def test_nine(self):
        print(b.role_list().text)
        print(b.event_config().text)
        print(b.warn_batch_status().text)


if __name__ == '__main__':
    pytest.main(['--alluredir', 'report/result', 'all_case.py'])
    split = 'allure' + 'generate' + '.report/result' + '-o' + '.report/html' + '--clean'
    os.system(split)
    # pytest.main("-v -s")
