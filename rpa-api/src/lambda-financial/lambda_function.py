import json
import os
import boto3

dynamodb_resource = boto3.resource('dynamodb')
def lambda_handler(event, context):
    table_financial= os.getenv("table")
    print("metodo",event['httpMethod'])
    if event['httpMethod']!= 'POST':
        return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False,
                    'code_status': 400, 'menssage': "http Method not support",
                    'data': {}})}
    if event['path'] in ['/rpa/financial-details']:
        try:
            playload = json.loads(event['body'])
            table = dynamodb_resource.Table(table_financial)
            row={"ndoc":playload["ndoc"],"tdoc":playload["tdoc"],"saldo":playload["saldo"]}
            table.put_item(Item= row)
            return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {'status': True,
                    'code_status': 200,
                    'menssage': "Registro creado correctamente - financial-details",
                    'data': row})}
        except Exception as e:
            print(e)
            return {"statusCode": 200,"headers": {"Content-Type": "application/json"},
                    "body": json.dumps({'status': False,
                    'code_status': 400, 'menssage': "financial-details",
                    'data': e.__str__()})}