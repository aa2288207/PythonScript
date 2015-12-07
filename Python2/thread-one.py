#-*- coding: utf-8 -*-
#!/usr/bin/python

import thread
import time

# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   print 'count:%s' % count
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )

# 创建两个线程
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"

time.sleep(10) 