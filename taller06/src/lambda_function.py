import json
import requests
import boto3
import os
from common.secretmanager import SecretManager

sm = SecretManager()

def lambda_handler(event, context):
    print("event",event)
    secret=sm.get_secret()
    print("secret",secret)
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)