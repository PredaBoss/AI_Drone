import statistics
from copy import deepcopy

from Domain.Individual import Individual
from Repository import *


class Controller():
    def __init__(self, repository):
        self.repository = repository

    def iteration(self, mutation_probability, crossover_probability):

        parent1, parent2 = self.repository.population.selection()
        offspring1, offspring2 = Individual.crossover(self.repository.map, parent1, parent2,crossover_probability)

        offspring1.mutate(mutation_probability)
        offspring2.mutate(mutation_probability)

        offspring1.update_fitness()
        offspring2.update_fitness()

        self.repository.population.selectSurvivors(offspring1, offspring2)


    def run(self,number_of_runs, mutation_probability, crossover_probability):
        fitness_list_avg = []
        best_solution = None

        for _ in range(number_of_runs):
            self.iteration(mutation_probability,crossover_probability)
            fitness_list_avg.append(statistics.mean([individual.fitness for individual in self.repository.population.population]))

        for individual in self.repository.population.population:
            if best_solution is None or best_solution.fitness < individual.fitness:
                best_solution = deepcopy(individual)

        path = best_solution.get_path()
        return path, fitness_list_avg, best_solution.fitness


    def solver(self, population_size, individual_size, number_of_runs, battery, going_back, mutation_probability,
               crossover_probability):
        self.repository.createPopulation(battery, population_size, individual_size, going_back)
        return self.run(number_of_runs, mutation_probability, crossover_probability)
