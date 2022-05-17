from queue import Queue
from random import random

from Utils.Directions import Directions


class Ant:
    def __init__(self, map):
        self.map = map
        self.path = [(map.x, map.y, 0)]
        self.path_of_sensors = [(map.start, 0)]
        self.battery = map.battery
        self.visited = set()
        self.visited.add(map.start)

    def efficiency(self):
        marked = [[0 for _ in range(self.map.m)] for _ in range(self.map.n)]
        for sensor in self.path_of_sensors:
            if sensor[1] == 0:
                continue
            energy = sensor[1]
            initial_position = self.map.sensors[sensor[0]]
            for i in range(4):
                current_position = initial_position
                x_modification = Directions.v.value[i][0]
                y_modification = Directions.v.value[i][1]
                for j in range(energy):
                    current_position = (current_position[0]+x_modification,current_position[1]+y_modification)
                    if not (0<=current_position[0]<self.map.n and 0<=current_position[1]<self.map.m):
                        break
                    if self.map.surface[current_position[0]][current_position[1]] == 1:
                        break
                    marked[current_position[0]][current_position[1]] = 1

        return sum([sum(row) for row in marked])

    def move(self, pheromone, alpha, beta, q0):
        current_sensor = self.path_of_sensors[-1][0]
        probabilities = []
        for next_sensor in range(self.map.nr_of_sensors):
            if self.visited.__contains__(next_sensor):
                continue
            if self.map.paths[current_sensor][next_sensor] is None:
                continue

            for energy in range(1,6):
                distance = len(self.map.paths[current_sensor][next_sensor])
                if self.battery < distance + energy:
                    continue
                possibility = (1/(energy + distance)) ** beta * pheromone[current_sensor][next_sensor][energy] ** alpha
                probabilities.append([(next_sensor,energy),possibility])

        if len(probabilities) == 0:
            return False

        if random() < q0:
            ans = max(probabilities, key = lambda x: x[1])
        else:
            selectedIndex = self.chose_element(probabilities)
            ans = probabilities[selectedIndex]

        next_sensor = ans[0]
        self.visited.add(next_sensor[0])

        path_to_next_sensor = [(cell[0], cell[1], 0) for cell in self.map.paths[current_sensor][next_sensor[0]]]
        self.path.extend(path_to_next_sensor)
        self.path[-1] = (self.path[-1][0],self.path[-1][1],next_sensor[1])
        #print(self.path)


        self.path_of_sensors.append(next_sensor)
        self.battery -= len(path_to_next_sensor) + next_sensor[1]

        return True

    def chose_element(self, probabilities):
        pSum = sum([element[1] for element in probabilities])
        ansVector = [(element[1]/pSum) for element in probabilities]
        r = random()
        index = 0
        current_sum = ansVector[0]
        while r > current_sum and index+1 < len(ansVector):
            index += 1
            current_sum += ansVector[index]
        return index