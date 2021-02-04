# -*- coding:utf-8 -*-
#  2020/12/11 
#  hardinfomeation.py
#  
# author:gyl

import subprocess
import re
import ipaddress,json,datetime
from subprocess import PIPE
import platform
from time import sleep
from stark.utils.log_ctrl import logger

from django.conf import settings
from tool.raids_h import rehis_h


class Hardinformeation(object):
    def __init__(self, ip):
        self.ip = ip
        self.harddetection = 'harddetection'
        self.host_info = 'host_info'
        self.ip_net = self.ip_network()
    def ip_network(self):
        if '/' not in self.ip:
            return self.ip
        else:
            net = ipaddress.ip_network(self.ip, strict=False)
            # 打印网络号,掩码
            ip =str(net.network_address) + '/' + self.ip.split('/')[1]
            logger.debug(ip)
            return ip
    def find_hosts(self):
        iphosts = []
        sys =platform.system()
        # name = settings.HARDNAME
        name = 'harddetection'

        if '/' not in self.ip:
            iphosts.append(self.ip)
        else:
            net = ipaddress.ip_network(self.ip, strict=False)
            for ip in net.hosts():
                if sys == "Windows":
                    comment = 'ping -n 1 %s' % ip
                    p = subprocess.Popen(comment, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    sleep(1)
                    if p.poll() is None:
                        logger.debug(ip,"is down")
                        pass
                    else:
                        logger.debug(ip, 'is up')
                        iphosts.append(ip)
                elif sys == "Linux":
                    comment = 'ping -c2 %s &> /dev/null' % ip
                    p = subprocess.Popen(comment, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    sleep(2)
                    if p.poll() == 0:
                        logger.debug(ip, "is up" )
                        iphosts.append(ip)
                        # pass
                    else :
                        logger.debug(ip, "is down")

            # logger.debug(name,self.ip_net)
            s = rehis_h.hget(name,self.ip_net)
            v = json.loads(s)
            v['completiontime'] = '共探测到%s主机' % len(iphosts)
            rehis_h.hset(name,self.ip_net,json.dumps(v))
        return iphosts

    def get_cpuinfo(self):
        '''
        CPU(s):                32                #逻辑CPU核数
        Thread(s) per core:    2                 #每核超线程数
        Core(s) per socket:    8                 #每个cpu核数
        Socket(s):             2                 #物理cpu个数
        Model name:            Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz
        CPU MHz:               1200.000          #cpu主频
         {
            '座': 'Socket(s)',
            '型号名称': 'Model name',

        }
        :return:
        '''
        command = 'lscpu'
        cpuinfo_h = self.organize_data(command)
        try:
            cpuinfo_h['Socket(s)'] = cpuinfo_h.pop('座')
            cpuinfo_h['Model name'] = cpuinfo_h.pop('型号名称')
        except Exception as e:
            logger.debug(e)
        cpu_info = {
            'name': cpuinfo_h['Model name'],
            'Core_number': cpuinfo_h['Core(s) per socket'], #核数
            'Core_thread':cpuinfo_h['Thread(s) per core'], #每核线程
            'Number': cpuinfo_h['Socket(s)'], #颗数
            'Frequ': cpuinfo_h['CPU MHz'], #频率
                    }
        return cpu_info

    def get_hostname(self):
        cmmand='hostname'
        hostname = self.organize_data(cmmand,hostname=True)
        logger.debug(hostname)
        return hostname

    def get_host(self):
        '''
        Manufacturer: 品牌
        Product Name: 型号
        Serial Number: 序列号
        :return:
        '''
        command = 'dmidecode|grep "System Information" -A9|egrep  "Manufacturer|Product|Serial"'
        hostname = self.organize_data(command)
        # logger.debug(hostname,str(hostname))
        hostname = {
            'Manufacturer':hostname['Manufacturer'],
            'Product_Name':hostname['Product Name'],
            'Serial_Number':hostname['Serial Number'],
        }
        return hostname

    def get_option_sys_v(self,system=True):
        command = 'cat /etc/redhat-release'
        hostname = self.organize_data(command,system=True)
        return hostname
    def get_ip(self):
        '''
        判断系统
        b'CentOS Linux release 7.3.1611 (Core) \n'
        b'CentOS release 6.3 (Final)\n'
        :return:
        '''
        # command = 'cat /etc/redhat-release'
        # # p = subprocess.Popen(comment, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # # Sysem_Centos = p.stdout.read()
        # # SC_Version = Sysem_Centos.decode()
        # SC_Version = self.organize_data(command,system=True)
        # pattern=r'7\.\d'
        # patern1= r'6\.\d'
        # if re.search(pattern, SC_Version):
        #     command='ip addr | grep inet | egrep -v  "inet6|127.0.0.1"'
        # elif re.search(patern1,SC_Version):
        #     command='ifconfig | grep inet | egrep -v  "inet6|127.0.0.1"'
        command = 'ip addr | grep inet | egrep -v  "inet6|127.0.0.1"'
        ip_h = self.organize_data(command)
        return ip_h

    def get_disk(self):
        pass

    def get_memory(self):
        command = 'dmidecode|grep -A16 "Memory Device"|egrep "logger.debug|Size" | egrep -v "Unknown|No Module Installed|Range"'
        return self.organize_data(command, memary=True)
    def get_data(self,command):
        p = subprocess.Popen(args=command, stdout=PIPE, )
        name, error = p.communicate()
        return name.decode()

    def organize_data(self,command,memary=False,system=False,hostname=False):
        data_h = self.get_data(command)
        if system == True or hostname==True:
            logger.debug(data_h)
            data_h = re.sub('\r','',data_h)
            return data_h
        data_h = re.sub('：', ':', data_h)
        if ':' in data_h:
            ansi_escape = re.compile(r'''
                        \x1B
                        [@-_]
                        [0-?]*
                        [ -/]*
                        [@-~]
                        ''', re.VERBOSE)
            data_h = ansi_escape.sub('',data_h)
            data_h = re.sub('\t\r', '', data_h).split('\n')
            del data_h[0]
            del data_h[-1]
            data_dict={}
            if memary:
                data_dict = {'count': 0}
            for x in data_h:
                if x and ':' in x:
                    x_list=x.split(':')
                    data_dict[x_list[0].strip()] = x_list[1].strip()
                    if memary and "Size" in x:
                        data_dict['count'] = data_dict['count'] + 1
        else:
            data_list=[]
            data_h = re.sub('\t', '', data_h).split('\n')
            logger.debug(data_h)
            del data_h[0]
            del data_h[-1]
            for ip_info in data_h:
                data_dict = {}
                if ip_info and 'inet' in ip_info:
                    ip_add = ip_info.split()[1]

                    if '/' in ip_add:
                        ip = ip_add.split('/')
                        data_dict['IP'] = ip[0]
                        data_dict['NETMASK'] = ip[1]
                        data_list.append(data_dict)
                    else:
                        data_dict['IP'] = ip_add
                        data_dict['NETMASK'] = '32'
                        data_list.append(data_dict)
            return data_list

        return data_dict
    def get_hostinfo(self):
        hostname = self.get_hostname()
        host=self.get_host()
        cpu_info = self.get_cpuinfo()
        memory = self.get_memory()
        ips = self.get_ip()
        harddection_dict = {
            'host': host,
            'cpu_info': cpu_info,
            'memory':memory,
            'ips':ips,
        }
        logger.debug(hostname,harddection_dict)
        return hostname,harddection_dict
    def regist_info(self):
        hostname = self.get_hostname()
        host = self.get_host()
        cpu_info = self.get_cpuinfo()
        memory = self.get_memory()
        ips = self.get_ip()
        name = 'host_info'
        harddection_dict = {
            'host': host,
            'cpu_info': cpu_info,
            'memory': memory,
            'ips': ips,
        }
        logger.debug(hostname)

        rehis_h.hset(name,hostname,json.dumps(harddection_dict))

class Hostregist(Hardinformeation):
    host_regist = []
    def regist_hostinfo(self, ip):
        hosts = self.find_hosts(self.ip)
        for host in hosts:
            self.regist_info(host)

