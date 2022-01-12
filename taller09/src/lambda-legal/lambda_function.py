import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import urllib.parse
import os

#secret_client = boto3.client('secretsmanager')
dynamodb_resource = boto3.resource('dynamodb')
    
def lambda_handler(event, context):
    
    tableLegal= os.getenv("table")
    
    if event['httpMethod']!= 'GET':
        return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False, 'code_status': 400, 'menssage': "http Method not support", 'data': {}})}
            
    if event['path'] in ['/rpa/legal-representatives']:
            try:
                request = event['queryStringParameters']
                print("request",request)
                ndoc=request.get("ndoc",None)
                table = dynamodb_resource.Table(tableLegal)
                legales = table.query(
                            KeyConditionExpression=Key("ndoc").eq(ndoc)
                        )
                data=[]
                for item in legales['Items']:
                    row={"ndoc":item["ndoc"],"name":item["name"],"tdoc":item["tdoc"]}
                    data.append(row)
                    
                return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': True, 'code_status': 200, 'menssage': "legal-representatives", 'data': data})}
    
            except Exception as e:
                print(e)
                return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False, 'code_status': 400, 'menssage': "legal-representatives", 'data': e.__str__()})}
        
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)