# -*- coding:utf-8 -*-
#  2020/12/22 
#  redis_c.py
#  
# author:gyl
from tool.raids_h import rehis_h
import time,json,datetime
from tool.hardifno_sshget import Hardifnfo_ssh
from stark.utils.log_ctrl import logger

def entryflag(ip_net,complete=False):
    data = rehis_h.hget('harddetection', ip_net)
    v = json.loads(data)
    if complete:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        v['endtime']=date
        rehis_h.hset('harddetection', ip_net, json.dumps(v))

def get_hash(name):
    for item in rehis_h.hscan_iter(name):
        yield item
while True:
    time.sleep(3)
    vs = get_hash('harddetection')
    for i in vs:
        k = i[0]
        v = json.loads(i[1])
        if v['endtime']:
            logger.debug(v['endtime'])
        else:
            v['endtime'] = '正在处理'
            port = '22'
            user = 'hamob'
            passwd = 'hamob123!@#'
            try:
                s = rehis_h.hget('harddetection', k)
                s = json.loads(s)
                s['endtime'] = '正在处理'
                rehis_h.hset('harddetection', k, json.dumps(s))
            except:
                logger.debug('数据有误')
                continue
            # s = rehis_h.hget('harddetection', k)
            # s = json.loads(s)
            # s['endtime'] = '正在处理'
            # rehis_h.hset('harddetection', k, json.dumps(s))
            hard = Hardifnfo_ssh(k)
            hard.regist_hostinfo(port,user,passwd)
            hard.sshclose()

