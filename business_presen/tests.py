# from django.test import TestCase

# Create your tests here.
from django_pandas.io import read_frame
# import pandas as pd
# s = pd.read_csv('b2.csv')
# print(s.columns)
# s.drop('')
# # s['time']=pd.to_datetime(s['inserttime'], format='%Y-%m-%d')
# s =s.groupby(['MonitorAddress','time']).sum()
# print(s)
# def plastic(x,):
#     x1 = list(str(x))
#     for i in range(len(str(x))):
#         if i == 0:
#             continue
#         x1[i] = '0'
#     a = ''.join(x1)
#     return int(a)
# a = 22.2
# print(plastic(a))
import datetime
print(datetime.datetime.now()+datetime.timedelta(mo=-30))