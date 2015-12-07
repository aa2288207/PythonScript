#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import subprocess
import socket


def log():
    log_path = os.path.join(os.getcwd(), 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logging.basicConfig(filename=os.path.join(log_path, 'cuckoo_monitor.log'), level=logging.DEBUG)


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


def monitor_process(key_word, cmd):
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)

    lines = p3.stdout.readlines()
    if len(lines) > 0:
        return

    logging.info('process[%s] is lost, run [%s]' % (key_word, cmd))
    subprocess.call(cmd, shell=True)


def monitor_port(protocol, port, cmd, ip='127.0.0.1'):
    address = (ip, port)
    socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
    client = socket.socket(socket.AF_INET, socket_type)

    try:
        client.bind(address)
    except Exception:
        client.close()
    else:
        client.close()
        logging.info('port[%s-%s] is lost, run [%s]' % (protocol, port, cmd))
        subprocess.call(cmd, shell=True)


def monitor_mongodb():
    cmd = 'sudo mongod --fork --dbpath=/var/lib/mongodb --logpath=/tmp/mongod.log --port 27017 --logappend &'
    monitor_port('tcp', 27017, cmd)


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
    monitor_process('cuckoo.py', cmd)


def main(sleep_time=120):
    i = 0
    while True:
        i += 1
        logging.info('%s monitor %d ' % (get_current_time(), i))
        monitor_mongodb()
        monitor_memcached()
        monitor_sysmon()
        monitor_cuckoo_server()
        monitor_cuckoo_api()
        monitor_cuckoo_django()
        time.sleep(sleep_time)

if __name__ == '__main__':
    log()
    try:
        logging.info('\n\n%s cuckoo服务监控开始....' % get_current_time())
        main()
    except Exception, e:
        logging.error('%s %s....' % (get_current_time(), e))
    finally:
        logging.info('%s 本次cuckoo服务监控结束....\n\n' % get_current_time())
