#!/usr/bin/env python

import time
import threading

class mythread(threading.Thread):
	def __init__(self,target):
		threading.Thread.__init__(self)
		self.target = target
   
	def run(self):
		self.target()
		print"run"

def myfunc1():
     while True:
	print "myfunc1"
	print("The time is {0}".format(time.ctime()))
	time.sleep(1)
	print"end1"
	print("The time is {0}".format(time.ctime()))
	
def myfunc2():
	print "myfunc2"
	print("The time is {0}".format(time.ctime()))
	time.sleep(3)
	print"end2"
	print("The time is {0}".format(time.ctime()))

thread1=mythread(myfunc1)
thread2=mythread(myfunc2)		
#thread1=threading.Thread(target=myfunc1)
#thread2=threading.Thread(target=myfunc2)
thread1.start()
thread2.start()
print("The time is {0}".format(time.ctime())) 
time.sleep(5)
print("The time is {0}".format(time.ctime()))
	
