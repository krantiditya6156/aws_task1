import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):  
    try:
        print(event)
        source_bucket_name = os.environ["SourceBucketName"]
        destination_bucket_name = os.environ["DestinationBucketName"]

        if not source_bucket_name or not destination_bucket_name:
            raise ValueError("Environment variables 'SourceBucketName' or 'DestinationBucketName' are not set")

        bucket_name = event['Records'][0]['s3']['bucket']['name']
        print("bucket_name: ", event['Records'][0]['s3']['bucket']['name'])

        file_name = event['Records'][0]['s3']['object']['key']
        print("file_name: ", event['Records'][0]['s3']['object']['key'])

        s3 = boto3.client('s3')
     
        if bucket_name == source_bucket_name:
            copy_source = {'Bucket': bucket_name, 'Key': file_name}
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=file_name)
            print("File copied successfully")
        else:
            raise ValueError(f"Event received from an unexpected bucket: {bucket_name}")    

        return {
            'statusCode': 200,
            'body': json.dumps(f"File {file_name} copied from {source_bucket_name} to {destination_bucket_name}")
        }

    except ClientError as e:
        print(f"AWS ClientError: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"AWS ClientError: {str(e)}")
        }

    except ValueError as e:
        print(f"Value error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Value error: {str(e)}")
        }
    
    except KeyError as e:
        print(f"Missing key: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing key: {str(e)}")
        }
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unexpected error: {str(e)}")
        }