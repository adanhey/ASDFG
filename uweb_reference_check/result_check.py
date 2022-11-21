from interface_document import *
class Result_check(Uweb_reference):
    def code_check(self,result):
        assert result.statuscode == 200
    def word_type(self,result,typedict):
        for i,y in result.json().items:
            for a,b in typedict.item():
                if a == i:
                    assert j == y