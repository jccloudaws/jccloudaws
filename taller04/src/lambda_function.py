import time
import json
import requests
import boto3

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    print("event",event)
    response = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
    print(response.json())
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)
    
    