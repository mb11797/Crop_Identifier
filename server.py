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
from flask import Flask, render_template, request, jsonify, request, send_from_directory
from flask_restful import Resource, Api, reqparse
import os
import random
import string
import cv2
import datetime
from keras.preprocessing import image
import numpy as np


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'QuarterNibble'
#api = Api(app)

# Loading model and predict.
from keras.models import load_model
model=load_model('Ignore/crop.h5')

Classes = ["Potato___Early_blight","Potato___Late_blight","Potato___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot","Tomato___Tomato_mosaic_virus","Tomato___healthy"]


# Folder where the image received from android will be saved.
UPLOAD_FOLDER = os.path.basename('Uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


######################### APP ROUTES ##############################

 
@app.route('/')
def home():
    return render_template('index.html')
#    return "<h1>HOME PAGE</h1>"


# Function to convert image from base64 format (from android POST request) to bytes object and then saving it in jpg format to the disk.  
def convertImage(imgData1, upload_loc):
	with open( upload_loc, "wb") as output:
		output.write(base64.b64decode(imgData1))

def prepare(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    x = image.img_to_array(img)
    x = x/255
    return np.expand_dims(x, axis=0)


# POST
@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML
    '''
    imgData = request.get_json()
    print(1)
    currentDT = datetime.datetime.now()    
    random_string = currentDT.strftime('%m/%d/%Y')
    upload_loc = os.path.join(UPLOAD_FOLDER, random_string + ".jpg")
    convertImage(imgData, upload_loc)
#    result = model.predict_classes([prepare('/content/drive/My Drive/Test_D/Tomato_BacterialSpot/Tomato___Bacterial_spot(901).JPG')])
    result = model.predict_classes([prepare(imgData)])
    pred_disease = Classes[int(result)]
    
    return render_template('index.html', prediction='Predicted disease is ${}'.format(pred_disease))


## POST
#@app.route('/uploadform', methods=['POST'])
#def form():
#    return render_template('index.html')
#
#class ImageUpload(Resource):
#    def post(self):
#        data = request.get_json()
#        # random_string = data["latitude"] + "_" + data["longitude"]
#
#
#        random_string = "KA"
#
#        upload_loc = os.path.join(UPLOAD_FOLDER, random_string + ".jpg")
#
#        imgData = data['image']
#        convertImage(imgData, upload_loc)
#        sz = len(imgData) / (1024 * 1024)
#
#        decoded_image = cv2.imread(upload_loc)
#
##        extracted_data = pytesseract.image_to_string(decoded_image, lang='eng+hin+tam')
##
##        data = {"Image Data": extracted_data}
##
##        data = jsonify(data)
#
#        return 1



#api.add_resource(ImageUpload, '/uploadimage')



## Running the server
#if __name__ == "__main__":
#    app.run(host='127.0.0.0', port = 5000)

# Running the server
if __name__ == "__main__":
    app.run()