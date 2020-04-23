#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 03:19:23 2020

@author: manas
"""

import requests
import base64
import json
import sys
from flask import Flask, render_template, request, jsonify, request, send_from_directory
from flask_restful import Resource, Api, reqparse
import os
import random
import string
#import numpy as np
#import skimage.io as io
#import numpy as np
#import pytesseract
import cv2


#app = Flask(__name__)
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'QuarterNibble'
#api = Api(app)

# Folder where the image received from android will be saved.
UPLOAD_FOLDER = os.path.basename('Uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


######################### APP ROUTES ##############################

@app.route('/')
def main():
    return render_template('index.html')
#    return "<h1>HOME PAGE</h1>"

@app.route('/index')
def index():
    return render_template('index.html')
    

# # GET
# @app.route('/api/info_back_to_android')
# def get_predicted_text(self):
# 	return "Got ur image successfully on the server"

# Function to conver image from base64 format (from android POST request) to bytes object and then saving it in jpg format to the disk.  
def convertImage(imgData1, upload_loc):
	with open( upload_loc, "wb") as output:
		output.write(base64.b64decode(imgData1))

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

#        extracted_data = pytesseract.image_to_string(decoded_image, lang='eng+hin+tam')
#
#        data = {"Image Data": extracted_data}
#
#        data = jsonify(data)

        return 1



#api.add_resource(ImageUpload, '/uploadimage')



## Running the server
#if __name__ == "__main__":
#    app.run(host='127.0.0.0', port = 5000)

# Running the server
if __name__ == "__main__":
    app.run()