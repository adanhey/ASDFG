# coding = utf-8
import pandas

df = pandas.read_excel('rowman.xlsx',sheet_name='interfaceinfo')
data = df.values
# print(data[0])
for line in data:
    c = str(line)
    c = c.replace('[','')
    c = c.replace(']','')
    c = c.replace("'","")
    linelist = c.split(' ')
    print(linelist)
        # with open('12222.py','w') as sd:
        #     sd.write(st.range('A%i' % row).value)
        #     sd.close()

