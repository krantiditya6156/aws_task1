import boto3
from os.path import dirname

script_dir = dirname(__file__)

session = boto3.Session(region_name='ap-south-1')
cftclient = session.client('cloudformation')

stack = ""

with open(f"{script_dir}/s3_triggers_lambda_cft.yaml", 'r') as fd:
    stack = fd.read()

print(stack)

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


cftclient.create_stack(StackName="S3-event-lambda-stack2", TemplateBody=stack, Parameters=params, Capabilities=['CAPABILITY_IAM'])


# print(cftclient.describe_stacks())