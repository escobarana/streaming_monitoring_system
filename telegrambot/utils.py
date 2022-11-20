import config
import prettytable as pt
import requests
from boto3.dynamodb.conditions import Attr
from dynamodb_config import dynamodb
import pickle
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_html_from_table(data=[], required_attention=False):
    """
        Returns the table format of the inserted data
    :param data: list of tuples of data
    :param required_attention: boolean variable that indicates if the machine needs attention
    :return: html in string format
    """
    table = pt.PrettyTable([' S ', '          Metric          ', '   Value    '])
    table.align['Metric'] = 'l'
    table.align['Value'] = 'r'
    for symbol, metric, value in data:
        table.add_row([symbol, metric, f'{round(value, 2):.2f}'])
    res = f'<pre>{table}</pre>'

    if not required_attention:
        res = '\n⚠️⚠️⚠️⚠️⚠️⚠️' + "\n" + res + '\n⚠️⚠️⚠️⚠️⚠️⚠️'
    else:
        res = '\n👉👈' + "\n" + res + '\n👉👈'

    return res


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


def update_data_dynamodb(uuid: str, device: str, prediction: int):
    """
        This functions updates an item in the DynamoDB table adding the prediction for a given record
    :param uuid: The uuid of the record
    :param device: The device name ['raspberry', 'pc1', 'pc2']
    :param prediction: The prediction made by the model for that item
    :return:
    """
    dynamodb.Table('sensors_data').update_item(Key={'uuid': uuid, 'device': device},
                                               UpdateExpression="set prediction=:pred",
                                               ExpressionAttributeValues={':pred': prediction},
                                               ReturnValues="UPDATED_NEW")


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

    def predict_output(self, device: str):
        """
            This function predicts the output value whether the device will need technical intervention or not based on
            the last produced record from the device
        :param device: device name
        :return: last data record and prediction
        """
        url = ""
        data_input = []
        val = get_data_dynamodb(device)  # dictionary
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
            prediction = model.predict([data_input + [0, 0]])
        else:
            prediction = model.predict([data_input])

        # Update the item in DynamoDB with the prediction result
        update_data_dynamodb(uuid=val['uuid'],
                             device=device,
                             prediction=int(prediction[0]))

        return data, prediction
