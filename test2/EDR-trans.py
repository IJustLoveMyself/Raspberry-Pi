#!/usr/bin/env python
import bluetooth
import subprocess
import time
#sub=subprocess.Popen("sudo hciconfig hci0 up",shell=True)
#sub=subprocess.Popen("sudo hciconfig hci0 piscan",shell=True)
#
#server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#
#port = 1
#server_sock.bind(("",port))
#server_sock.listen(1) 
#
#client_sock,address = server_sock.accept()
#print "Accepted connection from ",address
#
#data = client_sock.recv(1024)
#print "received [%s]" % data
#
#client_sock.close()
#server_sock.close()

def bluetooth():
	service_matches = bluetooth.find_service( address = "00:1B:10:F1:FB:D4" )
	while len(service_matches) == 0:
		print "couldn't find the FooBar service"
		service_matches = bluetooth.find_service( address = "00:1B:10:F1:FB:D4" )
		time.sleep(1)
	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]
	print "connecting to \"%s\" on %s port:%s" % (name, host, port)
	return port
	
port=bluetooth()
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect(( "00:1B:10:F1:FB:D4", port))
while True:
	try:
		sock.send("012345678901234567890123456789!!\r\n")
	except bluetooth.BluetoothError:
		port=bluetooth()
		sock.connect(( "00:1B:10:F1:FB:D4", port))
sock.close()