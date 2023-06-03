import os
import io
import json
import time
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices. vision. computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests #pip install requests
from PIL import Image, ImageDraw, ImageFont

credentials = json.load(open("credentials.json"))
API_KEY = credentials["API_KEY"]
ENDPOINT = credentials["ENDPOINT"]

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
image_location = "https://hackxstorage.blob.core.windows.net/pictures/IMG_0421.jpeg"
#"https://hackxstorage.blob.core.windows.net/pictures/IMG_0420.jpeg?sp=r&st=2023-06-03T13:45:36Z&se=2023-06-03T21:45:36Z&spr=https&sv=2022-11-02&sr=b&sig=BxHM8%2BKbomm7lo6iShgHb5y3hLG%2Bdqd3d%2F%2FBlCvWLW8%3D"#os.getcwd()+"/images/IMG_0420.jpeg"#"images/IMG_0420.jpeg" 
#print(image_location)

response = cv_client.read(
    url=image_location,
    language="lt",
    raw=True
)

operationLocation = response.headers['Operation-Location']

operation_id = operationLocation.split('/')[-1]
result = cv_client.get_read_result(operation_id)

while result.status == OperationStatusCodes.running:
    #print(result)
    #print(result.status)
    #print(result.analyze_result)
    time.sleep(2)
    result = cv_client.get_read_result(operation_id)

if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)
            #break
