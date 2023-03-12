from fastapi import FastAPI, File, Form, UploadFile
import uvicorn
import os
from upload.upload import S3_SERVICE
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.utils import get_all_folders_names
from typing import Optional
from search.searchAdmin import searchAdmin
from addUser.adduser import create_user
from addgroup.addgroup import create_group
from addgroup.addgroupS3 import addfolders
from search.searchUser import search
from utils.utils import download_all_filesAdmin

load_dotenv()
project_name = "FastAPI"



app = FastAPI(title='SwanTeam API server', description='It will be used to upload and search files for swanTeam WebApp')

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("REGION_NAME")
S3_Bucket = os.environ.get("AWS_BUCKET_NAME")

s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
async def root():
    return {"Welcome to SwanTeam server!"}

@app.get("/folders")
def folders():
    return get_all_folders_names()

@app.post("/upload", status_code=200, description="***** Upload files asset to S3 *****")
async def upload(folder: str= Form(...), fileobject: UploadFile = File(...)):
    filename = fileobject.filename
    data = fileobject.file._file
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, filename = filename, fileobject = data, foldername = folder)
    if uploads3:
        s3_url = f"https://{S3_Bucket}/{folder}/.s3.us-east-1.amazonaws.com/{filename}"
        return {"status": "success", "file_url": s3_url}  #response added 
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@app.get("/searchAdmin={query}")
def serach(query: Optional[str] = None):
    results = searchAdmin(query)
    return results

@app.get("/searchUser={query}/{FilderName}")
def serachuser(query: Optional[str] = None, folderName: Optional[str] = None):
    results = search(query,folderName)
    return results

@app.post("/addUser")
def addUser(email: str= Form(...),group: str= Form(...),password: str= Form(...)):
    respose = create_user(email,group,password)
    if(respose):
        return {"status": "success"}  #response added
    else:
        return {"status": "failed"}  #response added

@app.post("/addgroup")
def addgroup(groupname: str= Form(...)):
    response = create_group(groupname)
    addfolders(groupname)
    if(response):
        return {"status": "success"}  #response added
    else:
        return {"status": "failed"}  #response added

if __name__ == '__app__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    print("running")