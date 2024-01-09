import json
import boto3
import os
from datetime import datetime

region = os.environ['AWS_REGION']
sns = boto3.client('sns', region_name=region)

def lambda_handler(event, context):
    try:
        # Log event and context object to CloudWatch Logs
        print("Event: ", json.dumps(event, indent=2))
        print("Context: ", vars(context))

        sns_message = str((int(datetime.now().timestamp()) + 1) % 1000000)
        date = str(datetime.now())

        # Create event object to return to caller
        event_obj = {
            "functionName": context.function_name,
            "SNS_Message": f"Message {sns_message} sent at {date}",
            "SNS_Subject": "New message from publisher"
        }

        # Params object for SNS
        params = {
            "Message": f"Message {sns_message} sent at {date}",
            "Subject": "New message from publisher",
            "TopicArn": os.environ['SNSTopicArn']
        }

        # Send to SNS
        result = sns.publish(**params)
        print(result)

        response = {
            "statusCode": 200,
            "body": json.dumps(event_obj, indent=2)
        }
        return response

    except Exception as e:
        print(e)
        raise e
