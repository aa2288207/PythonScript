# -*- coding: utf-8 -*-


import os, win32api, win32con

def getenv_system(varname, default=''):
    ven_system = default
    try:
        rkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
        try:
            ven_system = str(win32api.RegQueryValueEx(rkey, varname)[0])
            ven_system = win32api.ExpandEnvironmentStrings(ven_system)
        except:
            pass
    finally:
        win32api.RegCloseKey(rkey)
    return ven_system

if __name__ == '__main__':
    # print getenv_system('TEMP')
    print os.path.join(os.getcwd(),'dll','adf.exe')