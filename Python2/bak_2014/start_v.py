#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import socket


class CuckooStart(object):
    """分析系统相关服务启动"""

    _terminal_command = 'gnome-terminal -x bash -c '
    _bash_command = ';exce bash'

    def __init__(self, terminal=False):
        self.terminal = terminal

    def get_cmd(self, cmd):
        """配置启动命令"""
        if self.terminal:
            cmd = '%s "%s &%s"' % (self._terminal_command, cmd, self._bash_command)
        else:
            cmd = '%s &' % cmd
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
            sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
            subprocess.call(cmd, shell=True)
            return True
        return False

    def virtualbox_network(self):
        """创建虚拟机网卡"""
        try:
            cmd = "vboxmanage hostonlyif create ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0"
            sys.stderr.write('create virtualbox network\n')
            subprocess.call(cmd, shell=True)
            return True
        except Exception:
            sys.stderr.write('create virtualbox network failed\n')
            return False

    def mongo_server(self):
        """启动mongod服务"""
        cmd = "mongod --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 27017 --logappend &"
        return self.monitor_port(self, 'tcp', 27017, cmd)

    def memcached_server(self):
        """启动监控服务器的资源"""
        cmd = "memcached -d -p 11214 -u root -m 32 &"
        return self.monitor_port('tcp', 11214, cmd)

    def sysmon_server(self):
        """启动sysmon服务"""
        try:
            cmd = "python /var/VenusAnalysis/cuckoo/utils/sysmon.py &"
            sys.stderr.write('run sysmon.py\n')
            subprocess.call(cmd, shell=True)
            return True
        except Exception:
            sys.stderr.write('run sysmon.py failed\n')
            return False

    def cuckoo_server(self):
        """启动cuckoo服务"""
        try:
            cmd = "cd /var/VenusAnalysis/cuckoo/ && python cuckoo.py"
            cmd = self.get_cmd(cmd)
            sys.stderr.write('run cuckoo.py\n')
            subprocess.call(cmd, shell=True)
            return True
        except Exception:
            sys.stderr.write('run cuckoo.py failed\n')
            return False

    def cuckoo_django_server(self):
        """启动cuckoo_web服务"""
        cmd = "cd /var/VenusAnalysis/cuckoo/web/ && python manage.py runserver 0.0.0.0:80"
        cmd = self.get_cmd(cmd)

        return self.monitor_port('tcp', 80, cmd)

    def cuckoo_api_server(self):
        """启动cuckoo_web服务"""
        cmd = "cd /var/VenusAnalysis/cuckoo/utils/ && python api.py --host 0.0.0.0 --port 8081"
        return self.monitor_port('tcp', 8081, cmd)

    def main(self):
        """cuckoo 入口程序"""
        self.virtualbox_network()
        subprocess.call('sleep 1', shell=True)
        if self.mongo_server() and self.memcached_server():
            subprocess.call('sleep 3', shell=True)
            if self.sysmon_server() and self.cuckoo_server():
                subprocess.call('sleep 3', shell=True)
                if self.cuckoo_django_server() and self.cuckoo_api_server():
                    sys.stderr.write('Cuckoo service has been open.\n')

if __name__ == '__main__':
    cs = CuckooStart()
    cs.main(terminal=True)
