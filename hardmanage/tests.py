from django.test import TestCase

# Create your tests here.

#获取IP地址
# import ipaddress
# ip = '192.168.3.1/29'
# net = ipaddress.ip_interface(ip)
# # print(net._make_netmask(32))
# if '/' not in ip:
#     print(ip)
# else:
#     net = ipaddress.ip_network(ip, strict=False)
#     for x in net.hosts():
#         print(x)

'''
import queue
put_data=[1, 2, 3]
q = queue.Queue(maxsize=12)
for each in put_data:
    q.put(each)
print(q.qsize())
print(q.empty())
print(q.full())
while not q.empty():
    print(q.get())
    q.task_done()
'''
# a = "python"

# b = "java"
# print(a+b)
# import re
# s = 'Size: 2048 MB\nSpeed: 800 MHz\nSize: 2048 MB\n'
#
# s =re.sub('\n', ' ', s)
# print(re.search('Size',s).group())
# a = ''
# if a:
#     print(111)

from types import FunctionType
def test():
    pass
class aaa:
    def test1(self):
        pass
    def test2(self):
        pass
print(type(aaa().test1))
if isinstance(aaa().test1,FunctionType):
    print(True)