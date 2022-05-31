import os

import torch
from PIL import Image

from train_model import SimpleNet
from utils import test_transformations

filePath = "models/network_78.model"
ann = SimpleNet()
ann.load_state_dict(torch.load(filePath))
ann.eval()

for file in os.listdir(f'test_images'):
    files = f"./test_images/" + file
    image = test_transformations(Image.open(files).convert('RGB'))
    image = image.unsqueeze(0)
    output = ann(image)
    other, prediction = torch.max(output.data, 1)
    if 1 == prediction.numpy()[0]:
        print(f"{files} is a face")
    else:
        print(f"{files} is not a face")