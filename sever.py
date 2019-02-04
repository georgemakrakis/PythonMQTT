#!/usr/bin/env python3
import paho.mqtt.client as paho
import socket

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
host = "127.0.0.1"
topic = "house/#"

# Callbacks


def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic +
          ", Message: " + str(msg.payload) + "\n")


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")


# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Your IP address is:", socket.gethostbyname(socket.gethostname()))
print("Connecting to "+host+"/"+topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# Loop forever, receiving messages
mqttc.loop_forever()

print("rc: " + str(rc))
