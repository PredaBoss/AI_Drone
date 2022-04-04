from random import sample

from Domain.Individual import Individual


class Population():
    def __init__(self, drone_map, battery=10, populationSize=10, individualSize=10, going_back = False, population = None):
        self.__populationSize = populationSize
        if population is None:
            population = [Individual(drone_map, battery, individualSize, go_back = going_back) for _ in range(populationSize)]

        self.population = population
        self.evaluate()
    def evaluate(self):
        # evaluates the population
        for x in self.population:
            x.update_fitness()

    def selection(self, k=2):
        # perform a selection of k individuals from the population
        # and returns that selection
        return sorted(sample(self.population,k), key=lambda x: x.fitness, reverse=True )[0]