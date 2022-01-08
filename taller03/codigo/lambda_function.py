import time
import json
import requests
import boto3

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    print("event",event)
    my_bucket = s3.Bucket('rpa-cfn-artifacts-40888866-us-east-1')
    for file in my_bucket.objects.all():
        print(file.key)
    
if __name__ == "__main__":
    pass
    #event={"key1":"value1"}
    #lambda_handler(event,None)
    
    