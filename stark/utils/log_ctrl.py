#!/usr/bin/env python
# -*- coding:utf-8 -*-
#log_ctrl.py
#log的工程应用
#author: De8uG

import logging
import os
import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
工程使用需求：
1-不同日志名称
2-同时打印在控制台，文件
3-灵活控制等级
"""


# def memo_log(logger_name='MEMO-LOG', log_file=os.path.join(BASE_DIR, 'log', 'hamob.log'), level = logging.INFO):
def memo_log(logger_name, level = logging.INFO):
    #创建logger对象
    logger = logging.getLogger(logger_name)
    logger.setLevel(level) #添加等级

    #创建控制台 console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    #创建文件 handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')

    #创建formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

    #添加formtter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    #ch fh 添加到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def main():
    #测试
    logger = memo_log()
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

# if __name__ == '__main__':
#     main()
dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# dir_path = 'C:/Users/gaoya/Desktop/python2020/CRM/s1016/'
log_file = os.path.join(dir_path,'log','hamob.log')
logger = memo_log(logger_name='hamob-log',level = logging.DEBUG)
