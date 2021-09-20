# ------------------------------------------------------------
# Listens to a specific mqtt topic and writes incoming
# message to influx db
# subscribes to "mytopic/#" and writes key/value pairs to influxdb.
# If you publish "Hello" to mytopic/greeting
# this will be written to influx:
# {"Topic" :"greeting", "Message": "Hello"}
# (w) SEPT 21 - Stephan Elsner
# ------------------------------------------------------------

import time
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

# ------------------------------------------------------------
# Parameter
# ------------------------------------------------------------

MQTTBROKER = "<mqtt broker url>"
MQTTPORT = 8883
MQTTUSER = "<your mqtt user>"
MQTTPASSWD="<your mqtt pw>"
LISTENTOPIC = "mytopic/"            # Topic to listen to (will subscribe to mytopic/# )
host     = 'localhost'
port     = 8086                     # default
user     = '<influxdb user>'
password = '<influxdb pw>'
dbname   = '<influx database name>'


influxclient = InfluxDBClient(host, port, user, password, dbname)
client = mqtt.Client()

# ----------------------------------------------------------------------
# Callback for connection
def on_connect(client, userdata, flags, rc):
    print("Connected with return value "+str(rc))

# ----------------------------------------------------------------------
# Callback for received messages (after subscribe)
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    subtopic = msg.topic[len(LISTENTOPIC):]
    payload = msg.payload.decode("utf-8")
    print(subtopic+" "+payload)
    iso = time.ctime()
    data=[{
    "measurement":"mqtt",
    "time":iso,
    "fields": {
    "topic" : subtopic,
    "message" : payload
    }
    }]
    influxclient.write_points(data)


# ----------------------------------------------------------------------
# Callback for published message
def on_publish(client, userdata, result):
    print ("Message published. Topic:"+TOPIC)


# Callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# connect to mqtt broker
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(MQTTUSER,MQTTPASSWD)
client.connect(MQTTBROKER,MQTTPORT)

# subscribe to topic
client.subscribe(LISTENTOPIC+"#");
print("running...")

client.loop_forever()

