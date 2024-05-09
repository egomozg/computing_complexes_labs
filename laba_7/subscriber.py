import time
import json
import random
from paho.mqtt import client as mqtt_client
import matplotlib.pyplot as plt

y_mqtt_global = []
t_mqtt_global = []

broker = 'broker.emqx.io'
port = 1883
topic = "iot-data"
client_id = f'subscribe-{random.randint(0, 1000)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %dn", rc)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, message):
        #print(f"Received message from `{message.topic}` topic")
        try:
            global y_mqtt_global, t_mqtt_global
            payload = json.loads(message.payload)
            t_mqtt_global.append(payload["t_csv"])
            y_mqtt_global.append(payload["y_csv"])
            print(f"Received `{payload}` from `{message.topic}` topic")
        except Exception as e:
            print(f"Error processing message: {e}")
    client.subscribe(topic)
    client.on_message = on_message
    print(f"Subscribed to `{topic}` topic")


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    time.sleep(35)
    client.loop_stop()
    fig, ax = plt.subplots()
    ax.plot(t_mqtt_global, y_mqtt_global)
    ax.set_title("subscriber graph")
    ax.set(xlabel='t, c', ylabel='y(t)')
    ax.grid(which='major', color='black')
    plt.show()


if __name__ == '__main__':
    run()
