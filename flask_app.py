from flask import Flask, request, redirect, abort
from raspberrypi.raspberry_singleton import Raspberry
from apscheduler.schedulers.background import BackgroundScheduler
from helpers.mqtt_config import MQTTConfig
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
        This function sends a message to the mqtt topic every 5 seconds
    :return: None
    """
    mqtt_data = Raspberry()
    logger.warn(mqtt_data.json)
    MQTTClient.publish(f'{os.environ["MQTT_TOPIC"]}', str(mqtt_data.json))


sched.start()
