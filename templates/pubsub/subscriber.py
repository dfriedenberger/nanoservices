from collections.abc import Callable
import paho.mqtt.client as mqtt
import yaml
import json


# This is the Subscriber

#time to live
timelive=60

class Subscriber:

    def __init__(self):
        self.client= mqtt.Client()
        with open("pubsub.yml") as f:
            config = yaml.safe_load(f)
            self.broker = config["broker"]
            self.port = config["port"]
            self.time_to_live = config["time_to_live"]
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)
    
    def on_message(self,client, userdata, msg):
        data = msg.payload.decode()
        print("Receive message",msg)
        self.recv_message(msg.topic,json.loads(data))

    
    def listen_to_topic(self,topics : list[str], recv_message : Callable[[str,str], None]):

        self.topics = topics
        self.recv_message = recv_message
        self.client.connect(self.broker,self.port,self.time_to_live)
        self.client.loop_forever()
