# benoetigt azure-iot-device, azure-iot-hub, asyncio
# Liest Temparatur, Feuchte und Luftdruck von einem BME 280 Sensor
# Holt Aktuelle Aussenwetterdaten von Openweathermap.com
# Schreibt in Influx-DB und 
# Script muss mit root-rechten laufen da sonst der Sensor nicht ausgelesen werden kann
# (w) Stephan Elsner 2021

import bme280
import time
import requests
import json
import sys
import logging
import asyncio
from datetime import datetime
from influxdb import InfluxDBClient
from azure.iot.device.aio import IoTHubDeviceClient


# Set up logging
log = "/var/log/bme280.log"
alog = logging.getLogger('asyncio')
alog.setLevel(logging.DEBUG)
handler=logging.FileHandler(filename=log,encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s %(message)s'))

#logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
alog.info('bme280 script started')


# Azure IOT Hub Connection String
CONNECTION_STRING = "<Insert device connection string here>"

# ------------------------------------------------------------
# Datenbank parameter
# ------------------------------------------------------------

host     = 'localhost'
port     = 8086 # default
user     = 'grafana'
password = '<insert password here>'
dbname   = 'temp'
location = 'schuppen'
measuremt= 'odroid-bme280'

influxclient = InfluxDBClient(host, port, user, password, dbname)

dgr = 'deg'
print('[Press CTRL + C to end the script!]')

# Vorbelegen falls die ersten Daten nicht abgerufen werden koennen
outtemp=10.0
outpr=1021
outhum=58

# Intervall der Sensormessungen in Sekunden
intervaldb = 5 
counter=11

# Intervall der Abruf der Wetterdaten und Pushen in Azure IoT Hub
# also interval * intervaldb = sekunden
interval=12 

alog.info('azure / webweather interval: '+str(interval))


async def main():
	alog.info("bme280 main started")
	global counter
	try:
		# IoT Hub Init
		azclient = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
		await azclient.connect()

		while(True):
			try:
				temperature,pressure,humidity = bme280.readBME280All()
				iso = time.ctime()
				counter = counter+1

				# Wetterdaten abrufen
				if counter==interval:
					logging.info("request openweathermap")
					print ("Abruf von Wetterdaten")
					try:
						r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=L%C3%BCbeck&appid=b702c266e5dfbee0472987f9c8651d11&units=metric')
						j = json.loads(r.text)
						outtemp = j['main']['temp']
						outpr= j['main']['pressure']
						outhum=j['main']['humidity']
					except:
						print ("Error beim Abruf der Wetterdaten")
						alog.exception("Fehler beim Abruf der Wetterdaten")


				data=[{
				"measurement":measuremt,
				"tags": { "location" : location },
				"time" : iso,
				"fields": {
				"temperature" : temperature,
				"humidity" : humidity,
				"pressure" : pressure,
				"outtemp" : float(outtemp),
				"outpressure": int(outpr),
				"outhumidity": int(outhum)
				}
				}]

				influxclient.write_points(data)

				print('Temperature = {}{}C'.format(temperature, dgr))
				print('Humidity = {:.2f}%'.format(humidity))
				print('Pressure = {:.2f}hPa\n'.format(pressure))

				# Pushen in Azure IoT Hub
				if counter==interval:
					alog.info("Push to Azure")
					print ("Push to Azure...")
#					await azclient.send_message(json.dumps(data[0]))
					counter=0

				time.sleep(intervaldb)
			except KeyboardInterrupt:
				raise
			except:
				alog.exception("Error schleife aussen")

	except KeyboardInterrupt:
		print('Script end!')
		await azclient.shutdown()

if __name__ == "__main__":
	asyncio.run(main())

alog.info("Script ended.");
