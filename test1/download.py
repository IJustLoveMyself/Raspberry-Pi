#!/usr/bin/env python
import pycurl

c = pycurl.Curl()
c.setopt(c.URL, "http://192.168.2.21/http/upload/wudao.txt")
f=file("123.txt","wb")
c.setopt(c.RANGE,"100-");
c.setopt(c.WRITEDATA, f)
# For older PycURL versions:
#c.setopt(c.WRITEFUNCTION, buffer.write)
#res=c.perform()
#print(res)
f.close()
c.close()
