from boto3.dynamodb.conditions import Attr
from dynamodb import dynamodb


def query_with_index(device: str):
    """
        This query returns all documents on dynamodb filtering by device and ordered by loading_datetime
    :return: query response
    """
    query_response = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                         IndexName="device-loading_datetime-index")
    return query_response


# query_response_raspberry = query_with_index(device="raspberry")
# query_response_pc1 = query_with_index(device="pc1")
# query_response_pc2 = query_with_index(device="pc2")
