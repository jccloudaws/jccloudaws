import json
import requests
import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("event",event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        content=response['Body'].read().decode('utf-8')
        print("content",content)
        return response['ContentType']
    except Exception as e:
        print('Error getting object {} from bucket {}.'.format(key, bucket))
        raise e
    
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)