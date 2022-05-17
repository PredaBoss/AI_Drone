from copy import deepcopy

from Domain.Ant import Ant
from Utils.Constants import Constants


class Controller():
    def __init__(self, map):
        self.map = map
        self.ants = Constants.ants.value
        self.alpha = Constants.alpha.value
        self.beta = Constants.beta.value
        self.rho = Constants.rho.value
        self.q0 = Constants.q0.value

        self.pheromone = []
        for i in range(self.ants):
            cost_list = []
            for j in range(self.ants):
                if i == j :
                    cost_list.append([0 for _ in range(6)])
                    continue
                cost_list.append([1 for _ in range(6)])
            self.pheromone.append(cost_list)

        self.initial_pheromone = deepcopy(self.pheromone)

    def iteration(self):
        colony = [Ant(self.map) for _ in range(self.ants)]

        found_next = [True for _ in range(self.ants)]
        something_found = True
        while something_found:
            something_found = False
            for i in range(self.ants):
                if found_next[i]:
                    found_next[i] = colony[i].move(self.pheromone, self.alpha, self.beta, self.q0)
                    something_found = something_found or found_next[i]

        self.update_pheromone()

        for ant in colony:
            for i in range(len(ant.path_of_sensors) - 1):
                current_sensor = ant.path_of_sensors[i]
                next_sensor = ant.path_of_sensors[i+1]
                self.pheromone[current_sensor[0]][next_sensor[0]][next_sensor[1]] += 1/ (len(ant.path_of_sensors)-1)

        ant = colony[max([(colony[i].efficiency(), i) for i in range(self.ants)])[1]]
        return ant

    def update_pheromone(self):

        for i in range(self.map.nr_of_sensors):
            for j in range(self.map.nr_of_sensors):
                if i == j:
                    continue
                for energy in range(1,6):
                    self.pheromone[i][j][energy] = (1-self.rho) * self.pheromone[i][j][energy] + \
                                                    self.rho * self.initial_pheromone[i][j][energy]
