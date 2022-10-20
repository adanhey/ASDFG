import jsonpath
from ASDFG.huiserver_interface_base import Huiserver_interface

class Interface_list(Huiserver_interface):
    def __init__(self):
        super().__init__()

    def find_from_result(self, result, key, value=None, islist=None):
        if value:
            jsonresult = jsonpath.jsonpath(result, "$..*[?(@.%s=='%s')]" % (key, value))
        else:
            jsonresult = jsonpath.jsonpath(result, '$...%s' % key)
        if islist:
            return jsonresult
        else:
            return jsonresult[0]