import random
import json 
import time
from paho.mqtt import client as mqtt


def generate_latitude(lat_start, lat_end):
    return generate_ramdom(lat_start, lat_end)

def generate_longitude(long_start, long_end):
    return generate_ramdom(long_start, long_end)

def generate_ramdom(val_start, val_end):
    secure_random = random.SystemRandom()
    return secure_random.uniform(val_start, val_end)

def convert_string_to_json(string_to_convert):
    return (json.dumps(string_to_convert))

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, send_msg):
    time.sleep(1)
    msg = convert_string_to_json(send_msg)
    print("mensaje a enviar" + msg)
    result = client.publish(topic, msg)

# Variables
lat_start = -33.660556
lat_end = -33.681070
long_start = -56.811974
long_end = -56.821008

broker = '10.4.101.204'
port = 1883
topic = "v1/devices/me/telemetry"

client_id = "1333"
username = 'test_mqtt'
password = 'test_mqtt'

client = connect_mqtt()
# Funciones
while (1):
    lat_now = generate_latitude(lat_start, lat_end)
    long_now = generate_longitude(long_start, long_end)
    now = int((time.time())*1000) # current date and time
    send_msg = {"ts": now, "values": {"longitude": long_now, "latitude": lat_now}}
    publish(client, send_msg)
