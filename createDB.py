import math
import random

import torch

nr_of_points = 1000

points = []

for _ in range(nr_of_points):
    x, y = random.random() * 20 - 10, random.random() * 20 - 10
    function_value = math.sin(x + (y/math.pi))
    points.append((x, y, function_value))
    torchData = torch.tensor([point for point in points])
    torch.save(torchData, "mydataset.dat")