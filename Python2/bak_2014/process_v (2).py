#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*/1 * * * * python /xxx/monitor.py >> /xxx/logs/monitor.log 2>&1  &

import os
import sys
import subprocess
import os.path as op
import socket

def this_abs_path(script_name):
    return op.abspath(op.join(op.dirname(__file__), script_name))


def monitor_process(key_word, cmd):
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)

    lines = p3.stdout.readlines()
    if len(lines) > 0:
        return

    sys.stderr.write('process[%s] is lost, run [%s]\n' % (key_word, cmd))
    subprocess.call(cmd, shell=True)


def monitor_port(protocol, port, cmd):
    address = ('127.0.0.1', port)
    socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
    client = socket.socket(socket.AF_INET, socket_type)

    try:
        client.bind(address)
    except Exception, e:
        return True
    else:
        sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
        subprocess.call(cmd, shell=True)
        return True
    finally:
        client.close()
    
    return False


#=============================================================================
def yuanzhaopin():
    cmd = '%s start' % this_abs_path('gun.sh')
    #monitor_process('\[yuanzhaopin\]', cmd)
    monitor_port('tcp', 8635, cmd)

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
    cmd = "mongod --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 26017 --logappend --auth &"
    # cmd = "mongod --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --directoryperdb --journal &"
    # cmd = "mongod --dbpath=/var/lib/mongodb > /tmp/mongod.log &"
    return monitor_port('tcp', 27017, cmd)


def memcached_server():
    cmd = "memcached -d -p 11214 -u root -m 32"
    return monitor_port('tcp', 11214, cmd)


def sysmon_server():
    try:
        cmd = "python /var/VenusAnalysis/cuckoo/utils/sysmon.py"
        sys.stderr.write('run sysmon.py\n')
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        sys.stderr.write('run sysmon.py failed\n')
        return False


def cuckoo_server():
    try:
        cmd = "python /var/VenusAnalysis/cuckoo/cuckoo.py &"
        sys.stderr.write('run cuckoo.py\n')
        subprocess.call(cmd, shell=True)
        return True
    except Exception, e:
        sys.stderr.write('run cuckoo.py failed\n')
        return False


def cuckoo_django_server():
    cmd = "cd /var/VenusAnalysis/cuckoo/web/ && python manage.py runserver 0.0.0.0:80"
    return monitor_port('tcp', 80, cmd)


def cuckoo_api_server():
    cmd = "cd /var/VenusAnalysis/cuckoo/utils/ && python api.py --host 0.0.0.0 --port 8081"
    return monitor_port('tcp', 8081, cmd)

def main():
    virtualbox_network()
    subprocess.call('sleep 5', shell=True)
    if mongo_server() and memcached_server():
        subprocess.call('sleep 50', shell=True)
        if sysmon_server() and cuckoo_server():
            subprocess.call('sleep 5', shell=True)
            if cuckoo_django_server() and cuckoo_api_server():
                sys.stderr.write('Cuckoo service has been open.\n')


if __name__ == '__main__':
    if mongo_server():
        print '--------xxxxxxxxxxx'
    # main()
