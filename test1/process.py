#!/usr/bin/env python

import multiprocessing
import time

def myfunc1():
	print "myfunc1"
	print (time.strftime("%H:%M:%S"))
	print "end1"
	print (time.strftime("%H:%M:%S"))
	while True:
		print "end1"
		

def myfunc2():
	print "myfunc2"
	print (time.strftime("%H:%M:%S"))
	print "end2"
	print (time.strftime("%H:%M:%S"))
	while True:
		print "end2"
	
if __name__=="__main__":
	p1=multiprocessing.Process(target=myfunc1)
	p2=multiprocessing.Process(target=myfunc2)
	p1.start()
	p2.start()
	time.sleep(10)
	print (time.strftime("%H:%M:%S"))

