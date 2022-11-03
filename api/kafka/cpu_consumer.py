from flask import render_template
import os
from argparse import ArgumentParser, FileType
from confluent_kafka import Consumer, OFFSET_BEGINNING
from dotenv import load_dotenv
from helpers.predicter import prediction


def output_results(valueClock, valueTemperatureCPU, valueLoadCPU, valuePowerCPU, valueTemperatureGPU, valueLoadGPU,
                   valueResult):
    return render_template('output.html',
                           resultClock=valueClock,
                           resultTemperatureCPU=valueTemperatureCPU,
                           resultLoadCPUTotal=valueLoadCPU,
                           resultPowerCPUPackage=valuePowerCPU,
                           resultTemperatureGPUCore=valueTemperatureGPU,
                           resultLoadGPUCore=valueLoadGPU,
                           resultPrediction=valueResult)


def launch_consumer_and_predicter():
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

    # Creates a Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
                consumer.assign(partitions)

    # Select the Kafka topic in confluent cloud we will be consuming records from
    topic = os.environ['TOPIC_NAME']
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:

        # Initializes a dictionary of records consumed from the kafka topic, it contains 6 key-value pairs that represents device components

        # records_dict = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}
        records_dict = {key: None for key in
                        ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package',
                         'Temperature GPU Core', 'Load GPU Core']}
        # records_dict_max_values = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}

        # Initiliazes a counter to determine when to predict
        count = 0

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

                # Appends the value consumed to the 'records_dict' dictionary
                records_dict[key] = float(value)

                print()
                # print(" Consumed event from topic "+topic+" -- "+key+" -- "+str(value_parsed_3[0]))
                # print(" Consumed event from topic "+topic+" -- "+key+" -- "+value)
                count += 1
                # print(" Count = "+str(count)+" Length Dict = "+str(len(records_dict)))
                print()

                # Condition to check if it's time to predict
                # Checks if size of 'record_dict' dictionary reached the number of devices components needed to predict
                if count == len(records_dict):
                    print()
                    print(" I am in prediction condition  ")
                    print()
                    count = 0

                    list_for_prediction_to_display = [records_dict['Clock CPU Core #1'],
                                                      records_dict['Temperature CPU Package'],
                                                      records_dict['Load CPU Total'],
                                                      records_dict['Power CPU Package'],
                                                      records_dict['Temperature GPU Core'],
                                                      records_dict['Load GPU Core']]

                    # prediction(list_for_prediction_to_display, records_dict)
                    prediction(records_dict)
                    # poll_set_prediction = prediction(list_for_prediction_to_display, records_dict)

                    # TO COMPLETE for auto refresh webpage feature
                    '''  
                    page = outputResults(records_dict['Clock CPU Core #1'], 
                            records_dict['Temperature CPU Package'],
                            records_dict['Load CPU Total'],
                            records_dict['Power CPU Package'],
                            records_dict['Temperature GPU Core'],
                            records_dict['Load GPU Core'], 
                            poll_set_prediction)

                    #return page
                    '''



    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


'''
                    # Creates the list to predict
                    list_for_prediction = [list_for_prediction_to_display]
                    print()
                    print(list_for_prediction)
                    print()
                    # Predicts the result
                    print("In the process of making a prediction.")                                                                                          
                    prediction = model.predict(list_for_prediction)

                    # Displays Results and Prediction in the CLI
                    print()
                    print(" Consumed events from Kafka and their prediction: ")
                    print()
                    print(pd.DataFrame(list_for_prediction_to_display, index=records_dict.keys()))
                    print()
                    print(" Prediction is: ")
                    print()
                    predicted = "No technical intervention is required" if prediction else "Technical intervention is required"
                    print(predicted+" for this device ")
                    print()
                    print() 

'''

# Sends the results to the template page 'index_two.html'


# TO COMPLETE for auto refresh webpage feature

# resultPredicted = f"The model has predicted that the result is: {predicted}"
# outputResultsTest()

'''
                    page = outputResults(records_dict['Clock CPU Core #1'], 
                                            records_dict['Temperature CPU Package'],
                                            records_dict['Load CPU Total'],
                                            records_dict['Power CPU Package'],
                                            records_dict['Temperature GPU Core'],
                                            records_dict['Load GPU Core'], 
                                            resultPredicted)
'''

'''                            
                        return outputResults(records_dict['Clock CPU Core #1'], 
                                            records_dict['Temperature CPU Package'],
                                            records_dict['Load CPU Total'],
                                            records_dict['Power CPU Package'],
                                            records_dict['Temperature GPU Core'],
                                            records_dict['Load GPU Core'], 
                                            resultPredicted)
'''
