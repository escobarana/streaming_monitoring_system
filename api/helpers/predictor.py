import requests
from boto3.dynamodb.conditions import Attr
from helpers.dynamodb import dynamodb
import pickle
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class Config:
    template_message_pc2 = "PC 2\n" + \
                           " 🕒 ClockCPUCoreOne          : {var1} \n" + \
                           " 🌡️ TemperatureCPUPackage   : {var2} \n" + \
                           " ⌛ LoadCPUTotal             : {var3} \n" + \
                           " ⚡ PowerCPUPackage          : {var4} \n" + \
                           " --------------------------------- \n" + \
                           " 📊 Prediction               : {var5} "

    template_message_pc1 = "PC 1\n" + \
                           " 🕒 ClockCPUCoreOne          : {var1} \n" + \
                           " 🌡️ TemperatureCPUPackage   : {var2} \n" + \
                           " ⌛ LoadCPUTotal             : {var3} \n" + \
                           " ⚡ PowerCPUPackage          : {var4} \n" + \
                           " 🌡️ TemperatureGPUCore      : {var5} \n" + \
                           " ⌛ LoadGPUCore              : {var6} \n" + \
                           " --------------------------------- \n" + \
                           " 📊 Prediction               : {var7} "

    template_message_rasp = "RASPBERRY PI 4B \n" + \
                            " 🕒 ClockCPUCoreOne         : {var1} \n" + \
                            " 🌡️ TemperatureCPUPackage  : {var2} \n" + \
                            " ⌛ LoadCPUTotal            : {var3} \n" + \
                            " ⚡ PowerCPUPackage         : {var4} \n" + \
                            " 🌡️ TemperatureGPUCore     : {var5} \n" + \
                            " ⌛ LoadGPUCore             : {var6} \n" + \
                            " --------------------------------- \n" + \
                            " 📊 Prediction              : {var7} "

    pc2_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage', 'LoadCPUTotal', 'PowerCPUPackage']

    pc1_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage', 'LoadCPUTotal', 'PowerCPUPackage', 'TemperatureGPUCore',
                    'LoadGPUCore']

    rasb_features = ['GPU_temp_celsius', 'CPU_temp_celsius', 'frequency_arm_hz', 'frequency_core_hz',
                     'frequency_pwm_hz',
                     'voltage_core_v']

    link_model_pc1 = "https://dstimlmodels.s3.amazonaws.com/pc1_model.bin"
    link_model_pc2 = "https://dstimlmodels.s3.amazonaws.com/pc2_model.bin"
    link_model_raspberry = "https://dstimlmodels.s3.amazonaws.com/raspb_model.bin"


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


def get_data_dynamodb(device: str):
    """
        This function returns all documents on dynamodb from the given device based on an index
    :param device: The device name to filter the query by ['raspberry', 'pc1', 'pc2']
    :return: last element from the executed query, which is the last element loaded produced by the device
    """
    query_response = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                         IndexName="device-loading_datetime-index")
    # Return the last element loaded, with latest loading_datetime
    return query_response["Items"][-1]


class Predict:
    """
        Class that predicts whether a device will need technical intervention or not
    """

    def __init__(self, url_pc1=Config.link_model_pc1, url_pc2=Config.link_model_pc2,
                 url_rasb=Config.link_model_raspberry):
        """
            Initialization of the class Predict
        :param url_pc1: URL for device PC1
        :param url_pc2: URL for device PC2
        :param url_rasb: URL for device Raspberry
        """
        self.pc1_model_url = url_pc1
        self.pc2_model_url = url_pc2
        self.rasb_model_url = url_rasb

    def predict_output(self, device: str):
        """
            This function predicts the output value whether the device will need technical intervention or not based on
            the last produced record from the device
        :param device: device name
        :return: last data record and prediction
        """
        url = ""
        data_input = []
        if device == "pc1":
            url = self.pc1_model_url
            logging.info("URL Device: PC1")
            val = get_data_dynamodb(device)
            for i, elt in enumerate(Config.pc1_features):
                for data in val:
                    if data == elt:
                        print(i, data, val[data])
                        data_input.append(float(val[data]))

        elif device == "pc2":
            url = self.pc2_model_url
            logging.info("URL Device: PC2")
            val = get_data_dynamodb(device)
            for i, elt in enumerate(Config.pc2_features):
                for data in val:
                    if data == elt:
                        print(i, data, val[data])
                        data_input.append(float(val[data]))

        elif device == "raspberry":
            url = self.rasb_model_url
            logging.info("URL Device: RASPBERRY")
            val = get_data_dynamodb(device)
            for i, elt in enumerate(Config.rasb_features):
                for data in val:
                    if data == elt:
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
            prediction = model.predict([data_input + [0, 0]])
        else:
            prediction = model.predict([data_input])

        return data, prediction
