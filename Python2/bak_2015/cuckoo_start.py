#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import subprocess
import socket

from ftp.lsof_kill import ShellAuxiliary
from ftp.ftp_auto_submit import FtpManager

def log():
    log_path = os.path.join('/var/VenusAnalysis/cuckoo', 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logging.basicConfig(filename=os.path.join(log_path, 'cuckoo_start.log'), level=logging.DEBUG)

def check_run_env():
    shell = ShellAuxiliary(port=2042)
    logging.info('check run env ....')
    try:
        shell.start()
    except:
        logging.info('close result_server port 2042 excetion !!!')
    shell.delete_file('/var/lib/mogodb/mongo.lock')


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


def cuckoo_static_log(desc, context):
    logging.info('%s %s[消息:%s]' % (get_current_time(), desc, context))


class CuckooStart(object):
    """分析系统相关服务启动"""

    _terminal_command = 'gnome-terminal -x bash -c'
    _bash_command = ';exce bash'
    _nohup_command = 'nohup'

    def get_cmd(self, cmd, folder='', flag=0, hidden='&'):
        """配置启动命令"""
        # 指定目录后台运行 1
        # 指定目录独立窗口显示 2
        if flag == 1:
            cmd = '%s && sudo %s %s > /tmp/cuckoo_nohup.out 2>&1 %s' % (folder, self._nohup_command, cmd, hidden)
        elif flag == 2:
            cmd = '%s "%s && sudo %s%s"' % (self._terminal_command, folder, cmd, self._bash_command)

        return cmd

    def monitor_port(self, protocol, port, cmd):
        """监听服务端口,端口未占用则启动服务"""
        address = ('127.0.0.1', port)
        socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
        client = socket.socket(socket.AF_INET, socket_type)

        try:
            client.bind(address)
        except Exception:
            client.close()
            return True
        else:
            client.close()
            logging.info('%s port[%s-%s] is lost, run [%s]' % (get_current_time(), protocol, port, cmd))
            subprocess.Popen(cmd, shell=True)
            return True
        return False

    def virtualbox_hostonlyif(self):
        """删除虚拟机无效的hostonlyif"""
        cmd = "sudo vboxmanage hostonlyif remove vboxnet0"
        subprocess.call(cmd, shell=True)
        cuckoo_static_log('删除无效虚拟网卡', cmd)

    def virtualbox_network(self):
        """创建虚拟机网卡"""
        self.virtualbox_hostonlyif()
        try:
            cmd = "sudo vboxmanage hostonlyif create ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0"
            subprocess.call(cmd, shell=True)
            cuckoo_static_log('创建虚拟网卡', cmd)
            return True
        except Exception, e:
            cuckoo_static_log('创建虚拟网卡异常', e)
            return False

    def mongo_server(self):
        """启动mongod服务"""
        cmd = "sudo mongod --fork --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 27017 --logappend &"
        cuckoo_static_log('启动Mongodb服务', cmd)
        return self.monitor_port('tcp', 27017, cmd)

    def memcached_server(self):
        """启动监控服务器的资源"""
        cmd = "sudo memcached -d -p 11214 -u root -m 32 &"
        cuckoo_static_log('启动资源服务器资源监控', cmd)
        return self.monitor_port('tcp', 11214, cmd)

    def sysmon_server(self):
        """启动sysmon服务"""
        try:
            cmd = "sudo python /var/VenusAnalysis/cuckoo/utils/sysmon.py &"
            cuckoo_static_log('启动sysmon服务', cmd)
            subprocess.call(cmd, shell=True)
            return True
        except Exception, e:
            cuckoo_static_log('启动sysmon服务异常', e)
            return False

    def cuckoo_server(self):
        """启动cuckoo服务"""
        flag = 2
        folder = 'cd /var/VenusAnalysis/cuckoo/'
        cmd = 'python cuckoo.py'
        try:
            cmd = self.get_cmd(folder=folder, cmd=cmd, flag=flag)
            cuckoo_static_log('启动cuckoo服务', cmd)
            subprocess.Popen(cmd, shell=True)
            return True
        except Exception, e:
            cuckoo_static_log('启动cuckoo服务异常', e)
            return False

    def cuckoo_django_server(self):
        """启动cuckoo_web服务"""
        flag = 2
        folder = 'cd /var/VenusAnalysis/cuckoo/web/'
        cmd = 'python manage.py runserver 0.0.0.0:80'
        try:
            cmd = self.get_cmd(folder=folder, cmd=cmd, flag=flag)
            cuckoo_static_log('启动cuckoo_django服务', cmd)
            return self.monitor_port('tcp', 80, cmd)
        except Exception, e:
            cuckoo_static_log('启动cuckoo_django服务异常', e)
            return False

    def cuckoo_api_server(self):
        """启动cuckoo_api服务"""
        flag = 1
        folder = 'cd /var/VenusAnalysis/cuckoo/utils/'
        cmd = 'python api.py --host 0.0.0.0 --port 8081'
        try:
            cmd = self.get_cmd(folder=folder, cmd=cmd, flag=flag)
            cuckoo_static_log('启动cuckoo_api服务', cmd)
            return self.monitor_port('tcp', 8081, cmd)
        except Exception, e:
            cuckoo_static_log('启动cuckoo_api服务异常', e)
            return False

    def cuckoo_monitor_server(self):
        """启动cuckoo监控服务"""
        flag = 1
        folder = 'cd /var/VenusAnalysis/cuckoo/'
        cmd = 'python cuckoo_monitor.py'
        try:
            cmd = self.get_cmd(folder=folder, cmd=cmd, flag=flag)
            subprocess.Popen(cmd, shell=True)
            cuckoo_static_log('启动cuckoo监控服务', cmd)
            return True
        except Exception, e:
            cuckoo_static_log('启动cuckoo监控服务异常', e)
            return False

    def main(self):
        """cuckoo 入口程序"""
        self.mongo_server()
        subprocess.call('sleep 2', shell=True)
        self.virtualbox_network()
        self.memcached_server()
        self.sysmon_server()
        self.cuckoo_server()
        self.cuckoo_api_server()
        self.cuckoo_django_server()
        subprocess.call('sleep 2', shell=True)
        self.cuckoo_monitor_server()
        cuckoo_static_log('Cuckoo service has been open.', 'over')

if __name__ == '__main__':

    subprocess.call('sleep 12', shell=True)
    log()
    logging.info('%s cuckoo_start 启动服务开始....' % get_current_time())
    check_run_env()
    subprocess.call('sleep 5', shell=True)
    try:
        cs = CuckooStart()
        cs.main()
    except Exception, e:
        logging.error('cuckoo_start error: %s' % e)
    finally:
        logging.info('%s cuckoo_start 启动服务结束....' % get_current_time())
    ftp = FtpManager()
    ftp.start()

    subprocess.call('sleep 16', shell=True)
