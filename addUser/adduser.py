import boto3
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("REGION_NAME")
S3_Bucket = os.environ.get("AWS_BUCKET_NAME")
poolId = os.environ.get("USER_POOL_ID")

session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
client = boto3.client('cognito-idp', region_name=AWS_REGION)

def create_user(email,group,passw):
    response = client.admin_create_user(
                UserPoolId=poolId,
                Username=email,
                TemporaryPassword= passw,
                UserAttributes=[{"Name": "email","Value": email}]
            )
    reply = client.admin_add_user_to_group( UserPoolId=poolId, Username=email, GroupName=group )
    if(response["ResponseMetadata"]["HTTPStatusCode"] == 200):
        return True
    else:
        return False