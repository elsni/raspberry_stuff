# ------------------------------------------------------------
# Listens to a specific mqtt topic and writes incoming
# message to influx db
# subscribes to "mytopic/#" and writes key/value pairs to influxdb.
# Torpic format is <configured base topic>/<influx measurement>/<fieldname>
# If you publish "19.8" to mytopic/weather/temperature
# this will be written to influx:
# measurement: "weather", fields: {"temperature" :"19.8"}
# (w) SEPT 21 - Stephan Elsner
# ------------------------------------------------------------

import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient
from  settings import *

influxclient = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PW, INFLUX_DBNAME)
client = mqtt.Client()

# -----------------------------------------------------------------------
# Check if a string is valid JSON
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

# ----------------------------------------------------------------------
# Callback for connection
def on_connect(client, userdata, flags, rc):
    print("Connected with return value "+str(rc))

# ----------------------------------------------------------------------
# Callback for received messages (after subscribe)
def on_message(client, userdata, msg):
    subtopic = msg.topic[len(MQTT_SUBSCRIBE):]
    splitted = subtopic.split("/");

    payload = msg.payload.decode("utf-8")
    print(subtopic+" -> "+payload)
    iso = time.ctime()

    data=[]

    # return if there is no subtopic (measurement)
    if len(subtopic) == 0:
        print("ERROR: No subtopic given")
        return

    method="SET"
    # if there is a field subtopic, write directly to field
    if (len(splitted) == 2) and splitted[1]:
        method="FIELD"


    # if only 2 level topic, 2nd level is measurement and message must be JSON for the fields
    if method=="SET":
        if (not is_json(payload)) or (payload[0] != '{'):
            print ("ERROR: 2-level topic requires a JSON object as message")
            return
        else:
            data=[{
            "measurement":splitted[0],
            "time":iso,
            "fields": json.loads(payload,parse_int=str, parse_float=str)
            }]


    # if 3-level topic, one field is directly written
    if method=="FIELD":
        data=[{
        "measurement":splitted[0],
        "time":iso,
        "fields": {
            splitted[1] : payload
        }
        }]

    try:
        influxclient.write_points(data)
    except:
        print("Error writing to INFLUX")


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
client.username_pw_set(MQTT_USER,MQTT_PW)
client.connect(MQTT_BROKER,MQTT_PORT)

# subscribe to topic
client.subscribe(MQTT_SUBSCRIBE+"#");
print("running...")

client.loop_forever()

