#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import json
import time
import datetime

from models.measurements import Measurements as Measurements

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode) #decode json data
    print(type(m_in))
    print("broker 2 address = ",m_in["broker2"])


def read_data():
    # Here a call to the modbus must happen to fetch the data
    timestamp = datetime.datetime.now().strftime("%Y-%-m-%-d %H:%M:%S.%f %Z%z")
    return Measurements(1, timestamp, "no failure", [])

broker_address="127.0.0.1"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("meters/sendData")
print("Publishing message to topic","meters/sendData")

dataToSend = read_data()

data_out=json.dumps(dataToSend.__dict__) # encode object to JSON

client.publish("meters/sendData",data_out)
time.sleep(4) # wait
client.loop_stop() #stop the loop
