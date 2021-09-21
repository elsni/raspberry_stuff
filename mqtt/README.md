# mqtt_to_influx.py

Script to write incoming mqtt messages to a local influx db.
Mqtt broker, influx db connections and subscribed topic can be configured in settings.py

## Example:
if you configured "db" as the topic to listen to, you can write data like so:

### Single value
publish "17.3"  to db/test/temp
will write "temp":"17.3" to measurement "test" to influx.

### multiple values by JSON
publish {"pressure":"1022", "humidity":64}  to db/air
will write "pressure":"1022" and "humidity":"64" to measurement "air" to influx.

Integers will be converted to strings
