import boto3
import os
import json

class SecretManager(object):
    
    def __init__(self):
        self.secret_client= boto3.client('secretsmanager')
        
    def get_secret(self):
        
        try:
            secretId = os.getenv("credentialsEmblue")
            secret_response = self.secret_client.get_secret_value(SecretId=secretId)
            secret = json.loads(secret_response.get('SecretString'))
            data={
                "credentials":secret['access_token']
            }
            #response = base64.b64decode(secret['credentials'])
        except Exception as e:
            raise Exception("Error: {0}".format(str(e)))
        return data



if __name__ == "__main__":
    sm=SecretManager()
    data=sm.get_secret()
    print(data['credentials'])