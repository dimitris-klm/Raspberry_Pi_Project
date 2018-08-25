import paho.mqtt.client as mqttClient
import time
import sys
import Data_json
import time
from datetime import datetime,timedelta
from Hologram.HologramCloud import HologramCloud

# Connect to internet using cellular
hologram = HologramCloud(dict(),network='cellular')
hologram.network.connect()

# Get the data
data_to_transmit = Data_json.get_measurements()
time.sleep(0.5)

# Connect to Broker
broker_address= "<IP_OF_THE_BROKER>"  	#Broker address - Public IP !
port = <PORT>                     		#Broker port (Number)
user = "<USER_NAME>"                    #Connection username
password = "<PASSWORD>"               	#Connection password
sent = 0

# Function for calback method to get response
def on_publish(client,userdata,result):
    global sent
    sent = 1
    print "Message published."

client = mqttClient.Client("<INSTANCE_NAME>")                # Create new instance
client.username_pw_set(user, password=password)     	     # Set username and password
client.connect(broker_address, port=port, keepalive=60)		 # Connect to broker
client.on_publish = on_publish

now_plus_2 = datetime.now() + timedelta(minutes = 2)
try:
    while now_plus_2>datetime.now() and sent == 0:
        client.publish("dev",data_to_transmit) # Make sure you publish the message on the same topic as the one you monitor from the server side.!
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit(0)
