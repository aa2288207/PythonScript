# -*- coding: utf-8 -*-
# windows 环境使用python _winreg 模块通过注册表获取系统环境变量

############################################################
# key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
# #获取该键的所有键值，因为没有方法可以获取键值的个数，所以只能用这种方法进行遍历
# try:
#     i = 0
#     while 1:
#         #EnumValue方法用来枚举键值，EnumKey用来枚举子键
#         name, value, type = _winreg.EnumValue(key, i)
#         print repr(name)
#         i +=1
# except WindowsError:
#     print 'error'

# #如果知道键的名称，也可以直接取值
# value, type = _winreg.QueryValueEx(key, "TEMP")
# print value,type
# print int(value.find('%'))
# print value.find('%',1)
# print value[value.find('%')+1: value.find('%',1)]
############################################################

import _winreg
import os

def getenv_system(varname, default=''):
    ven_system = default
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
    try:
        value, type = _winreg.QueryValueEx(key, varname)
        ven_system = os.path.join(os.getenv(value[value.find('%')+1: value.find('%', 1)]), value[value.find('%', 1)+2:])
    except:
        pass
    return ven_system

if __name__ == '__main__':
    print getenv_system('TEMP')