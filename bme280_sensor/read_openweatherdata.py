# ------------------------------------------------------------------------------------
# reads waetherdata from openweathermap.org
# you must register to receive an API key
#´(w) Stephan Elsner
# ------------------------------------------------------------------------------------

import requests
import json

APPID='xxxx' # your APPID here

r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=L%C3%BCbeck&appid={APPID}&units=metric')
j = json.loads(r.text)
outtemp = j['main']['temp']
outpr= j['main']['pressure']
outhum=j['main']['humidity']
print ('Current weather in Lübeck/Germany:')
print (f'Temperature: {outtemp} °C')
print (f'Pressure: {outpr} hPa')
print (f'Humidity: {outhum} %')

