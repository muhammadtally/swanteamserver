import cv2 
import pytesseract
import numpy as np
from urllib.request import urlopen
from pdf2image import  convert_from_bytes
from os.path import splitext
from urllib.parse import urlparse
from PIL import Image
import io
import requests

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)
    return image 

def ocr_img(url):
    image = url_to_image(url)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mtall\Desktop\swan_team_server\utils\Tesseract-OCR\tesseract.exe'
    gray = get_grayscale(image)
    text = pytesseract.image_to_string(gray, lang='heb')
    return text 

def image_to_byte_array(image: Image) -> bytes:
  # BytesIO is a fake file stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file as a argument, passing a bytes io ins
  image.save(imgByteArr, format='PNG')
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def pdfOCR(url, readFlag=cv2.IMREAD_COLOR):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mtall\Desktop\swan_team_server\utils\Tesseract-OCR\tesseract.exe'
    final_text = ""
    pdf_file = requests.get(url)
    pdf_pages = convert_from_bytes(pdf_file.content, poppler_path=r'C:\Users\mtall\Desktop\Swan_Team_backend\utils\poppler-0.68.0\bin')
    for page in pdf_pages:
        page = image_to_byte_array(page)
        page = np.asarray(bytearray(page), dtype="uint8")
        page = cv2.imdecode(page, readFlag)
        gray = get_grayscale(page)
        text = pytesseract.image_to_string(gray, lang='heb')
        final_text = "{} {}".format(final_text, text)
        text = ""
    return final_text

def get_ocr(url):
    path = urlparse(url).path
    url_type = splitext(path)[1]
    if(url_type == ".pdf"):
        return pdfOCR(url)
    else:
       return ocr_img(url) 