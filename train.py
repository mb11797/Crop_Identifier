#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:51:36 2020

@author: manas
"""

import os
from torchvision import transforms
import torch
import torch.nn as nn
import argparse
import numpy as np

os.environ["CUDA_VISIBLE_Devices"] = "0"
device = torch.device("cude" if torch.data.is_available() else "cpu")

def train(args):
    xtrain, xtest, ytrain, ytest = split_dataset.load_datset()
    
    