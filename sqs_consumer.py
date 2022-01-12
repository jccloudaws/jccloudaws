import json
import requests
import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("event",json.dumps(event))
    
    for record in event['Records']:
        print(record['body'])
        data = json.loads(record['body'])
        print(type(record['body']))

    
    #print("data",data)
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)
