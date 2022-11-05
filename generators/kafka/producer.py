from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from generators.kafka.raspberry_sensor_schema import schema as schema_str
import os


def sensor_to_dict(data, ctx):
    """
        Function to transform a Sensor object into a dictionary
    :param data: Sensor
    :param ctx:
    :return:
    """
    return dict(data)


def delivery_report(err, msg):
    """
        Message to be sent on delivery of a produced message to a kafka topic
    :param err: error message
    :param msg: success message
    :return:
    """
    if err is not None:
        print(f"Delivery failed for Sensor record {msg.key()}: {err}")
    print(
        f'Sensor record {msg.key()} successfully produced to {msg.topic()} [{msg.partition}] at offset {msg.offset()}')


# https://www.confluent.io/blog/getting-started-with-apache-kafka-in-python/?_ga=2.173179299.1203553419.1652971193-440072228.1652822793
class KafkaProducer:
    """
        KafkaProducer Class to send topics to kafka cloud cluster
    """

    def __init__(self):
        """
            Initialization of the class KafkaProducer configuring the broker and cloud settings from Confluent Cloud
        """
        conf = {
            'bootstrap.servers': os.environ["KAFKA_BROKER_SETTINGS"],
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': os.environ["KAFKA_CLUSTER_KEY"],
            'sasl.password': os.environ["KAFKA_CLUSTER_SECRET"]
        }

        schema_registry_conf = {'url': os.environ["KAFKA_SCHEMA_ENDPOINT"],
                                'basic.auth.user.info': f"{os.environ['SCHEMA_USERNAME']}:{os.environ['SCHEMA_PASSWORD']}"
                                }
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        self.json_serializer = JSONSerializer(schema_str, schema_registry_client, sensor_to_dict)
        self.string_serializer = StringSerializer('utf_8')
        self.producer = Producer(conf)

    def produce(self, topic_name: str, value):
        """
            Function to send a topic to the kafka cluster
        :param topic_name: topic name
        :param value: the value record to be sent to the kafka topic
        :return:
        """
        print(f"Producing raspberry pi records to topic {topic_name}.")
        self.producer.produce(topic=topic_name, key=str(uuid4()), value=value)

        # Wait up to 1 second for events. Callbacks will be invoked during his method call
        # if the message is acknowledged.
        # self.producer.poll(1)

        print("n\Flushing records...")
        self.producer.flush(30)  # send the data
        print(f'Produced to topic {topic_name}')

    def produce_json(self, topic_name: str, data):
        """
            Function to produce a json document to a kafka topic
        :param topic_name: name of the topic
        :param data: the value record to be sent to the kafka topic
        :return:
        """
        # https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html
        print(f"Producing raspberry pi record to topic {topic_name}.")
        # Serve on_delivery callbacks from previous calls to produce()
        self.producer.poll(0.0)

        self.producer.produce(topic=topic_name,
                              key=self.string_serializer(str(uuid4()),
                                                         SerializationContext(topic_name, MessageField.VALUE)),
                              value=self.json_serializer(data,
                                                         SerializationContext(topic_name, MessageField.VALUE)),
                              on_delivery=delivery_report)


        print("n\Flushing record...")
        self.producer.flush()

        print(f'Produced json encoded record to topic {topic_name}')
