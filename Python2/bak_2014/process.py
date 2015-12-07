#-*- encoding:UTF-8 -*-

import sys
import string
import psutil
import re


def get_pid(name):
    process_list = psutil.get_process_list()
    regex = r"pid=(\d+), name=u'%s'" % name
    pid = 0
    for line in process_list:
        process_info = str(line)
        print process_info
        ini_regex = re.compile(regex)
        result = ini_regex.search(process_info)
        if result is not None:
            pid = string.atoi(result.group(1))
            print result.group()
            print pid
            break


def main(argv):
    name = 'services.exe'
    get_pid(name)


if __name__ == "__main__":
    main(sys.argv)
