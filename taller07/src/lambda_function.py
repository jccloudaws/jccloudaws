import json
import requests
import boto3
#from boto3.dynamodb.conditions import Key, Attr
import urllib.parse
import os
from commom.secretmanager import SecretManager




sm=SecretManager()    
    
def lambda_handler(event, context):
    print("event",event)
    secretId= os.getenv("credentialsEmblue")
    response=sm.get_secret()
    #secret_response = secret_client.get_secret_value(SecretId=secretId)
    #secret = json.loads(secret_response.get('SecretString'))
    print("secret",response)
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)