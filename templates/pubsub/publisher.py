import paho.mqtt.client as mqtt
import json
import yaml

class Publisher:

    def __init__(self):
        self.client= mqtt.Client("admin")
        with open("pubsub.yml") as f:
            config = yaml.safe_load(f)
            self.broker = config["broker"]
            self.port = config["port"]
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect

        
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
    def on_publish(self,client,userdata,result):
        print("Device 1 : Data published.")

    def publish(self,topic,message):
        self.client.connect(self.broker,self.port)
        ret = self.client.publish(topic,json.dumps(message))
        print("publish",ret)