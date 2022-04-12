from copy import deepcopy
from queue import Queue
from random import random, randrange, randint

from Utils.Directions import Directions


class Individual:
    def __init__(self, drone_map, battery, size=0, chromosome=None, go_back=False):
        self.drone_map =drone_map
        if chromosome is None:
            chromosome = [randrange(0, 3) for _ in range(size)]
        self.chromosome = chromosome
        self.battery = battery
        self.fitness = None
        self.go_back = go_back

    def get_path(self):
        drone = [self.drone_map.x, self.drone_map.y]
        path = [drone]

        for i in range(len(self.chromosome)):
            new_drone = [drone[0] + Directions.v.value[self.chromosome[i]][0], drone[1] + Directions.v.value[self.chromosome[i]][1]]

            if 0 <= new_drone[0] < self.drone_map.n and 0 <= new_drone[1] < self.drone_map.m:
                if self.drone_map.surface[new_drone[0]][new_drone[1]] != 1:
                    if self.battery >= len(path):
                        drone = new_drone
                        path.append(drone)
        return path


    def update_fitness(self):
        path = self.get_path()
        marked = [[0 for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
        for position in path:
            marked[position[0]][position[1]] = 1
            for direction in Directions.v.value:
                sight = deepcopy(position)
                while True:
                    sight[0] += direction[0]
                    sight[1] += direction[1]

                    if 0 <= sight[0] < self.drone_map.n and 0 <= sight[1] < self.drone_map.m:
                        if self.drone_map.surface[sight[0]][sight[1]] != 1:
                            marked[sight[0]][sight[1]] = 1
                            continue
                    break

        self.fitness = sum([sum(row) for row in marked])
        if self.go_back and path[0] == path[-1]:
            self.fitness += 100

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability and len(self.chromosome) >= 2:
            i = 0
            j = 0
            while i == j:
                i = randrange(len(self.chromosome))
                j = randrange(len(self.chromosome))
            self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i]

    @staticmethod
    def crossover(drone_map, firstParent, otherParent, crossoverProbability=0.8):
        size = len(firstParent.chromosome)
        if random() < crossoverProbability:
            cutting_point = randint(0, size)
            offspring1 = Individual(drone_map, firstParent.battery, chromosome=[
                firstParent.chromosome[i] if i < cutting_point else otherParent.chromosome[i] for i in range(size)], go_back=firstParent.go_back)
            offspring2 = Individual(drone_map, firstParent.battery, chromosome=[
                otherParent.chromosome[i] if i < cutting_point else firstParent.chromosome[i] for i in range(size)], go_back=firstParent.go_back)

        else:
            offspring1 = Individual(drone_map,firstParent.battery, size, go_back=firstParent.go_back)
            offspring2 = Individual(drone_map,firstParent.battery, size, go_back=firstParent.go_back)

        return offspring1, offspring2