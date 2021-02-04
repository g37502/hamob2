# -*- coding:utf-8 -*-
#  2020/12/23 
#  hard_tmp.py
#  
# author:gyl
from django.template import Library
register = Library()

from tool.raids_h import rehis_h
from django.conf import settings
import json
from stark.utils.pagination import Pagination
@register.inclusion_tag('hardmanage/iphandle.html')
def iphandle_tmp():
    ipchadleall = rehis_h.hgetall(settings.HARDNAME)
    for k,v in ipchadleall.items():
        v = json.loads(v)
        ipchadleall[k] = v
    return {'ipchadleall':ipchadleall}

@register.inclusion_tag('hardmanage/waithard.html')
def hardwait_tmp():
    s ={}
    hardinfoall = rehis_h.hgetall(settings.HARDINFO)
    for k,v in hardinfoall.items():
        hardinfoall[k]=json.loads(v)
        v=json.loads(v)
        v1={}
        v1['host'] = v['host']['Product_Name']
        v1['cpu_info'] = v['cpu_info']['name'] + '* ' + v['cpu_info']['Number']
        v1['memory'] = v["memory"]["Size"] +"*" + str(v["memory"]["count"])
        ips=""
        for ip in  v["ips"]:
            i = ip['IP']+'/'+ip["NETMASK"] +'\n'
            ips = ips + i
        v1['ips']= ips
        s[k]=v1
    return {'hardinfoall':s}

