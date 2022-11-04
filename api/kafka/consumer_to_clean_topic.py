import os
from argparse import ArgumentParser, FileType
from confluent_kafka import Consumer, OFFSET_BEGINNING
from dotenv import load_dotenv

if __name__ == '__main__':

    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Loads the environmental variables within the .env file
    load_dotenv()

    # Initializes a configuration dictionary
    config = {'bootstrap.servers': os.environ['BOOTSTRAP.SERVERS'],
              'security.protocol': os.environ['SECURITY.PROTOCOL'],
              'sasl.mechanisms': os.environ['SASL.MECHANISMS'], 'sasl.username': os.environ['KAFKA_CLUSTER_KEY'],
              'sasl.password': os.environ['KAFKA_CLUSTER_SECRET'], 'group.id': os.environ['GROUP.ID'],
              'auto.offset.reset': os.environ['AUTO.OFFSET.RESET']}

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)


    # Select the Kafka topic in confluenct cloud we will be consuming records from
    topic = os.environ['TOPIC_NAME']
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:

        # Initializes a dictionary of records consumed from the kafka topic, it contains 6 key-value pairs
        records_dict = {key_dict: [] for key_dict in
                        ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package',
                         'Temperature GPU Core', 'Load GPU Core']}

        records_dict_max_values = {key_dict: [] for key_dict in
                                   ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total',
                                    'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the key and value and append the value to the corresponding list
                topic = msg.topic()
                key = msg.key().decode('utf-8')
                value = msg.value().decode('utf-8')
                value_parsed_1 = value.replace('[', '')
                value_parsed_2 = value_parsed_1.replace(']', '')

                list_1 = value_parsed_2.split(",")
                value_parsed_3 = list(map(float, list_1))

                print(" Consumed event from topic " + topic + " -- " + key + " -- " + value)

                # records_dict[key].append(value_parsed_3[0])

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
