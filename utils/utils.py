import os
import boto3

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("REGION_NAME")
S3_Bucket = os.environ.get("AWS_BUCKET_NAME")

s3 = boto3.resource(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_all_folders_names():
    folders_names = []
    client = boto3.client('s3')
    i = 0
    result = client.list_objects(Bucket=os.environ.get("AWS_BUCKET_NAME"), Delimiter='/')
    for f in result.get('CommonPrefixes'):
        foldername2 = f["Prefix"][:-1]
        foldername = {"value": i , "label": foldername2}
        folders_names.append(foldername)
        i += 1
    
    
    return folders_names


def get_files_from_folder(foldername):
    files_urls = []
    file_url = ""
    my_bucket = s3.Bucket(os.environ.get("AWS_BUCKET_NAME"))
    result = my_bucket.objects.filter(Prefix=foldername)
    for obj in result:
        filename = obj.key
        file_url = "https://"+ my_bucket +"/"+ foldername + ".s3.us-east-1.amazonaws.com/" + filename
        files_urls.append(file_url)
    return files_urls

def download_all_filesUSER(group):
    files_urls = []
    file_url = ""
    # download files
    for s3_object in s3.Bucket(os.environ.get("AWS_BUCKET_NAME")).objects.all():
        filename = s3_object.key
        if not filename.endswith('/'):
            if group in filename:
                    file_url = "https://swanteamfiles.s3.amazonaws.com/" + filename
                    files_urls.append(file_url)
    return files_urls

def download_all_filesAdmin():
    files_urls = []
    file_url = ""
    # download files
    for s3_object in s3.Bucket(os.environ.get("AWS_BUCKET_NAME")).objects.all():
        filename = s3_object.key
        if not filename.endswith('/'):
            file_url = "https://swanteamfiles.s3.amazonaws.com/" + filename
            files_urls.append(file_url)
    return files_urls