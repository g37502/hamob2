# from django.test import TestCase

# Create your tests here.
from django_pandas.io import read_frame
import pandas as pd
s = pd.read_csv('../conf/dataframe.csv')
print(s.columns)
# s.drop('')
# s.to_excel('../conf/dataframe.xlsx')
count_list= ['monitorURLNUM','Monitor']
cloum_list =['MonitorAddress','inserttime']
cloum_list.extend(count_list)
s=s[cloum_list]
s['inserttime']=pd.to_datetime(s['inserttime'])
# s =s.groupby(['MonitorAddress','inserttime']).sum()
# s = s[cloum_list]
s.set_index('inserttime', inplace=True)
s = s.groupby('MonitorAddress',as_index=False)
for name, data in s:
    data.resample('d').sum()
    print(type(data))
    for i in data.values:
        print(i)





