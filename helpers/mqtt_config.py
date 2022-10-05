import paho.mqtt.client as paho
from paho import mqtt
import json
import os
import logging
from kafka.producer import KafkaProducer

logging.basicConfig()
logger = logging.getLogger('mqtt')
logger.setLevel(logging.INFO)


class MQTTConfig:
    def __init__(self):
        # Initiate MQTT Client
        self.mqttc = paho.Client(client_id="", userdata=None)
        self.mqttc.on_connect = self.on_connect

        # Enable TLS for secure connection
        self.mqttc.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # Set username and password
        self.mqttc.username_pw_set(os.environ["HIVE_USERNAME"], os.environ["HIVE_PASSWORD"])

        # Connect with MQTT Broker
        self.mqttc.connect(os.environ["MQTT_HOST"],
                           os.environ["MQTT_PORT"],
                           os.environ["MQTT_KEEPALIVE_INTERVAL"])

        # Register publish callback function
        self.mqttc.on_message = self.on_message
        self.mqttc.on_publish = self.on_publish

        self.mqttc.on_log = self.on_log

    @staticmethod
    def on_publish(client, userdata, mid):
        print("Message Published, mid: " + str(mid))

    @staticmethod
    def on_connect(client, userdata, flags, rc, properties=None):
        client.subscribe(os.environ["MQTT_TOPIC"])
        print('Connect received with code %s. ' % rc)

    @staticmethod
    def on_message(client, userdata, msg):
        print(msg.topic)
        print(msg.qos)
        print(json.loads(msg.payload))
        # TODO: generate csv

        # payload = json.loads(msg.payload)
        # MQTT Bridge to Kafka
        # value = dict(Device=payload["device"],
        #              ClockCPUCoreOne=payload["frequency_core_hz"],
        #              TemperatureCPUPackage=payload["CPU_temp_celsius"],
        #              TemperatureGPUCore=payload["GPU_temp_celsius"],
        #              LoadCPUTotal=payload["memory_arm_bytes"],
        #              LoadGPUCore=payload["memory_gpu_bytes"],
        #              PowerCPUPackage=payload["voltage_core_v"],
        #              Throttled=payload["throttled"],
        #              loading_datetime=payload['loading_datetime'])
        # print(value)
        # KafkaProducer().produce_json(os.environ['TOPIC_NAME'], value)

    @staticmethod
    def on_log(client, userdata, level, buf):
        logger.info(buf)

    def publish(self, topic: str, message: str):
        self.mqttc.publish(topic, message)
