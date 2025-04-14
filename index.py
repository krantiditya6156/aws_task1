import json
import os
import boto3


def lambda_handler(event, context):
    print(event)

    source_bucket_name = os.environ["SourceBucketName"]
    destination_bucket_name = os.environ["DestinationBucketName"]

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    print("bucket_name: ", event['Records'][0]['s3']['bucket']['name'])

    file_name = event['Records'][0]['s3']['object']['key']
    print("file_name: ", event['Records'][0]['s3']['object']['key'])

    s3 = boto3.client('s3')
    # and s3.Bucket(destination_bucket_name) in s3.buckets.all()
    try:  
        if bucket_name == source_bucket_name:
            print("Source bucket exists")
            copy_source = {'Bucket': bucket_name, 'Key': file_name}
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=file_name)
            print("File copied successfully")
        else:
            print("Source bucket or Destination bucket does not exist")
    except Exception as e:
        print("Error: ", e)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }