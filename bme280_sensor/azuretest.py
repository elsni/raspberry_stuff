import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

CONNECTION_STRING = "<insert azure IOT device connection string here>"


async def main():
	device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
	await device_client.connect()

	print("Sending message...")
	await device_client.send_message("Testnachricht")
	print ("Message successfully sent")
	await device_client.shutdown()



if __name__ == "__main__":
	asyncio.run(main())


