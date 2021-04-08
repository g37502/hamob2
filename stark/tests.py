from django.test import TestCase

# Create your tests here.
# import re
# s = 'http://127.0.0.1:8000/stark/business_presen/count_data/list/?&kssj=2021-01-21%2014:56:18'
#
# reg =r'^&jssj=[1-9]\d{3}-\d{1}-\d{1}\s(%20[0-2]\d):[0-5]\d:[0-5]\d$'
# reg1 = r'&jssj=[1-9]\d{3}-\d{2}-\d{2}%20\d{2}:\d{2}:\d{2}'
# reg2 = r'&kssj=[1-9]\d{3}-\d{2}-\d{2}(\+|\%\d{2})\d{2}:\d{2}:\d{2}'
# reg3 = r'\+'
# # matchobj = re.sub(reg1, '',s)
# matchobj = re.search(reg2, s)
# print(matchobj)
kssj = '2020-02-05 13:45:41'
jssj = '2021-01-21 11:02:58'
import datetime
dd = '2019-03-17 11:00:00'
dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
# print(dd,type(dd))

# 时间格式转str:
dc = dd.strftime("%Y-%m-%d %H:%M:%S")
# print(dc,type(dc))
import base64
s='http://www.hamob.com'
bm=base64.b64encode(s.encode('utf-8'))
print(bm)
# bm = str(bm,encoding='utf-8')
# s=str(bm,encoding='utf-8')
# print(s)
aa=base64.b64decode(bm).decode('utf-8')
print(aa)

