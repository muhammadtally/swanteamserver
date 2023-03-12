import boto3
import os

poolId = os.environ.get('USER_POOL_ID')
AWS_REGION = os.environ.get('REGION_NAME')
client = boto3.client('cognito-idp', region_name=AWS_REGION)

def create_group(group):
    return client.create_group(UserPoolId=poolId,  GroupName=group)