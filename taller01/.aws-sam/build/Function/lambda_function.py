import time
import json

def lambda_handler(event, context):
    print("event",event)
    print(type(event))
    #print("Lambda function ARN:", context.invoked_function_arn)
    #print("CloudWatch log stream name:", context.log_stream_name)
    #print("CloudWatch log group name:",  context.log_group_name)
    #print("Lambda Request ID:", context.aws_request_id)
    #print("Lambda function memory limits in MB:", context.memory_limit_in_mb)
    #time.sleep(1) 
    #print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())
    
if __name__ == "__main__":
    event={"key1":"value1"}
    lambda_handler(event,None)
    
    