import requests
import json

r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=L%C3%BCbeck&appid=b702c266e5dfbee0472987f9c8651d11&units=metric')
j = json.loads(r.text)
outtemp = j['main']['temp']
outpr= j['main']['pressure']
outhum=j['main']['humidity']
print (outtemp)
print (outpr)
print (outhum)
