#!/usr/bin/env python

import multiprocessing
import time
import select

def proc1(pipe):
	while True:
		pipe.send(3)
		print "send ok"
		time.sleep(5)
#		print "proc1 recv:" , pipe.recv()
#		time.sleep(1)

def proc2(pipe):
	while True:
		print "parent rev:",pipe.recv()

if __name__ == "__main__":
	pipe = multiprocessing.Pipe()
	p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
	p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
	p1.start()
	time.sleep(20)
	p2.start()
	while True:			
#		if pipe2[1].recv()==3:
#				print "parent rev:", pipe2[1].recv()
		time.sleep(20)
#	p2.start()
#	p2.join()
