#!/usr/bin/env python

# Blink an LED on Pin 16 to GND
# tested on ODROID C4

import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()
# pin 16 ist output
wpi.pinMode(4,1)

while True:
	wpi.digitalWrite(4,1)
	time.sleep(1)
	wpi.digitalWrite(4,0)
	time.sleep(1)


