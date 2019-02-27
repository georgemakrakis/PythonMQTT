#!/usr/bin/env python3
import paho.mqtt.client as mqtt #import the client1
import json
import time
import datetime
import configparser

from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient
from models.measurements import Measurements as Measurements

# Configuration initialization
config = configparser.ConfigParser()
config.read('config.ini')

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode) #decode json data
    print(type(m_in))
    print("broker 2 address = ",m_in["broker2"])

def readModbus(host, port, address, registers, roundingFactor):
    client = ModbusTcpClient(host, port)
    metrics = client.read_holding_registers(address, registers, unit=0x1)
    result = []
    for res in metrics.registers:
        result.append(round(res * roundingFactor, 2))
    client.close()

    return result


def read_data():
    # Here a call to the modbus must happen to fetch the data
    timestamp = datetime.datetime.now().strftime("%Y-%-m-%-d %H:%M:%S.%f %Z%z")
    volts = readModbus(config['DEFAULT']['METER_HOST'], config['DEFAULT']['METER_PORT'], 13312, 3, 0.1)
    amperes = readModbus(config['DEFAULT']['METER_HOST'], config['DEFAULT']['METER_PORT'], 13318, 3, 0.1)
    kWh = readModbus(config['DEFAULT']['METER_HOST'], config['DEFAULT']['METER_PORT'], 13324, 3, 0.001)

    return Measurements(timestamp, "no failure", volts, amperes, kWh)

broker_address=config['DEFAULT']['MQTT_BROKER_IP']
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

while True:
    client.loop_start() #start the loop
    print("Subscribing to topic","house/bulbs/bulb1")
    client.subscribe("meters/sendData")
    print("Publishing message to topic","meters/sendData")

    dataToSend = read_data()

    data_out=json.dumps(dataToSend.__dict__) # encode object to JSON

    client.publish("meters/sendData",data_out)
    time.sleep(4) # wait
    client.loop_stop() #stop the loop

    time.sleep(5)
