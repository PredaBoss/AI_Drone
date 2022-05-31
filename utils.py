import random

from PIL import Image
from torchvision.transforms import transforms

pictureSize = 64


def random_subset(s, percentage):
    out1 = []
    out2 = []
    for x in s:
        if random.random() < percentage:
            out1.append(x)
        else:
            out2.append(x)
    return out1, out2


def get_image_list(): # the list of paths to pictures

    image_list = [f'data/men{i}.jpg' for i in range(1, 51)]
    image_list.extend([f'data/women{i}.jpg' for i in range(1, 51)])
    image_list.extend([f'data/other{i}.jpg' for i in range(1, 51)])
    return image_list


def strings_to_images(strings):
    return [Image.open(file_name).convert('RGB') for file_name in strings]


test_transformations = transforms.Compose([
        transforms.Resize(pictureSize),
        transforms.CenterCrop(pictureSize),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

train_transformations = transforms.Compose([
        transforms.Resize(pictureSize),
        transforms.CenterCrop(pictureSize),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])