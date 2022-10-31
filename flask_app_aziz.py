
from flask import Flask, request
import json
import logging
import model.config
import pickle

logging.basicConfig()
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/get_predection', methods= ['GET'])
def get_predection():
    """
    This method is to be called by kafka
    it will return a prediction of the status of the machine
    """
    data = json.loads(request.data)

    if data["device"] in model.config.map_device_mode.keys():
        trained_model = model.config.map_device_mode[data["device"] ]
        data_x = data["data"] 
        X=[]
      
        for elt in model.config.map_device_X[data["device"]]:
            print(elt)
            X.append(data_x[elt])

        with open(trained_model , 'rb') as f:
            lr = pickle.load(f)
            prediction = lr.predict([X])
            return {
                "prediction": str(prediction)
            }
            print(prediction)
    return ""


@app.route('/get_status', methods= ['GET'])
def get_statud():
    """
    Return to the user the last status of the app
    """
    return ""

if __name__ == '__main__':
    app.run()