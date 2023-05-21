# Server For SwanTeam WebApp

## Table of Contents
* [SwanTeamServer](#Server-For-Swan-Team-WebApp)
  * [About](#about)
  * [Upload](#Upload)
  * [Search](#Search)

## About
This project is the server side of the project [SwanTeam](https://github.com/muhammadtally/swanteam). And the API Gateways were built using the [FastAPI](https://fastapi.tiangolo.com/) web framework.

This project contains functions for uploading files to **AWS S3 Bucket**, downloading files from S3 Bucket, searching for files by folder and user type in S3 Bucket, an information retrieval system based on the Doc2Victor model, adding a new folder and a new user log to S3 Bucket and Cognito Users Pool, and adding New user to **Cognito Users Pool**.

## Upload

We used AWS S3 BUCKET to save the files, and in order to do this, we built an **API gateway** for uploading, which receives the user type from the application (the files are saved in a folder named according to the user Group, so the user Group is actually the name of the company the user belongs to), and receives the file about bytes, then a Session is opened that addresses the S3 bucket and the name of the folder where the file should be saved.

## Search
File search is essentially an information retrieval system, where the search is based on the **DOC2VIC** model, that is, turning the documents from **PDF or image** documents into numeric vectors.
This system is divided into 4 processes:

1) Downloading the files from the S3 bucket
2) Performing OCR for files, when this process turns our PDF or image files into text files
3) NLP for each text file received from the files we downloaded.
4) Comparing vectors between the document vectors and the query vector.

### Download Files
The files are downloaded while opening a session according to the type of user to the folder belonging to this type of user, then the system downloads all the relevant files of this user from the S3 bucket

### OCR
After downloading the files relevant to this user, each file goes through an **OCR process**, so that this process turns the files (which in our case are image files or PDF files), into **TXT files**.
This operation is implemented by the system using the **pytesseract** library which is based on [tesseract]https://github.com/tesseract-ocr/tesseract.

### Natural language processing (NLP)
After we transferred the files to TXT files, we activate the NLP functions, which is actually a process of analyzing the received text in order to turn the files into vectors.
The NLP operations were compiled using manually built auxiliary libraries and functions (NLP folder), the auxiliary libraries:
1) [YAP-Wrapper]https://github.com/amit-shkolnik/YAP-Wrapper/blob/c214ede3839327c08b7dfd17a3c28587348fa53d/yap_api.py#L44
2) [Hebrew-Tokenizer]https://github.com/YontiLevin/Hebrew-Tokenizer

### Represent each file as a vector
After we have performed all the operations, we will now transfer each file to vector form according to the NLP operations performed, and then we will perform a vector comparison between the query vector and the vector of each and every document.
We will return the documents to the user in an array sorted by the document vector most similar to the query vector.
