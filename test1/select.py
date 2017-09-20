#!/usr/bin/env python

import select
import serial
import time
import multiprocessing 

def uart(port):
	rv_buf=""
	ch=''
	while True:
		ch=port.read()
		rv_buf+=ch
		if ch=='' or ch=='\r':
			return rv_buf			
			
def uart_trans():
	send_buf0=""
	send_buf1=""
	i=0
	port0=serial.Serial("/dev/myuart0",baudrate=115200,timeout=0)
	port1=serial.Serial("/dev/ttyUSB1",baudrate=115200,timeout=0)
	fd0=file("/dev/myuart0","r+")
	fd1=file("/dev/ttyUSB1","r+")
	while True:
		rlist,wlist,elist=select.select([fd0,fd1],[],[],)
		for fd in rlist:
			if(fd==fd0):
				send_buf0=uart(port0)
				port0.write(send_buf0)
			if(fd==fd1):
				send_buf1=uart(port1)
				port1.write(send_buf1)
if __name__ =="__main__":
	uart_trans()