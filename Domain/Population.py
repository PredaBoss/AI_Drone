from random import sample, random

from Domain.Individual import Individual


class Population():
    def __init__(self, drone_map, battery=10, populationSize=10, individualSize=10, going_back = False, population = None):
        self.population = [Individual(drone_map, battery, individualSize, go_back = going_back) for _ in range(populationSize)]
        self.__populationSize = populationSize
        self.evaluate()

    def evaluate(self):
        # evaluates the population
        for x in self.population:
            x.update_fitness()

    def selectSurvivors(self, offspring1, offspring2):

        worstIndividual = None
        secondWorstIndividual = None
        worstIndex = None
        secondWorstIndex = None
        counter = 0

        for individual in self.population:
            if worstIndividual is None or individual.fitness < worstIndividual.fitness:
                secondWorstIndividual = worstIndividual
                secondWorstIndex = worstIndex
                worstIndividual = individual
                worstIndex = counter

            elif secondWorstIndividual is None or individual.fitness < secondWorstIndividual.fitness:
                secondWorstIndividual = individual
                secondWorstIndex = counter

            counter+=1

        (worstOffspring, secondWorstOffspring) = (offspring1, offspring2) if offspring1.fitness < offspring2.fitness else (offspring2, offspring1)

        if secondWorstIndividual.fitness < secondWorstOffspring.fitness and worstIndividual.fitness < worstOffspring.fitness:
            self.population[worstIndex] = worstOffspring
            self.population[secondWorstIndex] = secondWorstOffspring
        elif secondWorstIndividual.fitness < worstOffspring.fitness and worstIndividual.fitness > worstOffspring.fitness:
            self.population[worstIndex] = secondWorstOffspring

    def selection(self, k=2):
        # perform a selection of k individuals from the population
        # and returns that selection
        population = sorted(self.population, key=lambda x: random() * x.fitness, reverse=True)
        return self.population[0], self.population[1]
        # possibleCases = (self.__populationSize) * (self.__populationSize + 1) / 2
        # probability = [(i+1)/possibleCases for i in range(self.__populationSize)]
        #
        # firstIndex = self.get_random_individual(probability)
        # secondIndex = self.get_random_individual(probability)
        #
        # while secondIndex == firstIndex:
        #     secondIndex = self.get_random_individual(probability)
        #
        # return population[firstIndex], population[secondIndex]

    def get_random_individual(self,probability):
        random_probability = random()
        counter = 0
        for index in range(self.__populationSize):
            counter += probability[index]
            if counter >= random_probability:
                return index
        return self.__populationSize-1

