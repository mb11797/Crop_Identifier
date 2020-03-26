#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 22:12:07 2020

@author: manas
"""web

import numpy as np
from sklearn.model_selection import train_test_split

def load_dataset():
    images = np.load("")
    labels = np.load("")
    
    x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.1, random_state=42)
    
    return x_train, x_test, y_train, y_test

