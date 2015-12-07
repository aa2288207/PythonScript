#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import socket


def monitor_port(protocol, port, cmd):
    address = ('127.0.0.1', port)
    socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
    client = socket.socket(socket.AF_INET, socket_type)

    try:
        client.bind(address)
    except Exception, e:
        client.close()
        return True
    else:
        client.close()
        sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
        subprocess.call(cmd, shell=True)
        return True
    
    return False


def virtualbox_network():
    try:
        cmd = "vboxmanage hostonlyif create ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0"
        sys.stderr.write('create virtualbox network\n')
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        sys.stderr.write('create virtualbox network failed\n')
        return False
    

def mongo_server():
    cmd = "mongod --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 27017 --logappend &"
    return monitor_port('tcp', 27017, cmd)


def memcached_server():
    cmd = "memcached -d -p 11214 -u root -m 32 &"
    return monitor_port('tcp', 11214, cmd)


def sysmon_server():
    try:
        cmd = "python /var/VenusAnalysis/cuckoo/utils/sysmon.py &"
        sys.stderr.write('run sysmon.py\n')
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        sys.stderr.write('run sysmon.py failed\n')
        return False


def cuckoo_server():
    try:
        cmd = "cd /var/VenusAnalysis/cuckoo/ && python cuckoo.py &"
        sys.stderr.write('run cuckoo.py\n')
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        sys.stderr.write('run cuckoo.py failed\n')
        return False


def cuckoo_django_server():
    cmd = "cd /var/VenusAnalysis/cuckoo/web/ && python manage.py runserver 0.0.0.0:80 &"
    return monitor_port('tcp', 80, cmd)


def cuckoo_api_server():
    cmd = "cd /var/VenusAnalysis/cuckoo/utils/ && python api.py --host 0.0.0.0 --port 8081 &"
    return monitor_port('tcp', 8081, cmd)


def main():
    virtualbox_network()
    subprocess.call('sleep 1', shell=True)
    if mongo_server() and memcached_server():
        subprocess.call('sleep 3', shell=True)
        if sysmon_server() and cuckoo_server():
            subprocess.call('sleep 30', shell=True)
            if cuckoo_django_server() and cuckoo_api_server():
                sys.stderr.write('Cuckoo service has been open.\n')


if __name__ == '__main__':
    main()
