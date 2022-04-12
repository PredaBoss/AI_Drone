# -*- coding: utf-8 -*-

import pickle
from Domain.Map import Map
from Domain.Population import Population


class Repository():
    def __init__(self):
        self.population = None
        self.map = Map()

    def createPopulation(self, battery, population_size, individual_size, going_back):
        self.population = Population(self.map, battery, population_size, individual_size, going_back)

    def load_random_map(self, fill_factor):
        self.map.randomMap(fill_factor)

    def save_map(self):
        with open("file.map","wb") as file:
            pickle.dump(self.map, file)

    def load_map(self):
        with open("file.map","rb") as file:
            self.map = pickle.load(file)