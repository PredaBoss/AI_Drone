# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 14:20:51 2021

@author: tudor
"""
import math

import torch
import torch.nn.functional as F

import myModel



# we load the model

filepath = "myNetwork.pt"
ann = myModel.Net(2,100,1)

ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)

while True:
    x =float( input("x = "))
    y =float( input("y = "))

    tens = torch.tensor((x,y))

    print("Result:",ann(tens).tolist()[0])
    print("The actual value:",math.sin(x + (y/math.pi)))
    print("\n")