# Server For SwanTeam WebApp

## Table of Contents
* [SwanTeamServer](#Server-For-Swan-Team-WebApp)
  * [About](#about)
  * [Upload](#Upload)
  * [Search](#Search)
        * [Download](#Download)
        * [OCR](#OCR)
        * [NLP](#NLP)
        * [Doc2Victor](#Document-To-Victor)
   * [AddUser](#Add-User)
   * [AddGroup](#Add-Group)

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
