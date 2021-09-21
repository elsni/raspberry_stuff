# ------------------------------------------------------------
# Template for settings file - add your settings
# and rename to settings.py
# ------------------------------------------------------------

# MQTT
MQTT_BROKER = "<mqtt broker url>"
MQTT_PORT = 8883
MQTT_USER = "<your mqtt user>"
MQTT_PW   ="<your mqtt pw>"
MQTT_SUBSCRIBE = "mytopic/"            # Topic to listen to (will subscribe to mytopic/# )

# INFLUXDB
INFLUX_HOST  = 'localhost'
INFLUX_PORT  = 8086                     # default
INFLUS_USER  = '<influxdb user>'
INFLUX_PW    = '<influxdb pw>'
INFLUX_DBNAME= '<influx database name>'
