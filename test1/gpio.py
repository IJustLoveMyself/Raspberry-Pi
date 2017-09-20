#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT)

GPIO.output(8,1)
time.sleep(0.5)
GPIO.output(8,0)
time.sleep(0.5)

GPIO.cleanup(8)
