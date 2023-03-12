import re
import requests
import json
import os
from NLP.nlp import *
from search.tfIdf import *
from search.doc2vec import *
from utils.utils import download_all_filesUSER
from OCR.ocr import get_ocr
import urllib.parse


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("REGION_NAME")
S3_Bucket = os.environ.get("AWS_BUCKET_NAME")

def search(query,group):
    allresults = []
    SearchResults = []
    finalSearchResults = {}
    docs = {}
    finalallresults = {}
    counter = 0
    query = clean_text(query)
    #get all files from s3 bucket
    files_urls = download_all_filesUSER(group)
    #convert files to string
    if files_urls:
        for fileurl in files_urls:
            textOCR = get_ocr(fileurl)
            filename = urllib.parse.unquote(fileurl.replace("https://{S3_Bucket}.s3.amazonaws.com/",""))
            textOCRclean = clean_text(textOCR)
            text_tokens = procces_text(textOCRclean)
            docs[filename] = text_tokens
            docdata = {'id' : counter, 'fileName': filename, 'url': fileurl, 'text': textOCRclean}
            allresults.append(docdata)
            counter += 1
        tfifd = TF_IFD(docs,False,query,500)
        docs2vectors = doc2vec(docs,query,20,15,False)
        if  docs2vectors:
            for doc in docs2vectors:
                if doc[1] > 0.0:
                    for doc2 in allresults:
                        if doc2['fileName'] == doc[0]:
                            SearchResults.append(doc2)
                        finalSearchResults['hits'] = SearchResults
            return finalSearchResults
    finalallresults['hits'] = allresults
    return finalallresults
