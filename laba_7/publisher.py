import csv
import time
import json
import random
import math as mh

from paho.mqtt import client as mqtt_client
import matplotlib.pyplot as plt

broker = 'broker.emqx.io'
port = 1883
topic = "iot-data"
client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %dn", rc)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def generate_csv(f, phi, observing_time, step):
    current_time = 0

    with open('measurements.csv', 'w') as csv_file:
        csv_file.write('t,y\n')
        while current_time < observing_time:
            y = mh.copysign(1, mh.sin(2 * mh.pi * f * current_time + mh.radians(phi)))
            csv_file.write(str(current_time) + ',' + str(y) + '\n')
            current_time += step
    print('File "measurements.csv" generated successfully')

def publish(client):
    t_csv = []
    y_csv = []
    with open("measurements.csv", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        count = 0
        for row in csv_reader:
            if count != 0:
                t_csv.append(float(row[0]))
                y_csv.append(float(row[1]))
            count += 1
    time.sleep(1)

    for a, b in zip(t_csv, y_csv):
        payload = json.dumps({"t_csv": a, "y_csv": b})
        result = client.publish(topic, payload=payload)
        status = result[0]
        if status == 0:
            print(f"Send '{payload}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(0.1)
    return y_csv, t_csv

def run():
    generate_csv(50, 0, 300e-3, 1e-3)
    client = connect_mqtt()
    client.loop_start()
    y_csv, t_csv = publish(client)

    fig, ax = plt.subplots()
    ax.plot(t_csv, y_csv)
    ax.set_title("publisher graph")
    ax.set(xlabel='t, c', ylabel='y(t)')
    ax.grid(which='major', color='black')
    plt.show()


if __name__ == '__main__':
    run()
