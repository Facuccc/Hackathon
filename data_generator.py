from datetime import datetime
import random
import json 
import time
from paho.mqtt import client as mqtt

now = int((time.time())*1000)

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

class Sensors():
    def __init__(self, input_base, output_base):
        self.input_data = input_base
        self.output_data = output_base

        self.initial = time.time()
        date_t = datetime.fromtimestamp(self.initial)

        self.input_data['ts'] = date_t.strftime("%m/%d/%Y, %H:%M:%S")
        self.output_data['ts'] = date_t.strftime("%m/%d/%Y, %H:%M:%S")
    
    def update_sensors(self):
        rand_choices = [-1, 1]

        self.initial += 30*60
        date_t = datetime.fromtimestamp(self.initial)

        self.input_data['ts'] = date_t.strftime("%m/%d/%Y, %H:%M:%S")
        self.output_data['ts'] = date_t.strftime("%m/%d/%Y, %H:%M:%S")

        for param in self.input_data.keys():
            if param != 'ts':
                self.input_data[param] = round(self.input_data[param] + self.input_data[param]*0.02*random.choice(rand_choices), 2)
                self.output_data[param] = round(self.output_data[param] + self.output_data[param]*0.02*random.choice(rand_choices), 2)

        print(self.output_data)

        return True

    def get_json_read(self):
        aux = {
            'input_sensor': self.input_data,
            'output_sensor': self.output_data
        }

        return json.dumps(aux)

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

input_sensor_params = {
    'ph': 7,
    'temperatura': 22,
    'fosforo': 0.4,
    'nitrogeno': 1
}

output_sensor_params = {
    'ph': 7,
    'temperatura': 23,
    'fosforo': 0.3,
    'nitrogeno': 1.5
}

water_sensors = Sensors(input_sensor_params, output_sensor_params)

# Variables

lat_max1 = -33.671029
lat_min1 = -33.677906
lon_max1 = -56.811211
lon_min1 = -56.818220

lat_start1 = -33.673327
lon_start1 = -56.813905

lat_max2 = -33.66749
lat_min2 = -33.67153
lon_max2 = -56.80714
lon_min2 = -56.8119

lat_start2 = -33.66962
lon_start2 = -56.80868

cow1 = Cow(lat_start1, lon_start1, lat_min1, lat_max1, lon_min1, lon_max1, name="Lola", color="blue")
cow2 = Cow(lat_start2, lon_start2, lat_min2, lat_max2, lon_min2, lon_max2, name="Lalo", color="yellow")

broker = '10.4.101.204'
port = 1883
cow_topic = "mapa/track"
sensors_topic = "mapa/sensors"

client_id = "1333"
username = 'mqtt'
password = 'jLnS7Fw422UcdC'

client = connect_mqtt()
# Funciones
initial = time.time() # current date and time

while (1):
    cow1.update_longitude()
    cow1.update_latitude()

    cow2.update_longitude()
    cow2.update_latitude()
    
    initial += 20*60
    date_t = datetime.fromtimestamp(initial)

    send_cow1 = {
        "ts": date_t.strftime("%m/%d/%Y, %H:%M:%S"), 
        "lon": cow1.get_longitude(), 
        "lat": cow1.get_latitude(),
        "name" : cow1.get_name(),
        "color" : cow1.get_color()
        }
    resp_cow = client.publish(topic=cow_topic, payload=json.dumps(send_cow1))

    print(send_cow1)

    send_cow2 = {
        "ts": date_t.strftime("%m/%d/%Y, %H:%M:%S"), 
        "lon": cow2.get_longitude(), 
        "lat": cow2.get_latitude(),
        "name" : cow2.get_name(),
        "color" : cow2.get_color()
        }
    resp_cow = client.publish(topic=cow_topic, payload=json.dumps(send_cow2))

    print(send_cow2)

    water_sensors.update_sensors()
    resp_sensors = client.publish(sensors_topic, water_sensors.get_json_read())
    time.sleep(3)