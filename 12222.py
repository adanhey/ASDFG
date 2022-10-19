import pytest
class a():
    def __iter__(self):
        self.index = 'asd'
        return self
    def __next__(self):
        self.index = 1
        self.index += 1
        return self.index
    def sad(self,a,b):
        c=a+b
        print(c)
asd = a()
cdd = 'asd'
for i in range(3):
    try:
        assert i==2
    except:
        pass
    cdd = 5
    continue
