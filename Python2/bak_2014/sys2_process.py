# -*- coding: utf-8 -*-
from win32com.client import GetObject
WMI = GetObject('winmgmts:')
print WMI
processes = WMI.InstancesOf('Win32_Process')

print len(processes)

print [process.Properties_('Name').Value for process in processes]

p = WMI.ExecQuery('select * from Win32_Process where Name="services.exe"')

print [prop.Name for prop in p[0].Properties_]

print p[0].Properties_('ProcessId').Value
