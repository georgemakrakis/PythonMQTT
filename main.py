#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import json
import time

from models.data import Data as Data

# def on_message(client, userdata, message):
#     print("message received " ,str(message.payload.decode("utf-8")))
#     print("message topic=",message.topic)
#     print("message qos=",message.qos)
#     print("message retain flag=",message.retain)

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode) #decode json data
    print(type(m_in))
    firstDataReceived = Data(m_in["message"])
    print("RRRRR",firstDataReceived.message)
    print("broker 2 address = ",m_in["broker2"])

broker_address="127.0.0.1"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")

firstData = Data("Hello World")

data_out=json.dumps(firstData.__dict__) # encode object to JSON

client.publish("house/bulbs/bulb1",data_out)
time.sleep(4) # wait
client.loop_stop() #stop the loop
