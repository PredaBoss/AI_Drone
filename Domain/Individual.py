from copy import deepcopy
from queue import Queue
from random import random, randrange, randint

from Utils.Directions import Directions


class Individual:
    def __init__(self, drone_map, battery, size=0, chromosome=None, go_back=False):
        self.drone_map =drone_map
        if chromosome is None:
            chromosome = [randrange(0,4) for _ in range(size)]
        self.chromosome = chromosome
        self.battery = battery
        self.fitness = None
        self.go_back = go_back

    def path_of_chromosome(self):
        drone = [self.drone_map.x, self.drone_map.y]
        bfs_distances = None
        prev = None
        if self.go_back:
            bfs_distances = [[None for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
            prev = [[None for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
            position = (drone[0],drone[1])
            bfs_distances[drone[0]][drone[1]] = 0
            queue = Queue()
            queue.put(position)
            while not queue.empty():
                current_position = queue.get()
                for i in range(len(Directions.v.value)):
                    new_position = (current_position[0] + Directions.v.value[i][0], current_position[1] + Directions.v.value[i][1])
                    if 0 <= new_position[0] < self.drone_map.n and 0 <= new_position[1] < self.drone_map.m:
                        if self.drone_map.surface[new_position[0]][new_position[1]] == 0:
                            if bfs_distances[new_position[0]][new_position[1]] is None:
                                queue.put(new_position)
                                bfs_distances[new_position[0]][new_position[1]] = bfs_distances[current_position[0]][current_position[1]]+1
                                prev[new_position[0]][new_position[1]] = Directions.Opposite.value[i]

        path = [drone]
        going_back = False
        if self.go_back and self.battery <= 1:
            going_back = True

        for i in range(len(self.chromosome)):
            if going_back:
                if prev[drone[0]][drone[1]] is None:
                    break
                new_drone = [drone[0] + Directions.v.value[prev[drone[0]][drone[1]]][0],
                             drone[1] + Directions.v.value[prev[drone[0]][drone[1]]][1]]
            else:
                new_drone = [drone[0]+ Directions.v.value[self.chromosome[i]][0], drone[1] + Directions.v.value[self.chromosome[i]][1]]

            if 0 <= new_drone[0] < self.drone_map.n and 0 <= new_drone[1] < self.drone_map.m:
                if self.drone_map.surface[new_drone[0]][new_drone[1]] != 1:
                    if self.battery >= len(path):
                        drone = new_drone
                        path.append(drone)
                        if self.go_back and len(path) + bfs_distances[drone[0]][drone[1]] >= self.battery:
                            going_back = True
        return path


    def update_fitness(self):
        path = self.path_of_chromosome()
        marked = [[0 for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
        for position in path:
            marked[position[0]][position[1]] = 1
            for direction in Directions.v.value:
                sight = deepcopy(position)
                while True:
                    sight[0] += direction[0]
                    sight[1] += direction[1]

                    valid = False
                    if 0 <= sight[0] < self.drone_map.n and 0 <= sight[1] < self.drone_map.m:
                        if self.drone_map.surface[sight[0]][sight[1]] != 1:
                            valid = True
                    if not valid:
                        break

                    marked[sight[0]][sight[1]] = 1

        self.fitness = sum([sum(row) for row in marked])

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
        size =  len(firstParent.chromosome)
        if random() < crossoverProbability:
            cutting_point = randint(0,size)
            offspring1 = Individual(drone_map, firstParent.battery, chromosome=[
                firstParent.chromosome[i] if i < cutting_point else otherParent.chromosome[i] for i in range(size)], go_back=firstParent.go_back)
            offspring2 = Individual(drone_map, firstParent.battery, chromosome=[
                otherParent.chromosome[i] if i < cutting_point else firstParent.chromosome[i] for i in range(size)], go_back=firstParent.go_back)

        else:
            offspring1 = Individual(drone_map,firstParent.battery, size, go_back=firstParent.go_back)
            offspring2 = Individual(drone_map,firstParent.battery, size, go_back=firstParent.go_back)

        return offspring1, offspring2