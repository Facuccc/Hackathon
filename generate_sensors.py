import random
import time
import json
from paho.mqtt import client as mqtt

class Sensors():
    def __init__(self, input_base, output_base):
        self.input_data = input_base
        self.output_data = output_base
    
    def update_sensors(self):
        rand_choices = [-1, 1]

        for param in self.input_data.keys():
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
    'ortofosfato': 20,
    'nitrato': 50,
    'nitrito': 13,
    'ph': 7,
    'temperatura': 25
}

output_sensor_params = {
    'ortofosfato': 21,
    'nitrato': 56,
    'nitrito': 10,
    'ph': 7,
    'temperatura': 25
}

water_sensors = Sensors(input_sensor_params, output_sensor_params)

broker = '10.4.101.204'
port = 1883
topic = "mapa/sensors"

client_id = "1333"
username = 'mqtt'
password = 'jLnS7Fw422UcdC'

client = connect_mqtt()

while(1):
    water_sensors.update_sensors()
    resp = client.publish(topic, water_sensors.get_json_read())
    print("Data sended")    
    time.sleep(5)
