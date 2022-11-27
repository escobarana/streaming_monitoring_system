import config
import requests
import pickle
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def download_model(url):
    """
        This function gets the deployed model from AWS
    :param url: AWS S3 bucket URL
    :return: .bin file with the model
    """
    try:
        response = requests.get(url).content
        return response
    except:
        return False


class Predict:
    """
        Class that predicts whether a device will need technical intervention or not
    """

    def __init__(self, url_pc1=config.link_model_pc1, url_pc2=config.link_model_pc2,
                 url_rasb=config.link_model_raspberry):
        """
            Initialization of the class Predict
        :param url_pc1: URL for device PC1
        :param url_pc2: URL for device PC2
        :param url_rasb: URL for device Raspberry
        """
        self.pc1_model_url = url_pc1
        self.pc2_model_url = url_pc2
        self.rasb_model_url = url_rasb

    def predict_output(self, device: str, data: dict):
        """
            This function predicts the output value whether the device will need technical intervention or not based on
            the last produced record from the device
        :param device: device name
        :param data: dictionary containing the sensor's measurements data
        :return: last data record and prediction
        """
        url = ""
        data_input = []
        val = data  # dictionary
        if device == "pc1":
            url = self.pc1_model_url
            logging.info("URL Device: PC1")
            for i, elt in enumerate(config.pc1_features):
                for data in val:
                    if data == elt[1]:
                        print(i, data, val[data])
                        data_input.append(float(val[data]))

        elif device == "pc2":
            url = self.pc2_model_url
            logging.info("URL Device: PC2")
            for i, elt in enumerate(config.pc2_features):
                for data in val:
                    if data == elt[1]:
                        print(i, data, val[data])
                        data_input.append(float(val[data]))

        elif device == "raspberry":
            url = self.rasb_model_url
            logging.info("URL Device: RASPBERRY")
            for i, elt in enumerate(config.rasb_features):
                for data in val:
                    if data == elt[1]:
                        print(i, data, val[data])
                        data_input.append(float(val[data]))
        else:
            logging.error("Wrong device provided.")

        # Download model from AWS S3 bucket
        model_raw = download_model(url)
        model = pickle.loads(model_raw)

        data = data_input

        # Make prediction based on the deployed model
        if device == 'pc2':
            prediction = model.predict_proba([data_input + [0, 0]])
        else:
            prediction = model.predict_proba([data_input])

        return data, prediction
