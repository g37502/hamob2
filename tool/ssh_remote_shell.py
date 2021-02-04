# -*- coding:utf-8 -*-
#  2020/12/17 
#  ssh_remote_shell.py
#  
# author:gyl
from stark.utils.log_ctrl import logger

import paramiko,time
class Ssh_Conn(object):
    def __init__(self,ip,port,user,passwd):
        self.user = user
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
        self.ssh.connect(ip,port,user,passwd)
    def ssh_command(self,command):
        stdin,stdout,stderr = self.ssh.exec_command(command)    #这三个得到的都是类文件对象
        outmsg,errmsg = stdout.read(),stderr.read()    #读一次之后，stdout和stderr里就没有内容了，所以一定要用变量把它们带的信息给保存下来，否则read一次之后就没有了
        if errmsg == "":
            return outmsg.decode()
        return errmsg.decode()
    def su_root(self,root_pwd,command):
        channl = self.ssh.invoke_shell()
        time.sleep(0.1)
        if self.user != 'root':
            #先判断提示符，然后下一步在开始发送命令，这样大部分机器就都不会出现问题
            buff = ''
            while not buff.endswith('$ '):
                resp = channl.recv(9999)
                logger.debug(999)
                buff += resp.decode('utf8')
                time.sleep(0.1)
            # print('获取登录后的提示符：%s' %buff)
            channl.send(' export LANG=en_US.UTF-8 \n') #解决错误的关键，编码问题
            channl.send('export LANGUAGE=en \n')
            channl.send('su - \n')
            buff = ""
            while not buff.endswith('Password: '): #true
                resp = channl.recv(9999)
                buff +=resp.decode('utf8')
            channl.send(root_pwd)
            channl.send('\n')
            buff = ""
            while not buff.endswith('# '):
                resp = channl.recv(9999)
                buff +=resp.decode('utf8')
        channl.send(command) #放入要执行的命令
        channl.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = channl.recv(9999).decode()
            buff +=resp
        result  = buff
        # print(type(buff))
        return result
    def ssh_close(self):
        self.ssh.close()

def main():
    # ip = '112.13.92.133'
    ip ='192.168.3.19'
    port='22'
    user = 'hamob'
    passwd='hamob123!@#'
    # command = 'dmidecode'
    # command = 'dmidecode|grep "System Information" -A9|egrep  "Manufacturer|Product|Serial"'
    command = 'hostname'
    ssh = Ssh_Conn(ip,port,user,passwd)
    root_passwd='vcluster'
    s = ssh.su_root(root_passwd, command)
    print(s)
    ssh.ssh_close()

if __name__ == '__main__':
    main()

