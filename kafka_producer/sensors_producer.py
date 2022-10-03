import os
from sensors.measures import Measures
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    producer = Producer(config)


    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


    # Produce data by selecting the following relevant sensors: Clock CPU Core #1, Temperature CPU Package,
    # Load CPU Total, Power CPU Package, Temperature GPU Core and Load GPU Core

    # Creation of a Measures object
    m = Measures()

    myList = m.temperature_info

    # Select the Kafka topic in confluent cloud we will be producing records into
    topic = os.environ['TOPIC_NAME']

    # Initialization of a list of sensor types and their names according to the list 'myList'
    data_fields = ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package',
                   'Temperature GPU Core', 'Load GPU Core']

    # A List Comprehension to create of a list of lists containing the sensor types, the names and the values
    data_values = [[x.SensorType + " " + x.Name, x.Value] for x in myList if x.SensorType + " " + x.Name in data_fields]

    # A loop to produce records to the Kafka topic with the selected information of sensors and their values
    count = 0
    for i in range(6):
        user_id = data_values[i][0]
        product = str(data_values[i][1])
        producer.produce(topic, product, user_id, callback=delivery_callback)
        count += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
