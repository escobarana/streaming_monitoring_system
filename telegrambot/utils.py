import prettytable as pt
from boto3.dynamodb.conditions import Attr
from telegrambot.dynamodb_config import dynamodb
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

    if required_attention:
        res = '\n⚠️⚠️⚠️⚠️⚠️⚠️' + "\n" + res + '\n⚠️⚠️⚠️⚠️⚠️⚠️'
    else:
        res = '\n👉👈' + "\n" + res + '\n👉👈'

    return res


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
