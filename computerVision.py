import os
import io
import re
import json
import time
from dateutil import parser
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices. vision. computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests #pip install requests
from PIL import Image, ImageDraw, ImageFont

credentials = json.load(open("credentials.json"))
API_KEY = "76c9b819a59645b6b7cf76daab81d902"#credentials["API_KEY"]
ENDPOINT = "https://hackcodex.cognitiveservices.azure.com/"#credentials["ENDPOINT"]

#access azure vision using credentials
cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
image_location = "https://hackxstorage.blob.core.windows.net/pictures/RRR.lt.pdf?sp=r&st=2023-06-04T09:20:55Z&se=2023-06-04T17:20:55Z&spr=https&sv=2022-11-02&sr=b&sig=MokH%2FCcUeXyV0aWJyURVwH%2BpKTxm4w4djYGMHpXxw6Q%3D"
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


#print the strings of data from image
if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)
            # if re.search('sia', line.text,re.IGNORECASE) and line.text != notSIA:
            #     sia = line.text
            # if re.search('reg. nr', line.text,re.IGNORECASE) or re.search('reg nr', line.text,re.IGNORECASE):
            #     tempReg = re.match(r"\b\d{11}\b",line.text)
            #     if tempReg:#.group(0) != notRegNo:
            #         print("SSSSSSSSSSSSSSSSSSSSSSSSSS")
            #         #regNo = tempReg
            # try:
            #     date = parser.parse(line.text, fuzzy=True, ignoretz=True)
            # except:
            #     print(line.text)

# print("Date in the string is ")
# print(date)
# print("SIA is ")
# print(sia)
# print("Reg No is ")
# print(regNo)