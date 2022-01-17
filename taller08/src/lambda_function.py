import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import urllib.parse
import os

secret_client = boto3.client('secretsmanager')
dynamodb_resource = boto3.resource('dynamodb')
    
def lambda_handler(event, context):
    print("event",event)
    secretId= os.getenv("credentialsEmblue")
    secret_response = secret_client.get_secret_value(SecretId=secretId)
    secret = json.loads(secret_response.get('SecretString'))
    print("secret",secret)
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)