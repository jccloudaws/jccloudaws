import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import urllib.parse
import os

#secret_client = boto3.client('secretsmanager')
dynamodb_resource = boto3.resource('dynamodb')
    
def lambda_handler(event, context):
    
    tableFinancial= os.getenv("table")
    print("metodo",event['httpMethod'])
    
    if event['httpMethod']!= 'POST':
        return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False, 'code_status': 400, 'menssage': "http Method not support", 'data': {}})}
            
    if event['path'] in ['/rpa/financial-details']:
        try:
            playload = json.loads(event['body'])
            table = dynamodb_resource.Table(tableFinancial)
            row={"ndoc":playload["ndoc"],"tdoc":playload["tdoc"],"saldo":playload["saldo"]}
            response=table.put_item(Item= row)
            return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                "body": json.dumps({'status': True, 'code_status': 200, 'menssage': "Registro creado correctamente - financial-details", 'data': row})}

        except Exception as e:
            print(e)
            return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False, 'code_status': 400, 'menssage': "financial-details", 'data': e.__str__()})}
        
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)