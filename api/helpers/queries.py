import json
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from helpers.dynamodb import dynamodb


class DecimalEncoder(json.JSONEncoder):
    """
        Class to encode decimal into JSON object
    """

    def default(self, obj):
        # If passed in object is instance of Decimal convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # Otherwise, use the default behavior
        return json.JSONEncoder.default(self, obj)


def get_all_data() -> list:
    """
        This function returns all documents on dynamodb table
    :return: list of all devices sensor's values
    """
    query_response = dynamodb.Table('sensors_data').scan(IndexName="device-loading_datetime-index")
    return json.loads(json.dumps(query_response, cls=DecimalEncoder))


def get_data_device(device: str) -> list:
    """
        This function returns all documents on dynamodb from the device indicated
    :return: list of sensor values for the device
    """
    query_response = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                         IndexName="device-loading_datetime-index")['Items']

    return json.loads(json.dumps(query_response, cls=DecimalEncoder))


def get_device_status(device: str) -> dict:
    """
        This function returns the status in real-time of the device specified
    :return: message specifying the current status of the device
    """
    prediction = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                     IndexName="device-loading_datetime-index")['Items'][-1]['prediction']
    msg = "The device is stressed" if prediction else "The device is OK"
    return {'msg': msg}
