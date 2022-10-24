import os
# from dotenv import load_dotenv
from fastapi.applications import FastAPI
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from fastapi.param_functions import File, Body
from utils.utils import *
from dotenv import load_dotenv
import datetime
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import os

import imageio

from io import BytesIO

import aiofiles

from PIL import Image

from stegano import lsb




app = FastAPI(title="FastAPI")

#crossdomain configs
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#utilize functions

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image




@app.get("/ping", status_code=200, description="***** Liveliness Check *****")
async def ping():
    return {"ping": "pong"}


@app.post("/stegano", status_code=200, description="***** Upload  asset to server to stegano hide with your secert secret text *****")
async def upload(fileobject: UploadFile = File(...),secret_txt:str="secret text"):
    filename = fileobject.filename
    current_time = datetime.datetime.now()
    split_file_name = os.path.splitext(filename)   #split the file name into two different path (string + extention)
    file_name_unique = str(current_time.timestamp()).replace('.','')  #for realtime application you must have genertae unique name for the file
    img_uploaded = read_imagefile(await fileobject.read())
    # img_data = None
    # if type(file) is str :
    #     imgdata = base64.b64decode(imgstr)
    #     print("imgdata:",imgdata)
    # # filename = '%s.jpg' % photo_name 
    # with open(file.filename, 'wb') as f:
    #     f.write(imgdata)
    # img_uploaded = read_imagefile(await file.read())

    # assert img_uploaded is None
    # print("file.filename:",file.filename)
    # print("img_uploaded:",img_uploaded)
    img_uploaded_path = "uploaded_"+ str(fileobject.filename)
    print("img_uploaded_path:",img_uploaded_path)
    img_uploaded.save(img_uploaded_path)

    secret = lsb.hide(img_uploaded_path, secret_txt)

    secret_img_uploaded_path= "secret_"+img_uploaded_path
    secret.save(secret_img_uploaded_path)


    return FileResponse(secret_img_uploaded_path, media_type="image/png")


@app.post("/reveal", status_code=200, description="***** Upload  asset to server to stegano reveal *****")
async def upload4reveal(fileobject: UploadFile = File(...)):
    filename = fileobject.filename
    current_time = datetime.datetime.now()
    split_file_name = os.path.splitext(filename)   #split the file name into two different path (string + extention)
    file_name_unique = str(current_time.timestamp()).replace('.','')  #for realtime application you must have genertae unique name for the file
    img_uploaded = read_imagefile(await fileobject.read())
    # img_data = None
    # if type(file) is str :
    #     imgdata = base64.b64decode(imgstr)
    #     print("imgdata:",imgdata)
    # # filename = '%s.jpg' % photo_name 
    # with open(file.filename, 'wb') as f:
    #     f.write(imgdata)
    # img_uploaded = read_imagefile(await file.read())

    # assert img_uploaded is None
    # print("file.filename:",file.filename)
    # print("img_uploaded:",img_uploaded)
    img_uploaded_path = "uploaded_"+ str(fileobject.filename)
    print("img_uploaded_path:",img_uploaded_path)
    img_uploaded.save(img_uploaded_path)

    secret_txt = clear_message = lsb.reveal(img_uploaded_path)

    # secret_img_uploaded_path= "secret_"+img_uploaded_path
    # secret.save(secret_img_uploaded_path)
    return {'image': img_uploaded_path,'secret':secret_txt}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)