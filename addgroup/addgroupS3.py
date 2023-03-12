import boto3
import os

s3 = boto3.client('s3')

S3_Bucket = os.environ.get("AWS_BUCKET_NAME")

def addfolders(folder_name):
    s3.put_object(Bucket=S3_Bucket, Key=(folder_name+'/'))
    s3.put_object(Bucket=S3_Bucket, Key=(folder_name+'/'+ "הכנסות" + '/'))
    s3.put_object(Bucket=S3_Bucket, Key=(folder_name+'/'+ "מסמך בנקאי" + '/'))
    s3.put_object(Bucket=S3_Bucket, Key=(folder_name+'/'+ "הוצאות" + '/'))
    s3.put_object(Bucket=S3_Bucket, Key=(folder_name+'/'+ "שעות עבודה" + '/'))
    return True