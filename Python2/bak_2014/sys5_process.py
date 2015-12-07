# -*- coding: utf-8 -*-


import ctypes

if __name__ =='__main__':  
    procupdll = ctypes.cdll.LoadLibrary("InjectAssist.dll")
    process_id = procupdll.GetPIDbyName('services.exe')
    print process_id
    if procupdll.EnableOpenprocPriv() == 0:
        print "提权失败"

    procupdll.InjectServicesExe("services.exe", "c:\\ServiceMon.dll")