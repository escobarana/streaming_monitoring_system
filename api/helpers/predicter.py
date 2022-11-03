import pickle
import pandas as pd


def prediction(sensors_dict: dict):
    sensors_list = [sensors_dict['Clock CPU Core #1'],
                    sensors_dict['Temperature CPU Package'],
                    sensors_dict['Load CPU Total'],
                    sensors_dict['Power CPU Package'],
                    sensors_dict['Temperature GPU Core'],
                    sensors_dict['Load GPU Core']]

    # Creates the input list for prediction
    list_for_prediction = [sensors_list]

    # Loads the model
    model = pickle.load(open('model/exported_models/pc1_model.bin', 'rb'))

    '''
    print()
    print(list_for_prediction)
    print()
    '''

    # Predicts the result using the model and the list, returns 'True' or 'False'
    print("In the process of making a prediction.")
    pred = model.predict(list_for_prediction)

    # Displays Results and Prediction in the CLI
    print()
    print(" Consumed events from Kafka and their prediction: ")
    print()
    print(pd.DataFrame(sensors_list, index=sensors_dict.keys()))
    print()
    print(" Prediction is: ")
    print()
    predicted = " No technical intervention is required" if pred else " Technical intervention is required"
    print(predicted + " for this device ")
    print()
    print()
    # return prediction
