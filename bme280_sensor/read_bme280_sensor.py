#!/usr/bin/env python

# Read bme280 sensor and prints out data.
# Made for odroid C4, requires bme280 lib

# Import modules for time and to access sensor
import time
from smbus import SMBus
from bme280 import BME280

# Initialise the BME280
bus = SMBus(0)
bme280 = BME280(i2c_dev=bus)

# Get data and disgard to avoid garbage first reading
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
time.sleep(1)	

while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
    time.sleep(1)
