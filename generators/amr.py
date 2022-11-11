import os
import time
# from decimal import Decimal

from generators.sensors.measures import Measures
from kafkaproducer.producer import KafkaProducer
from dotenv import load_dotenv
# from dynamodb import dynamodb
# import json


def data_push(device: str):
    """
        This function sends a json message to the Kafka topic specified from the PC1 device
        :param device: name of the device to get the data from
    :return: None
    """
    # Loads the environmental variables within the .env file
    load_dotenv()
    topic = os.environ['TOPIC_NAME']
    pc = Measures().get_desired_data(device_name=device)
    # item = json.loads(json.dumps(pc), parse_float=Decimal)
    # dynamodb.Table('sensors_data').put_item(Item=item)
    KafkaProducer().produce_json(topic_name=topic, data=pc)


def main():
    """
        Main method of the file. Infinite loop to produce records to the kafkaproducer topic
    :return: None
    """
    while True:  # infinite loop
        data_push('pc1')
        time.sleep(5)  # Every 5 seconds to avoid data repetition in small periods of time


if __name__ == "__main__":
    main()
