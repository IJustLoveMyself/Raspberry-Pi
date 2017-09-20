#!/usr/bin/env python
#coding:utf-8
import pycurl
import select
import serial
import datetime
import multiprocessing
import RPi.GPIO as GPIO
import os
import sys
import time 
import struct
from bluepy.btle import Scanner, DefaultDelegate,Peripheral



#def bluetooth():
#	class ScanDelegate(DefaultDelegate):
#		def __init__(self):
#			DefaultDelegate.__init__(self)
#
#		def handleDiscovery(self, dev, isNewDev, isNewData):
#			if isNewDev:
#				print "Discovered device", dev.addr
#			elif isNewData:
#				print "Received new data from", dev.addr
#	scanner = Scanner().withDelegate(ScanDelegate())
#	devices = scanner.scan(10.0)
#	for dev in devices:
#			info=dev.getScanData()
#			print  len(info[0])
#			if len(info)>2:	
#				print  info[2][2]
#				if info[2][2]=="SCREAM":
#					print dev.addr 
#					return dev.addr	         



#接收传感器数据string
def uart_rec_str(port):
	ch=''
	rv_buf="S"
	r_flag=0
	while True:
		ch=port.read()		
		if ch=='#':
			r_flag=0
			return rv_buf			
		if r_flag==1:
			rv_buf+=ch
		if ch=='$':
			r_flag=1
#			rv_buf="$"

#接收点击数据hex
def uart_rec_int(port):
	i=0
	ch=0
	res=0 
	rv_buf=[]
	rtn_buf="M,"
	r_flag=0
	while True:
		res=port.read()
#		print 'res: ',res,', type: ',type(res),', len: ',len(res)
		if res=='#':
			rv_buf.append(res)
#			print 'rv_buf: ',rv_buf
			if i==25:
				ch=(rv_buf[2]<<8)|rv_buf[1]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[6]<<24)|(rv_buf[5]<<16)|(rv_buf[4]<<8)|rv_buf[3]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[8]<<8)|rv_buf[7]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[12]<<24)|(rv_buf[11]<<16)|(rv_buf[10]<<8)|rv_buf[9]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[14]<<8)|rv_buf[13]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[18]<<24)|(rv_buf[17]<<16)|(rv_buf[16]<<8)|rv_buf[15]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[20]<<8)|rv_buf[19]
				rtn_buf+=str(ch)
				rtn_buf+=','
				ch=(rv_buf[24]<<24)|(rv_buf[23]<<16)|(rv_buf[22]<<8)|rv_buf[21]
				rtn_buf+=str(ch)
				return rtn_buf
			rv_buf=[]
			r_flag=0
			i=0			
		if r_flag==1:
			res = struct.unpack("b", res)   #将\xhh形式的字符串中的\x去掉
#			res=int(res,16)
			rv_buf.append(int(res[0]))   #以追加额方式存放在list中
			i=i+1
		if res=='$':
			r_flag=1
			rv_buf.append(res)
			i=i+1
#			rv_buf="$"

def bt_send(btfd,handle,buf):
	btfd.writeCharacteristic(handle,buf,withResponse=True)


def data_write(buf):
	fds=open("/scream/upload/data.txt","a+")
	fds.write(buf)
	fds.close()
			
def data_recev(port0,port1,lock,pipe0):
	ble_sendflag=0       
	flag=0      
	send_buf0=""
	send_buf1=""
	ble_buf=""
	data_buf=""
	data_buf_20_1=""
	data_buf_20_2=""
	data_buf_20_3=""
	data_buf_choose=0
	start_flag="start"
	stop_flag="stop"
	i=0  
	times=0
	fd0=open("/dev/myuart0","r+")
	fd1=open("/dev/myuart1","r+")
	port1.write(start_flag)
	port0.write(start_flag)
	conn = Peripheral("08:08:08:08:08:01","public")
	while True:
		rlist,wlist,elist=select.select([fd0,fd1,pipe0],[],[],)
		for fd in rlist:
			if(fd==fd0):
				lock.acquire()
				try:
					send_buf0=uart_rec_int(port0)
					flag=flag|0x01			
				finally:
					lock.release() 
			if(fd==fd1):
					send_buf1=uart_rec_str(port1)
					ble_sendflag=1
					flag=flag|0x10
			if(fd==pipe0):
					i=pipe0.recv()					
		if(flag == 0x11):
					flag=0
					time_0=str(datetime.datetime.now())
					data_buf=send_buf0+','+send_buf1+time_0+"\r\n"
					print(data_buf)
					data_buf_20_1+=data_buf
					times+=1
					if times==20:
						if data_buf_choose==0:
							data_buf_20_2=data_buf_20_1
							data_buf_20_3=""
							data_buf_20_1=""
							data_buf_choose=1
							p=multiprocessing.Process(target=data_write,args=(data_buf_20_2,))
							p.start()
						else:
							data_buf_20_3=data_buf_20_1
							data_buf_20_2=""
							data_buf_20_1=""
							data_buf_choose=0
							p=multiprocessing.Process(target=data_write,args=(data_buf_20_3,))
							p.start()
						times=0					
#					fds.write(data_buf)
		if(ble_sendflag==1):
			ble_sendflag=0
			ble_buf=send_buf1
			x=ble_buf.split(',') 
#			ble_buf=chr(int(x[1])/255)+chr(int(x[1])%255)+\
#							chr(int(x[3])/255)+chr(int(x[3])%255)+\
#							chr(int(x[5])/255)+chr(int(x[5])%255)+\
#							chr(int(x[7])/255)+chr(int(x[7])%255)
			ble_data=","+x[1]+",0,"+x[3]+",0,"+x[5]+",0,"+x[7]+",0,"
			ble_buf="start"+ble_data+"stop"+"\r\n"
#			conn.writeCharacteristic(0x0036,ble_buf,withResponse=True)
			bt_p=multiprocessing.Process(target=bt_send,args=(conn,0x0036,ble_buf,))
			bt_p.start()
			ble_buf=""
		if(i==1):
			port1.write(stop_flag)
			port0.write(stop_flag)
			fd0.close()
			fd1.close()
			break
				
def upload():
	c = pycurl.Curl()
#	c.setopt(c.URL,"http://192.168.2.115/upload/" )
	c.setopt(c.URL,"http://192.168.2.213/http/upload/" )
	c.setopt(c.HTTPPOST, [
		('fileupload', (
		# upload the contents of this file
		c.FORM_FILE, "/scream/upload/data.txt",
       		 # specify a different file name for the upload
		c.FORM_FILENAME, "data.txt",
		# specify a different content type
		c.FORM_CONTENTTYPE, 'txt/plain',
   		 )),
		])	
	c.perform()
	c.close()
	os.remove("/scream/upload/data.txt")
	GPIO.output(13,1)
	time.sleep(0.5)
	GPIO.output(13,0)

	
def download():
	c = pycurl.Curl()
#	c.setopt(c.URL, "http://192.168.2.115/download/data.txt")
	c.setopt(c.URL, "http://192.168.2.213/http/download/data.txt")
	f=open("/scream/download/data.txt","wb")
	c.setopt(c.WRITEDATA, f)
	c.perform()	
	f.close()
	c.close()
	
def getname():
	try:
		c = pycurl.Curl()
#		c.setopt(c.URL, "http://192.168.2.115/download/name.txt")
		c.setopt(c.URL, "http://192.168.2.213/http/download/name.txt")
		f1=open("/scream/download/name1.txt","wb+")
		c.setopt(c.WRITEDATA,f1)
		c.perform()
		c.close()
		f1.close()
	except (pycurl.error,IOError):
		os.remove("/scream/download/name1.txt")
		return 3
	f1=open("/scream/download/name1.txt","r")                 
	filename=f1.readline()
	print(filename)         
	f2=open("/scream/download/name.txt","r")
	lastname=f2.readline()
	print(lastname)
	f2.close()
	f1.close()
	if filename.find(lastname)==-1:          #对比文件名字
		f2=open("/scream/download/name.txt","wb+")
		f2.write(filename)
		f2.close()
		os.remove("/scream/download/name1.txt")
		return 1
	else:
		return 0
	
	
#def data_send(port,lock):
#	while True:
#		lock.acquire()
#			try:
##				time_1=str(datetime.datetime.now())
##				send_buf1+=time_1
##				fdm.write(send_buf1)
#				port.write(send_buf)	
#			finally:
#				lock.release()2017/6/16 星期五 上午 11:24:512017/6/16 星期五 上午 11:24:51
#		sleep(0.05)

i=0
key_flag=False
start_flag=False			 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT) #喇叭
GPIO.setup(11,GPIO.OUT) #LED
GPIO.setup(7,GPIO.IN) #按键
port0=serial.Serial("/dev/myuart0",baudrate=115200,timeout=0)
port1=serial.Serial("/dev/myuart1",baudrate=115200,timeout=0)
while True:
	filename=getname()
	print(filename)
	if filename!=3:
		break
if(filename==1):  #初始化比较文件名字，不同就下载
	download()
GPIO.output(13,1)
time.sleep(0.5)
GPIO.output(13,0)
lock = multiprocessing.Lock()	#创建锁
uart_pipe=multiprocessing.Pipe()
#ble_pipe=multiprocessing.Pipe()
GPIO.output(11,1)
p1=multiprocessing.Process(target=data_recev,args=(port0,port1,lock,uart_pipe[0],))
#p2=multiprocessing.Process(target=data_send,args=(port0,lock))
p3=multiprocessing.Process(target=upload,args=())
#p4=multiprocessing.Process(target=ble,args=(ble_pipe[0],))
#p4.start()
try:
	while True:
		if (GPIO.input(7)==0):
			time.sleep(0.2)
			if (GPIO.input(7)==0):
				if (key_flag==True):
					key_flag=False
				else:
					key_flag=True
					i=i+1
		if (key_flag==True and start_flag==False):
			p1=multiprocessing.Process(target=data_recev,args=(port0,port1,lock,uart_pipe[0],))
			GPIO.output(11,0)
			start_flag=True
			p1.start()
		if(key_flag==False and start_flag==True ):
			p3=multiprocessing.Process(target=upload,args=())
			start_flag=False
			GPIO.output(11,1)
			uart_pipe[1].send(1)
			p3.start()
except (KeyboardInterrupt,AssertionError):
	GPIO.cleanup(13)
	GPIO.cleanup(11)
	GPIO.cleanup(7)