import logging

import azure.functions as func

import os
import io
import re
import json
import time
import pyodbc
from dateutil import parser
from msrest.authentication import  * #CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices. vision. computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests #pip install requests
from PIL import Image, ImageDraw, ImageFont

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Location: {myblob.uri}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    API_KEY = "76c9b819a59645b6b7cf76daab81d902"#credentials["API_KEY"]
    ENDPOINT = "https://hackcodex.cognitiveservices.azure.com/"#credentials["ENDPOINT"]

    #access azure vision using credentials
    cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
    image_location = myblob.uri
    #"https://hackxstorage.blob.core.windows.net/pictures/RRR.lt.pdf?sp=r&st=2023-06-04T09:20:55Z&se=2023-06-04T17:20:55Z&spr=https&sv=2022-11-02&sr=b&sig=MokH%2FCcUeXyV0aWJyURVwH%2BpKTxm4w4djYGMHpXxw6Q%3D"
    #"https://hackxstorage.blob.core.windows.net/pictures/IMG_0421.jpeg"
    #"https://hackxstorage.blob.core.windows.net/pictures/IMG_0420.jpeg?sp=r&st=2023-06-03T13:45:36Z&se=2023-06-03T21:45:36Z&spr=https&sv=2022-11-02&sr=b&sig=BxHM8%2BKbomm7lo6iShgHb5y3hLG%2Bdqd3d%2F%2FBlCvWLW8%3D"#os.getcwd()+"/images/IMG_0420.jpeg"#"images/IMG_0420.jpeg" 

    #sent the file to azure vision
    response = cv_client.read(
        url=image_location,
        language="lt",
        raw=True
    )

    operationLocation = response.headers['Operation-Location']

    operation_id = operationLocation.split('/')[-1]
    result = cv_client.get_read_result(operation_id)

    #get the result
    while result.status == OperationStatusCodes.running:
        time.sleep(2)
        result = cv_client.get_read_result(operation_id)

    #create the data of the corp which should not be saved
    notSIA = "DaaL Telekom SIA"
    notRegNo = "40203412722"
    notPVNNo = "LV40203412722"
    notTelNum = "+37122841151"

    #connect to DB
    server = 'databasehackx.database.windows.net'
    database = 'databasehackx'
    username = 'CloudSAc66b69ee'
    password = '{KriksisPuksis123!}'   
    driver= '{ODBC Driver 17 for SQL Server}'

    answer = ""
    #print the strings of data from image
    if result.status == OperationStatusCodes.succeeded:
        read_results = result.analyze_result.read_results
        for analyzed_result in read_results:
            for line in analyzed_result.lines:
                print(line.text)
                answer = answer + " " + line.text
                date = getDate(line.text)
                bankCode = getBankCode(line.text)
                logging.info(line.text)
    
    logging.info("DATUMS IR")
    logging.info(date)
    logging.info("BANK CODE")
    logging.info(bankCode)
    logging.info(answer)

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO Information VALUES ('{answer}');")
def getDate(text):
    try:
        date = parser.parse(text, fuzzy=True, ignoretz=True)
        return date
    except:
        pass

def getBankCode(text):
    pattern = r'^LV\d{2}[A-Z]{4}\d{11}$'
    regex = re.compile(pattern)
    try:
        bankCode = regex.match(text)
        return bankCode
    except:
        pass
