import pandas as pd
from boto3.dynamodb.conditions import Attr
import boto3
import os

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ["AWS_REGION_NAME"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)


def get_data_dynamodb(device: str):
    """
        This function returns all documents on dynamodb from the given device based on an index
    :param device: The device name to filter the query by ['raspberry', 'pc1', 'pc2']
    :return: last element from the executed query, which is the last element loaded produced by the device
    """
    query_response = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                         IndexName="device-loading_datetime-index")
    return query_response["Items"]


def save_into_csv(dictionary_source: dict, device_name: str):
    """
        Save the csv data into a csv file
    :param dictionary_source: dict of data produced by dynamodb
    :param device_name: name of device in reference
    :return None
    """
    pd.DataFrame(dictionary_source).to_csv(device_name + '.csv')


if __name__ == '__main__':
    save_into_csv(get_data_dynamodb('pc1'), 'training_data/data_pc_1')
    save_into_csv(get_data_dynamodb('pc2'), 'training_data/data_pc_2')
    save_into_csv(get_data_dynamodb('raspberry'), 'training_data/data_rasb')
