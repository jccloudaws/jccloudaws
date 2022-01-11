import json
import requests
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

secret_client = boto3.client('secretsmanager')
dynamodb_resource = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print("event",event)
    secretId= os.getenv("credentialsEmblue")
    secret_response = secret_client.get_secret_value(SecretId=secretId)
    secret = json.loads(secret_response.get('SecretString'))
    print("secret",secret)
    #---------------------------------------------------
    tableConfig= os.getenv("table")
    marca=event.get("marca",None)
    table = dynamodb_resource.Table(tableConfig)
    response = table.query(
                KeyConditionExpression=Key("marca").eq(marca)
            )
    print (response['Items'])
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)