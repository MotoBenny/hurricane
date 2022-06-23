from urllib import response
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import boto3
import PIL
import urllib
from PIL import Image
import pathlib
import requests
from colorizer_app import Colorizer

# import psycopg2

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.resource('s3')
S3_BUCKET_NAME = "iro-bucket"


class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str


@app.get("/photos", response_model=List[PhotoModel])
async def get_all_photos():
    
    print(s3) 
    formatted_photos = []
    for row in rows:
        formatted_photos.append(
            PhotoModel(
                id=row[0], photo_name=row[1], photo_url=row[2]
            )
        )

    return formatted_photos


@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):
    print("Endpoint hit!!")
    print(file.filename)
    print(file.content_type)
    print(type(file.file))
    print(type(file.filename))

        
    # Upload file to AWS S3
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename,
                          ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.us-west-1.amazonaws.com/{file.filename}"
    urllib.request.urlretrieve(uploaded_file_url, f"images/{file.filename}")
    

    colorized = Colorizer(f"images/{file.filename}")
    colorized_image = Image.fromarray(colorized)
    print(type(colorized_image))
    bucket.upload_fileobj(colorized_image, file.filename,
                          ExtraArgs={"ACL": "public-read"})


    

@app.get("/test")
async def root():
    return {"message": "Hello, world!"}


@app.post("/uploadfile")
async def create_uploadfile(file: UploadFile):
    return {"filename": file.filename}
