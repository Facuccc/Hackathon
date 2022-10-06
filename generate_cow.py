import random
import json 
import time
from paho.mqtt import client as mqtt

class Cow():
    def __init__(self, init_lat, init_lon,
                 min_lat, max_lat,
                 min_lon, max_lon,
                 name, color):
        self.latitude = init_lat
        self.longitude = init_lon

        self.min_latitude = min_lat
        self.max_latitude = max_lat
        self.min_longitude = min_lon
        self.max_longitude = max_lon

        self.name = name
        self.color = color

    def update_latitude(self):
        rand_choices = [-1, 1]
        step = random.randint(0, 5)/10000
        new_latitude = self.latitude+(step*random.choice(rand_choices))

        if new_latitude < self.max_latitude and new_latitude > self.min_latitude:
            self.latitude = new_latitude

    def update_longitude(self):
        rand_choices = [-1, 1]
        step = random.randint(0, 5)/10000
        new_longitude = self.longitude+(step*random.choice(rand_choices))

        if new_longitude < self.max_longitude and new_longitude > self.min_longitude:
            self.longitude = new_longitude

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color


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
    result = client.publish(topic, msg)

# Variables

lat_max = -33.671029
lat_min = -33.677906
lon_max = -56.811211
lon_min = -56.818220

lat_start = -33.673327
lon_start = -56.813905

cow1 = Cow(lat_start, lon_start, lat_min, lat_max, lon_min, lon_max, name="Lola", color="blue")

broker = '10.4.101.204'
port = 1883
topic = "mapa/track"

client_id = "1333"
username = 'mqtt'
password = 'jLnS7Fw422UcdC'

client = connect_mqtt()
# Funciones
while (1):
    # lat_now = generate_latitude(lat_start, lat_end)
    # long_now = generate_longitude(long_start, long_end)


    cow1.update_longitude()
    cow1.update_latitude()

    now = int((time.time())*1000) # current date and time
    send_msg = {
        "ts": now, 
        "lon": cow1.get_longitude(), 
        "lat": cow1.get_latitude(),
        "name" : cow1.get_name(),
        "color" : cow1.get_color()
        }

    result = client.publish(topic=topic, payload=json.dumps(send_msg))

    print(send_msg)
    # publish(client, json.dumps(send_msg))
    time.sleep(1)