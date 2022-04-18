import pickle
from random import random, randrange, randint

import numpy as np
import pygame

from Utils.Colors import Colors
from Utils.Directions import Directions


class Map():
    def __init__(self, n=Directions.mapLengh.value, m=Directions.mapLengh.value, x= None, y = None):
        self.n = n
        self.m = m

        if x is None or y is None:
            x = randint(0, n-1)
        self.x = x

        if y is None:
            y = randint(0, m-1)
        self.y = y

        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        self.surface = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill and (i != self.x or j != self.y):
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string