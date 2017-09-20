#!/usr/bin/env python
import pycurl
import StringIO 

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

c = pycurl.Curl()
upload(c,"http://192.168.2.21/http/upload/","wudao.txt","123.txt")
c.close()

