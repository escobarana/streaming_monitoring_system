from flask import Flask, request, redirect, abort
from raspberrypi.raspberry_singleton import Raspberry
from apscheduler.schedulers.background import BackgroundScheduler
from helpers.mqtt_config import MQTTConfig
from sensors.measures import Measures
from sensors.producer import KafkaProducer
import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TODO: Endpoints

# MQTT Sending
logging.getLogger('apscheduler').setLevel(logging.WARN)
sched = BackgroundScheduler()
MQTTClient = MQTTConfig()


@sched.scheduled_job('interval', id='mqtt_send', seconds=5)
def data_push():
    """
        This function sends a message to the mqtt topic from the Raspberry Pi and to the kafka topic using
        CPU measurements every 5 seconds
    :return: None
    """
    mqtt_data = Raspberry()
    logger.warn(mqtt_data.json)
    MQTTClient.publish(f'{os.environ["MQTT_TOPIC"]}', str(mqtt_data.json))

    topic_name = os.environ['TOPIC_NAME']
    temp = Measures().get_temperature()
    power = Measures().get_power()
    load = Measures().get_load()
    voltage = Measures().get_voltage()
    fan = Measures().get_fan()
    clock = Measures().get_clock()

    # send data to kafka topic 'test'
    KafkaProducer().produce_json(topic_name, temp)
    KafkaProducer().produce_json(topic_name, power)
    KafkaProducer().produce_json(topic_name, load)
    KafkaProducer().produce_json(topic_name, voltage)
    KafkaProducer().produce_json(topic_name, fan)
    KafkaProducer().produce_json(topic_name, clock)


sched.start()
