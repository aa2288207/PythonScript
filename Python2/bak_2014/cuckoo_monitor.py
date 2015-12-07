#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*/1 * * * * python /xxx/monitor.py >> /xxx/logs/monitor.log 2>&1  &

import sys
import time
import subprocess
import socket


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
    except Exception:
        client.close()
    else:
        client.close()
        sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
        subprocess.call(cmd, shell=True)


def monitor_mongodb():
    cmd = 'sudo mongod --fork --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 27017 --logappend &'
    monitor_port('tcp', 27017, cmd)


def monitor_vboxnet():
    cmd = "sudo vboxmanage hostonlyif create ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0"
    monitor_port('tcp', 2042, cmd)


def monitor_memcached():
    cmd = "sudo memcached -d -p 11214 -u root -m 32 &"
    monitor_port('tcp', 11214, cmd)


def monitor_sysmon():
    cmd = "cd /var/VenusAnalysis/cuckoo/utils/ && sudo python sysmon.py &"
    monitor_process('sysmon.py', cmd)


def monitor_cuckoo_api():
    cmd = "cd /var/VenusAnalysis/cuckoo/utils/ && python api.py --host 0.0.0.0 --port 8081 &"
    monitor_port('tcp', 8081, cmd)


def monitor_cuckoo_django():
    cmd = 'cd /var/VenusAnalysis/cuckoo/web/ && python manage.py runserver 0.0.0.0:80 &'
    monitor_port('tcp', 80, cmd)


def monitor_cuckoo_server():
    cmd = "cd /var/VenusAnalysis/cuckoo/ && python cuckoo.py &"
    monitor_process('cuckoo', cmd)


def main(sleep_time=30):
    while True:
        time.sleep(sleep_time)
        monitor_mongodb()
        monitor_vboxnet()
        monitor_memcached()
        monitor_cuckoo_api()
        monitor_cuckoo_django()
        monitor_cuckoo_server()

if __name__ == '__main__':
    main()
