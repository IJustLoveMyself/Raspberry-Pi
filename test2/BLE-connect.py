#!/usr/bin/env python

from bluetooth.ble import GATTRequester

address="F8:EF:FE:C6:35:AD"
nrf=GATTRequester("F8:EF:FE:C6:35:AD", False)
#nrf.write_by_handle(0x10, str(bytearray([14, 4, 56])))
nrf.connect( wait=True, channel_type="public")
print ("OK")

# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

#from __future__ import print_function
#
#import sys
#from bluetooth.ble import GATTRequester

#
#class JustConnect(object):
#    def __init__(self, address):
#        self.requester = GATTRequester(address, False)
#        self.connect()
#
#    def connect(self):
##        print("Connecting...", end=' ')
##        sys.stdout.flush()
#
#        self.requester.connect(True)
#        print("OK!")
#
#if __name__ == '__main__':
#    if len(sys.argv) < 2:
#        print("Usage: {} <addr>".format(sys.argv[0]))
#        sys.exit(1)

#    JustConnect(address)
#    print("Done.")