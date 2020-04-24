#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 03:19:23 2020

@author: manas
"""

import requests
import base64
import json
#import sys
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api, reqparse
import os
import random
import string
import cv2
import datetime
from keras.preprocessing import image
import numpy as np
from keras.models import load_model



app = Flask(__name__)
app.config['SECRET_KEY'] = 'QuarterNibble'
api = Api(app)

# Folder where the image received from android will be saved.
UPLOAD_FOLDER = os.path.basename('Uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Loading model and predict.
model=load_model('Ignore/crop.h5')

Classes = ["Potato___Early_blight","Potato___Late_blight","Potato___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot","Tomato___Tomato_mosaic_virus","Tomato___healthy"]


######################### APP ROUTES ##############################

 
@app.route('/')
def home():
    return render_template('index.html')
#    return "<h1>HOME PAGE</h1>"


# Function to convert image from base64 format (from android POST request) to bytes object and then saving it in jpg format to the disk.  
def convertImage(imgData1, upload_loc):
    print(1)
    with open(upload_loc, "wb") as output:
        output.write(base64.b64decode(imgData1))

def prepare(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
#    img = image.res
#    img = resize(img, target_size=(256, 256))
#    img = img.resize((256, 256))
    x = image.img_to_array(img)
    x = x/255
    return np.expand_dims(x, axis=0)


    value = request.files['file']
    for key, value in request.files('file'):
        print(key)
        print(type(value))
    data = request.form.get()
    imgData = request.get_json()
    print(imgData)
    print(type)
    print(1)
    
    currentDT = datetime.datetime.now()    

# POST
@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML
    '''

    if request.method == 'POST':
        file = request.files['file']
        if file:
#            print(file.filename)
            temp = random.randint(0, 11)
#            print(file)
            upload_loc = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(upload_loc)
            
            print(upload_loc)
            img = cv2.imread(upload_loc, 0)
            cv2.imshow('image', img)
            result = model.predict_classes([prepare(upload_loc)])

            pred_disease = Classes[int(result)]
            return render_template('index.html', prediction='Predicted disease is ${}'.format(pred_disease))
    n = Classes[temp]
#    print("Name: " + n)
    return render_template('index.html', prediction='Predicted disease is {}'.format(n))
            

    value = request.files['file']
    for key, value in request.files('file'):
        print(key)
        print(type(value))
    data = request.form.get()
    imgData = request.get_json()
    print(imgData)
    print(type)
    print(1)
    currentDT = datetime.datetime.now()    
    random_string = currentDT.strftime('%m/%d/%Y')
    random_string = "mb";
    upload_loc = os.path.join(UPLOAD_FOLDER, random_string + ".jpg")
    imgData = data['file']
    print(key)
    print(value)
    convertImage(imgData, upload_loc)
    result = model.predict_classes([prepare(imgData)])
    r = request
    print(r.get_json())
    # convert string of image data to uint8
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (256,256))
    result = model.predict_classes([prepare(img)])
    pred_disease = Classes[int(result)]
    
    return render_template('index.html', prediction='Predicted disease is ${}'.format(n))
    return "MB"

# POST
@app.route('/uploadform', methods=['POST'])
def form():
    return render_template('index.html')

class ImageUpload(Resource):
    def post(self):
        data = request.get_json()
        # random_string = data["latitude"] + "_" + data["longitude"]


        random_string = "KA"

        upload_loc = os.path.join(UPLOAD_FOLDER, random_string + ".jpg")

        imgData = data['image']
        convertImage(imgData, upload_loc)
        sz = len(imgData) / (1024 * 1024)

        decoded_image = cv2.imread(upload_loc)

        extracted_data = pytesseract.image_to_string(decoded_image, lang='eng+hin+tam')

        data = {"Image Data": extracted_data}

        data = jsonify(data)

        return 1



#api.add_resource(ImageUpload, '/uploadimage')



## Running the server
#if __name__ == "__main__":
#    app.run(host='127.0.0.0', port = 5000)

# Running the server
if __name__ == "__main__":
    app.run()