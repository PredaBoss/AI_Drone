import pickle
from queue import Queue
from random import random, randrange, randint

import numpy as np
import pygame

from Utils.Colors import Colors
from Utils.Constants import Constants
from Utils.Directions import Directions


class Map():
    def __init__(self, n=Constants.mapLength.value, m=Constants.mapLength.value, battery = 10):
        self.n = n
        self.m = m

        self.x = randint(0, n-1)
        self.y = randint(0, m-1)

        self.battery = battery
        self.surface = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.start = None
        self.sensor_index = [[None for _ in range(self.m)] for _ in range(self.n)]
        self.sensors = []

    def randomMap(self, wall_fill = 0.2, sensor_fill = 0.04):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= wall_fill and (i != self.x or j != self.y):
                    self.surface[i][j] = 1
                elif random() <= sensor_fill and (i != self.x or j != self.y):
                    self.surface[i][j] = 2
        self.analyzeMap()

    def loadMap(self):
        self.surface = []
        with open("map.txt") as file:
            self.n, self.m = map(int, file.readline.strip().split(" "))
            for row in range(self.n):
                self.surface.append(list(map(int, file.readline().strip().split(" "))))
                self.x, self.y = list(map(int, file.readline().strip().split(" ")))

        self.analyzeMap()

    def analyzeMap(self):
        self.nr_of_sensors = 0
        self.sensors = []
        self.surface[self.x][self.y] = 2
        self.sensor_index = [[None for _ in range(self.m)] for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 2:
                    self.sensor_index[i][j] = self.nr_of_sensors
                    self.nr_of_sensors += 1
                    self.sensors.append((i,j))
                    if self.x == i and self.y == j:
                        self.start = self.sensor_index[i][j]

        self.paths = [[None for _ in range(self.nr_of_sensors)] for _ in range(self.nr_of_sensors)]
        for sensor in range(self.nr_of_sensors):
            q = Queue()
            distance = [[None for _ in range(self.m)] for _ in range(self.n)]
            prev = [[None for _ in range(self.m)] for _ in range(self.n)]
            distance[self.sensors[sensor][0]][self.sensors[sensor][1]] = 0
            q.put(self.sensors[sensor])

            while not q.empty():
                pos = q.get()
                for direction in Directions.v.value:
                    next_pos = (pos[0]+direction[0], pos[1] + direction[1])
                    if 0<=next_pos[0]<self.n and 0<=next_pos[1]<self.m and self.surface[next_pos[0]][next_pos[1]]!=1:
                        if distance[next_pos[0]][next_pos[1]] is None:
                            distance[next_pos[0]][next_pos[1]] = distance[pos[0]][pos[1]] + 1
                            q.put(next_pos)
                            prev[next_pos[0]][next_pos[1]] = pos

            for i in range(self.n):
                for j in range(self.m):
                    if not (i==self.sensors[sensor][0] and j==self.sensors[sensor][1]):
                        if self.surface[i][j] == 2 and distance[i][j] is not None:
                            path = []
                            current = (i, j)
                            while current!=self.sensors[sensor]:
                                path.append(current)
                                current = prev[current[0]][current[1]]
                            self.paths[sensor][self.sensor_index[i][j]] = list(reversed(path))
        self.surface[self.x][self.y] = 0


    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string