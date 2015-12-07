#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function:
【记录】折腾Python中的psutil：一个用于获得处理器和系统相关信息的模块
 
http://www.crifan.com/try_python_psutil
 
Author:     Crifan Li
Version:    2013-01-02
Contact:    admin at crifan dot com
"""
 
import psutil;
 
def tryPsutil():
    pidList = psutil.get_pid_list();
    print "pidList=",pidList;
     
    processToTest = "services.exe";
    # processToTest = "YodaoDict.exe";
     
    for eachPid in pidList:
        try:
            eachProcess = psutil.Process(eachPid);
            print "eachProcess=",eachProcess;
            processName = eachProcess._name;
            print "-----------------------------------------------------------processName=",processName;
            if processName:
                if(processName.lower() == processToTest.lower()):
                    print "Found process";
                    print "processName=",processName;
                    processExe = eachProcess.exe;
                    print "processExe=",processExe;
                    processGetcwd = eachProcess.getcwd();
                    print "processGetcwd=",processGetcwd;
                    processCmdline = eachProcess.cmdline;
                    print "processCmdline=",processCmdline;
                    processStatus = eachProcess.status;
                    print "processStatus=",processStatus;
                    processUsername = eachProcess.username;
                    print "processUsername=",processUsername;
                    processCreateTime = eachProcess.create_time;
                    print "processCreateTime=",processCreateTime;
                    print "Now will terminate this process !";
                    eachProcess.terminate();
                    eachProcess.wait(timeout=3);
                    print "psutil.test()=",psutil.test();
                 
        except psutil.NoSuchProcess,pid:
            print "no process found with pid=%s"%(pid);
 
if __name__ == "__main__":
    tryPsutil();