import flask; print(flask.__version__)
from flask import Flask, render_template, request
import os
import numpy as np
import pickle


import sys
import os
import pandas as pd
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from dotenv import load_dotenv



#def prediction(sensorsList, sensorsDict):
def prediction(sensorsDict):    

    sensorsList = [sensorsDict['Clock CPU Core #1'], 
                   sensorsDict['Temperature CPU Package'],
                   sensorsDict['Load CPU Total'],
                   sensorsDict['Power CPU Package'],
                   sensorsDict['Temperature GPU Core'],
                   sensorsDict['Load GPU Core']]    
    
    # Creates the input list for prediction
    list_for_prediction = [sensorsList]

    # Loads the model
    model = pickle.load(open('model/exported_models/pc1_model.bin', 'rb'))

    '''
    print()
    print(list_for_prediction)
    print()
    '''


    # Predicts the result using the model and the list, returns 'True' or 'False'
    print("In the process of making a prediction.")                                                                                          
    prediction = model.predict(list_for_prediction)
                        

    # Displays Results and Prediction in the CLI
    print()
    print(" Consumed events from Kafka and their prediction: ")
    print()
    print(pd.DataFrame(sensorsList, index=sensorsDict.keys()))
    print()
    print(" Prediction is: ")
    print()
    predicted = " No technical intervention is required" if prediction else " Technical intervention is required"
    print(predicted+" for this device ")
    print()
    print()
    #return prediction