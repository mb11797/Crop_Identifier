#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:07:57 2020

@author: manas
"""

from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def main():
    return str('Hello Universe!!!')

if __name__=="__main__":
    app.run()