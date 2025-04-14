import boto3
import zipfile
import os
from os.path import dirname, join, basename

ZIP_FILE = "lambda-code.zip"
LAMBDA_CODE = "index.py"
LAMBDA_CODE_BUCKET = "lambda-code-bucket789"
TEMPLATE_FILE = "s3_triggers_lambda_cft.yaml"
STACK_NAME = "S3-event-lambda-stack2"
REGION = "ap-south-1"

script_dir = dirname(__file__)

def zip_lambda_code():
    zip_file_path = join(script_dir, ZIP_FILE)
    lambda_code_path = join(script_dir, LAMBDA_CODE)
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(lambda_code_path, arcname=basename(lambda_code_path))
    print("zip file created")    
    return zip_file_path

def upload_zipfile_to_s3(zip_file_path):
    s3_client = boto3.client('s3', region_name=REGION)
    s3_client.upload_file(zip_file_path, LAMBDA_CODE_BUCKET, ZIP_FILE)
    print("Zip file uploaded to s3 bucket")
    os.remove(zip_file_path)
    

def deploy_cloudformation_stack():
    template_path = join(script_dir, TEMPLATE_FILE)
    with open(template_path, 'r') as file:
        stack = file.read()

    params = [
        {
            'ParameterKey': 'SourceBucketName',
            'ParameterValue': 'source-aditya-573532'
        },
        {
            'ParameterKey': 'DestinationBucketName',
            'ParameterValue': 'destination-aditya-573532'
        }
    ]

    cftclient = boto3.client('cloudformation', region_name=REGION)

    try:
        cftclient.create_stack(StackName=STACK_NAME, TemplateBody=stack, Parameters=params, Capabilities=['CAPABILITY_IAM'])
        print("creating stack")
    except cftclient.exceptions.AlreadyExistsException:
        cftclient.update_stack(StackName=STACK_NAME, TemplateBody=stack, Parameters=params, Capabilities=['CAPABILITY_IAM'])
        print("updating stack")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    zip_file = zip_lambda_code()
    upload_zipfile_to_s3(zip_file)
    deploy_cloudformation_stack()