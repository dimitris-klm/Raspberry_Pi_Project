import paho.mqtt.client as mqttClient
import time
import pymongo
from datetime import datetime
from pymongo import MongoClient
import json
import ast
import base64

time.sleep(1)
broker_address= "<IP_BROKER_ADDRESS>"  #Broker address. If the script runs on the same server as the broker you can use the local IP
port = <BROKER_PORT>                #Broker port
user = "<USERNAME>"                 #Connection username
password = "<PASSWORD>"             #Connection password

mongodb = MongoClient('localhost',27017) # Mongodb is installed on the server and the port that is listening to is 27017
db = mongodb.Measurements

def save_img_locally(img_binary):
    image_64_decode = base64.b64decode(img_binary)
    filename = '<FULL_PATH_OF_THE_IMAGE_TO_BE_SAVED>' + str(datetime.now().strftime('%Y%m%d%H%M')) +'.jpg' 
    with open(filename, 'wb') as f:
        f.write(image_64_decode)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")v
        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    msg_to_dict = ast.literal_eval(msg)
    msg_to_dict['load_date']=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print ("Incoming data:\n" + str(msg_to_dict))
	print ("Saving data to mongodb...")
    db.Raspberry_Pi.insert_one(msg_to_dict)
	print ("Data saved!")
	
	print ("Saving image to disk...")
    save_img_locally(msg_to_dict['image_binary'])
	print ("Image saved!")

Connected = False   #global variable for the state of the connection
client = mqttClient.Client(client_id="<INSTANCE_NAME>")       #create new instance
client.username_pw_set(user, password=password)    	#set username and password
client.on_connect= on_connect                      	#attach function to callback
client.on_message= on_message                      	#attach function to callback
client.connect(broker_address, port=port)          	#connect to broker
client.loop_start()        							#start the loop
while Connected != True:    						#Wait for connection
    time.sleep(0.1)

try:
    print ("Subscriber is listening..")
    while True:
        client.subscribe("<TOPIC>")
        client.on_message = on_message
        time.sleep(1)

except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
