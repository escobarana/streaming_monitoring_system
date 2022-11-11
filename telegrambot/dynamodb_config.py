import boto3
import os

"""
    This file has the necessary configurations to successfully connect to DynamoDB on AWS
"""

client = boto3.client(
    'dynamodb',
    region_name=os.environ["AWS_REGION_NAME"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ["AWS_REGION_NAME"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)

ddb_exceptions = client.exceptions
