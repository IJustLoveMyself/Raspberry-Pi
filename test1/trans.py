#!/usr/bin/env python
import pycurl
import StringIO 

def cut_out(name1,name2,size):
		fa=file(name1,"r+")
		fb=file(name2,"wb")
        	fa.seek(size)
        	while True:
                	line=fa.readline()
                	fb.write(line)
                	if len(line)==0:
                        	break
		fa.close()
		fb.close()
			
def get_header(url,pl,name):
	pl.setopt(pl.URL, url)
	pl.setopt(pl.NOBODY, 1L)
	f_header=file(name,"wb")
	pl.setopt(pl.WRITEHEADER,f_header)
	try:
		pl.perform()
		f_header.close()
		f_header=file(name,"r")
		while True:
			line=f_header.readline()
			if  line.find("Content-Length")!=-1:
     				break
		line=line.split(' ')
		f_header.close()
		return int(line[1])
	except pycurl.error,error:
		print "wait for connect"
		f_header.close()
		return -1

def upload(pl,url,filename,transname):
	pl.setopt(pl.URL, url)
	#c.setopt(c.NOBODY, 1L);
	pl.setopt(pl.HTTPPOST, [
		('fileupload', (
		# upload the contents of this file
		pl.FORM_FILE, filename,
       		 # specify a different file name for the upload
		pl.FORM_FILENAME, transname,
		# specify a different content type
		pl.FORM_CONTENTTYPE, 'txt/plain',
   		 )),
		])
	pl.perform()
	print "upload"

def download(pl,url)
	pl.setopt(pl.URL,url)
	f=file("123.txt","wb")
	pl.setopt(c.WRITEDATA, f)
	# For older PycURL versions:
	#c.setopt(c.WRITEFUNCTION, buffer.write)
	pl.perform()
	print(res)
	f.close()
	
basename="data"
localfile="localdata.txt"
localfile2="localdata2.txt"
url_upload="http://192.168.2.21/http/upload/"
header="header.txt"
upload_flag=0
size=0
c = pycurl.Curl()
try:
	sendname=basename+str(upload_flag)+".txt"
	upload(c,url_upload,localfile,sendname)
	c.close()
except pycurl.error,error:
	upload_flag+=1
while(upload_flag!=0):
		url_header=url_upload+sendname
		num=get_header(url_header,c,header)
		print 111
		if(num!=-1):
			print 222
			size=size+num
			try:
#				cut_out(localfile,localfile2,size)
				sendname=basename+str(upload_flag)+".txt"
				upload(c,url_upload,localfile2,sendname)
				c.close()
				print 333
				break
			except pycurl.error,error:
				upload_flag+=1

		
