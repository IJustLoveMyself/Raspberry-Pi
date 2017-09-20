#!/usr/bin/env python

def cut_out(fa,fb,size):	
	fa.seek(size)
	while True:
		line=fa.readline()
		fb.write(line)
		if len(line)==0:
			break

fa=file("wudao.txt","r+")
fb=file("456.txt","wb")
cut_out(fa,fb,5596259)	
fa.close()
fb.close()
