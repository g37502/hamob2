#!/usr/bin/env python
#-*- coding:utf-8 -*-
#config.py
#配置文件方法
#author gggg


import  os
import sys
import configparser

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)


from stark.utils.log_ctrl import logger



class Adminconfig:
    '''配置文件方法'''
    def __init__(self,config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'conf'),config_name = 'config.ini'):
        '''加载配置文件'''
        self.config_path = config_path
        print(config_path,2222)
        self.config_name = config_name
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    def reade_config(self):
        self.config.read(os.path.join(self.config_path,self.config_name))
        print(os.path.join(self.config_path,self.config_name))
    def write_config(self):
        '''写入配置文件'''
        ret = {'status':0, 'statusText':'save'}
        try:
            with open(os.path.join(self.config_path,self.config_name), 'w') as f: 
                self.config.write(f)
        except Exception as e:
            ret['status'] = 1
            ret['statusText'] = e
            logger.warning(f'没有保存成功，{ret}')
        return ret
    def get_config(self, section, option):
        '''读取配置'''
        value = self.config.get(section,option)
        return value
    def get_int(self,section,option):
        return self.config.getint(section,option)
    def get_blool(self,section,option):
        return self.config.getboolean(section,option)
    def add_config(self, section, option, value):
        if self.config.has_section(section):
            self.config.set(section, option, value) 
        else:
            self.config.add_section(section)
            self.config.set(section, option, value)
    def check_config(self):
        pass


# def main():
#     dir_path = 'C:\\Users\\gaoya\\Desktop\\py2018\\02-auto\\log_study\\51memov035'
#     config_path = os.path.join(dir_path,'conf')
#     config_name = 'test.ini'
#     config = Adminconfig()
#     # config.add_config('Home','ip','10.10.10.10')
#     # config.write_config()
#     # ip = config.get_config('Home','ip')
#     # # print(ip)
#     config.reade_config()
#     ip = config.get_config('Home','ip')
#     print(ip)
#     # # print(config.get_config('ddd','passwd_filename'))
#
# if __name__ == '__main__':
#     main()


# print(os.path.abspath(__file__))
dir_path = r'C:/Users/gaoya/Desktop/python2020/CRM/s1016/'
config_path = os.path.join(dir_path,'conf')

config_name = 'config.ini'
config_h = Adminconfig(config_path=config_path)
config_h.reade_config()

