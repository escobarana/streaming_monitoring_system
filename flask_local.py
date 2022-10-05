from flask import Flask
from raspberrypi.raspberry_singleton import Raspberry
from apscheduler.schedulers.background import BackgroundScheduler
from helpers.mqtt_config import MQTTConfig
from sensors.measures import Measures
from kafka.producer import KafkaProducer
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


@sched.scheduled_job('interval', id='send_data', seconds=5)
def data_push():
    """
        This function sends a message to the mqtt topic from the Raspberry Pi and to the kafka topic using
        CPU measurements every 5 seconds
    :return: None
    """
    # mqtt_data = Raspberry()
    # logger.warn(mqtt_data.json)
    # MQTTClient.publish(f'{os.environ["MQTT_TOPIC"]}', str(mqtt_data.json))

    topic_name = os.environ['TOPIC_NAME']

    # Creation of a Measures object
    measures_info = Measures().temperature_info
    # Initialization of a list of sensor types and their names according to the list 'myList'
    data_fields = ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package',
                   'Temperature GPU Core', 'Load GPU Core']
    # A List Comprehension to create of a list of lists containing the sensor types, the names and the values
    data_values = [[x.SensorType + " " + x.Name, x.Value] for x in measures_info if
                   x.SensorType + " " + x.Name in data_fields]

    # A loop to produce records to the Kafka topic with the selected information of sensors and their values
    for i in range(6):
        user_id = data_values[i][0]
        product = str(data_values[i][1])
        # send data to kafka topic
        KafkaProducer().produce_json(topic_name, product)


sched.start()
