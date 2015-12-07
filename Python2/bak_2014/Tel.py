#!/usr/bin/env python
#-*- coding:UTF-8 -*-

import os

def users(ud, name, phone):
    udb = {}
    
    if ud == '1':
        udb[name] = phone
    elif ud == '2':
        del udb[name]
    elif ud == '3':
        for k, v in udb.items():
            print k, ":", v
    else:
        ud = '4'
        os._exit(1)

def main():
    while True:
        ud = raw_input('Please input select: ')
        name = raw_input('Please input name: ')
        phone = raw_input('Please input phone: ')
        users(ud, name, phone)
    
    raw_input()
    
if __name__ == '__main__':
    l = [1,23,24]
    for a in l:
        print a, l[-1]
