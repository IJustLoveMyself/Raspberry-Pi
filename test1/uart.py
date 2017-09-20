#!/usr/bin/env python

import serial
import time

def uart(port):
	rv_buf=""
	ch=''
	while True:
		ch=port.read();
		rv_buf+=ch
		if ch=='' or ch=='\r':
			return rv_buf			
			
send_buf=""
port=serial.Serial("/dev/myuart2",baudrate=115200,timeout=None)
while True:
	send_buf=uart(port)
	port.write(send_buf)
	print(send_buf)
	