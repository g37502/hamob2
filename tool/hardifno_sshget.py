# -*- coding:utf-8 -*-
#  2020/12/18 
#  hardifno_sshget.py
#  
# author:gyl
import re,subprocess
from subprocess import PIPE
import datetime,json
from tool.hardinfomeation import Hostregist
from tool.ssh_remote_shell import Ssh_Conn
from tool.raids_h import rehis_h
from stark.utils.log_ctrl import logger

class Hardifnfo_ssh(Hostregist):
    def sshconn(self,ip,port,user,passwd):
        self.ssh = Ssh_Conn(ip, port, user, passwd)
    def get_data(self,command):
        root_passwd = 'vcluster'
        s = self.ssh.su_root(root_passwd, command)
        return s
    def sshclose(self):
        try:
            self.ssh.ssh_close()
        except Exception as e:
            logger.debug(e)
    def get_hostname(self,hostname=True):
        cmmand = 'hostname'
        hostname = self.organize_data(cmmand, hostname=True)
        hostname = hostname.split('\n')[1]
        logger.debug(hostname)
        return hostname
    def regist_hostinfo(self,port,user,passwd):
        hosts = self.find_hosts()
        i = 0
        y = 0
        for host in hosts:
            logger.debug(111,host)
            try:
                self.sshconn(str(host),port,user,passwd)
                logger.debug(222)
                self.regist_info()
                self.sshclose()
                i+=1
            except Exception as e:
                logger.debug(e, r'\n', host,'不能连接')
                y+=1
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        v = rehis_h.hget(self.harddetection, str(self.ip_net))
        v = json.loads(v)
        v['endtime'] = date
        v["completiontime"] = v["completiontime"] + "登录成功%s台，登录失败%s台" % (i, y)
        # logger.debug(self.ip.split('/'][1])
        rehis_h.hset(self.harddetection,self.ip_net,json.dumps(v))
def main():
    hard = Hardifnfo_ssh('192.168.3.40/30')
    port = 22
    user = 'hamob'
    passwd = 'hamob123!@#'
    hard.regist_hostinfo(port,user,passwd)
    hard.sshclose()
if __name__ == "__main__":
    main()