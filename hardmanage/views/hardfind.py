# -*- coding:utf-8 -*-
#  2020/12/9 
#  hardfind.py
#  
# author:gyl
from django.shortcuts import render, redirect, HttpResponse
from hardmanage.models import *
from django.db import models
from django.forms import ModelForm
import ipaddress
from tool.raids_h import rehis_h
from stark.utils.config import config_h
from stark.utils.log_ctrl import logger
import datetime, json
import pickle

def ipadd_h(ip):
    if '/' not in ip:
        return ip
    else:
        net = ipaddress.ip_network(ip, strict=False)
        s = str(net.network_address) + '/' + ip.split('/')[1]
        return s


def get_hash(name):
    for item in rehis_h.hscan_iter(name):
        yield item

def hardfind_hamob(request):
    name = 'harddetection'
    if request.method == 'POST':
        ip = request.POST.get("ip_addr")
        ip = ipadd_h(ip)
        try:
            net = ipaddress.ip_interface(ip)
        except Exception as e:
            return render(request, 'hardmanage/ipaddrtest.html', {'e': e})
        date = {'inserttime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'endtime': '', 'explain': ''}
        rehis_h.hset(name, ip, json.dumps(date))
        data = rehis_h.hgetall(name)
        data_dict= {}
        for k,v in data.items():
            data_dict[k]=json.loads(v)
        return render(request, 'hardmanage/ipaddrtest.html', {'data': data_dict})
    return render(request, 'hardmanage/ipaddrtest.html')


def get_data(hostname):
    key = config_h.get_config('Redis_h', 'HARDINFO')
    host_info = json.loads(rehis_h.hget(key, hostname))
    try:
        mem = Memory.objects.get(Size=host_info['memory']['Size'])
    except Exception as e:
        Memory.objects.create(Size=host_info['memory']['Size'])
        mem = Memory.objects.get(Size=host_info['memory']['Size'])
    try:
        Producer =Producer_Name.objects.get(Product_Name=host_info['host']['Product_Name'])
    except Exception as e:
        Producer_Name.objects.create(Product_Name=host_info['host']['Product_Name'])
        Producer = Producer_Name.objects.filter(Product_Name=host_info['host']['Product_Name'])
    try:
        Model_Name =Manufacturer.objects.get(Manufacturer=host_info['host']['Manufacturer'])
    except:
        Manufacturer.objects.create(Manufacturer=host_info['host']['Manufacturer'])
        Model_Name = Manufacturer.objects.get(Manufacturer=host_info['host']['Manufacturer'])

    Core_Number_instance = Count.objects.get(count=host_info['cpu_info']['Core_number'])
    try:
        Frequ_instance = Frequ.objects.get(Frequ=host_info['cpu_info']['Frequ'])
    except Exception as e:
        Frequ_instance = Frequ.objects.create(Frequ=host_info['cpu_info']['Frequ'])
        Frequ_instance = Frequ.objects.get(Frequ=host_info['cpu_info']['Frequ'])
    Core_thread_instance = Count.objects.get(count=host_info['cpu_info']['Core_thread'])
    try:
        CPU_instance = CPU.objects.get(name=host_info['cpu_info']['name'])
    except Exception as e:
        CPU.objects.create(name=host_info['cpu_info']['name'],Core_number=Core_Number_instance,Frequ=Frequ_instance,Core_thread=Core_thread_instance)
        CPU_instance = CPU.objects.get(name=host_info['cpu_info']['name'])
    CPU_NUMber = Count.objects.get(count=host_info['cpu_info']['Number'])
    Memory_NUMber = Count.objects.get(count=host_info['memory']['count'])
    frequ = host_info['memory'].get("Speed",None)
    if frequ:
        try:
            Memory_Frequ =Frequ.objects.get(Frequ=frequ)
        except:
            Frequ.objects.create(Frequ=frequ)
            Memory_Frequ = Frequ.objects.get(Frequ=frequ)
    else:
        Memory_Frequ = Frequ.objects.get(Frequ=0)

    logger.debug(host_info['host']['Serial_Number'])
    logger.debug(hostname, Producer,Model_Name,CPU_instance,CPU_NUMber,mem, Memory_Frequ,Memory_NUMber)
    try:
        host = Host.objects.create(HOSTNAME=hostname,
                                          Serian_Number=host_info['host']['Serial_Number'],
                                          Producer_Name=Producer,
                                          Manufacturer=Model_Name,
                                          CPU=CPU_instance,
                                          CPU_NUMber=CPU_NUMber,
                                          Memory=mem,
                                          Memory_Frequ=Memory_Frequ,
                                          Memory_NUMber=Memory_NUMber,
                                          )
        for ip in host_info['ips']:
            try:
                netmask = Count.objects.get(count=int(ip['NETMASK']))
            except:
                Count.objects.create(count=int(ip['NETMASK']))
                netmask = Count.objects.get(count=int(ip['NETMASK']))
            try:
                a =IP.objects.create(IP=ip['IP'],NETMASK=netmask)
                host.IP.add(a)
            except Exception as e:
                a = IP.objects.get(IP=ip['IP'])
                host.IP.add(a)
                logger.debug(e)
                # return HttpResponse('录入IP有误')
        host.save()
    except Exception as e:
        logger.debug(e)
        return HttpResponse('%s 主机已存在, 或者其它原因无法保存' %hostname)
def hard_save(request,pk):
    get_data(pk)
    key = config_h.get_config('Redis_h', 'HARDINFO')
    rehis_h.hdel(key, pk)
    return redirect('/hardmanage/list/')

def hard_del(request,pk):
    key = config_h.get_config('Redis_h','HARDINFO')
    rehis_h.hdel(key, pk)
    return redirect('/hardmanage/list/')
def hard_multip(request):
    hard_sele = request.POST.get('hard_sele')
    hard_list = request.POST.getlist('hardhost')
    key = config_h.get_config('Redis_h', 'HARDINFO')
    if hard_sele == 'multip_save':
        for hostname in hard_list:
            get_data(hostname)
            rehis_h.hdel(key, hostname)
    elif hard_sele == 'multip_del':
        for hostname in hard_list:
            rehis_h.hdel(key, hostname)
    return redirect('/hardmanage/list/')
def test(request):
    # obj = .Memory.objects.get(pk=3)
    # obj = .Memory.objects.filter(pk=3).first()
    # hosts = obj.memory_host.all()
    # for host in hosts:
    #     logger.debug(host)
    info_list = ['HOSTNAME','Serian_Number']
    obj = Host.objects.filter(pk=1).first()
    # host_info = [obj.HOSTNAME, obj.Serian_Number,obj.ModelName.Manufacturer, obj.Producer.Product_Name, ]
    # cpu_info = [obj.CPU.name , obj.CPU.Core_number.count, obj.CPU.Frequ.Frequ,obj.CPU.Core_number.count,obj.CPU_NUMber.count,obj.CPU.Core_thread.count]
    # memory_info = [obj.Memory.Size,obj.Memory_NUMber.count]
    # ip_info = [{x.IP:x.NETMASK.count} for x in obj.IP.all()]
    # print(ip_info)
    idc_info = obj.host_idc.all()
    # print(idc_info,type(idc_info))
    # for x in idc_info:
    #     print(x.address.city.prov)
    # ret=obj.Memory
    # print(ret)
    # logger.debug(type(obj.IP.all()))
    # for i in obj.IP.all():
    #     logger.debug(i)
    # print(obj.CPU_set.all())
    hostname = Host._meta.get_field('HOSTNAME') #通过字符获取字段
    # print(hostname.verbose_name)
    # print(obj._meta.get_field('CPU_NUMber').verbose_name)
    # print(type(obj._meta.get_field('CPU_NUMber')))
    # print(type(obj.ModelName._meta.fields),type(obj.Memory))
    # print(obj.ModelName._meta.get_field('Manufacturer'))
    # for ver_name in .Host._meta.fields:
    #     print(ver_name, ver_name.verbose_name)
    print(type(obj.CPU),type(obj.CPU_NUMber),type(obj))
    s = obj.CPU
    s1 = s.host_cpu.all()
    print(type(s1))
    return render(request, 'hardmanage/test.html',{'obj':obj})
