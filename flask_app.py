import flask; print(flask.__version__)
from flask import Flask, render_template, request
import os
import numpy as np
import pickle


import sys
import os
import pandas as pd
from sensors.measures import Measures
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from dotenv import load_dotenv


app = Flask(__name__)
app.env = "development"
result = ""
print("I am in flask app")



@app.route('/', methods=['GET'])
def hello():
    print("I am In hello. Made some changes")
    return render_template('index.html')                           

@app.route('/ResultOutput', methods=['GET'])
def outputResultsTest():
    print()
    print(" This is a test ")
    print()
    return render_template('index_two.html')

#resultPrediction='True'
def outputResults(valueClock, valueTemperatureCPU, valueLoadCPU, 
                  valuePowerCPU, valueTemperatureGPU, valueLoadGPU):
    #resultPrediction='True'
    return render_template('index_two.html',
                            resultClock=valueClock, 
                            resultTemperatureCPU=valueTemperatureCPU, 
                            resultLoadCPUTotal=valueLoadCPU, 
                            resultPowerCPUPackage=valuePowerCPU,
                            resultTemperatureGPUCore=valueTemperatureGPU, 
                            resultLoadGPUCore=valueLoadGPU) 
                            



@app.route('/predict', methods=['POST'])
def predict():

    print(" I am in predict ")
    print("Request.method:", request.method)
    print("Request.TYPE", type(request))
    print("In the process of making a prediction.")

    if request.method == 'POST':
        print(request.form)
        

        # Parse the command line.
        parser = ArgumentParser()
        parser.add_argument('config_file', type=FileType('r'))
        parser.add_argument('--reset', action='store_true')
        args = parser.parse_args()
    
        # Loads the environmental variables within the .env file
        load_dotenv()

        # Initializes a configuration dictionary
        config =    {'bootstrap.servers': os.environ['BOOTSTRAP.SERVERS'], 'security.protocol': os.environ['SECURITY.PROTOCOL'], 
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
            #records_dict = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}
            records_dict = {key: None for key in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}

            records_dict_max_values = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}
        
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
                    topic=msg.topic()              
                    key=msg.key().decode('utf-8')           
                    value=msg.value().decode('utf-8')
                    value_parsed_1 = value.replace('[','')
                    value_parsed_2 = value_parsed_1.replace(']','')
                                
                    list_1 = value_parsed_2.split(",")              
                    value_parsed_3=list(map(float,list_1))
                                                              
                    #records_dict[key].append(value_parsed_3[0])
                    records_dict[key] = value_parsed_3[0]

                    print()
                    print(" Consumed event from topic "+topic+" -- "+key+" -- "+str(value_parsed_3[0]))
                    count += 1
                    print()

                    if count == len(records_dict):

                        print()
                        print(" I am in consumer condition  ")
                        print()
                        count = 0

                        #outputResultsTest()
                        
                        '''
                        return render_template('index_two.html',
                                            resultClock=records_dict['Clock CPU Core #1'], 
                                            resultTemperatureCPU=records_dict['Temperature CPU Package'], 
                                            resultLoadCPUTotal=records_dict['Load CPU Total'], 
                                            resultPowerCPUPackage=records_dict['Power CPU Package'],
                                            resultTemperatureGPUCore=records_dict['Temperature GPU Core'], 
                                            resultLoadGPUCore=records_dict['Load GPU Core'])
                        '''

                        #return outputResultsTest()
                        return outputResults(records_dict['Clock CPU Core #1'], 
                                            records_dict['Temperature CPU Package'],
                                            records_dict['Load CPU Total'],
                                            records_dict['Power CPU Package'],
                                            records_dict['Temperature GPU Core'],
                                            records_dict['Load GPU Core'])

                       
                       
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()            




        '''
        model = pickle.load(open('/model/exported_models/pc1_model.bin', 'rb'))
        model = pickle.load(open('ml_model.pkl', 'rb'))
        print("Model Object: ", model)
        prediction = model.predict(test_arr)
        predicted = "Technical Intervention" if prediction else "No Technical Intervention" 
        result = f"The model has predicted that the result is: {predicted}"
        return render_template('index.html', result=result)
        '''
        
        '''
        return render_template('index_two.html', 
                                resultClock=2, 
                                resultTemperatureCPU=6, 
                                resultLoadCPUTotal=8, 
                                resultPowerCPUPackage=10,
                                resultTemperatureGPUCore=12, 
                                resultLoadGPUCore=14, resultPrediction='True')    
        '''


app.run(host='0.0.0.0', port=5001, debug=False)
