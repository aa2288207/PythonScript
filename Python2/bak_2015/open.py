# -*- coding:utf-8

# if not True:
#     print 'xx'
# print 'bb'

# abc = 'A1asdfasdfAddA'

# print abc.lower().find('a')

# a = ['d','a','b','c']
# b = ['b','c','d','a']
# print a.issubset(b)

# try:
#     str = 'jquery-1.11.2.min.js'
#     print str.find('.', -1)
# except Exception, e:
#     print e
# else:
#     pass
# finally:
#     pass



# import time
# import datetime

# def main():
#     print time().hour,time().minute,time().second

# if __name__ == '__main__':
#     main()


# import os
# import chardet

# import _winreg

# key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,\
#                           r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
# RunDir = _winreg.QueryValueEx(key, "Desktop")[0]

# print type(RunDir)
# print type(str(RunDir))

# print str(RunDir)
# r = chardet.detect(str(RunDir))
# print r
# os.system('pause')

for i in range(0, 10):
    print i