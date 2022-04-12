import statistics
import time
from matplotlib import pyplot
from random import seed

from Repository.Repository import Repository
from Controller.Controller import Controller
from View.Gui import Gui


class Ui:
    def __init__(self):
        repository = Repository()
        self.controller = Controller(repository)
        self.gui = Gui()
        self.loaded_map = False
        self.parameters_setup = False
        self.program_solved = False
        self.population_size = None
        self.individual_size = None
        self.number_of_runs = None
        self.battery = None
        self.going_back = None
        self.path = None
        self.fitness_avg = None
        self.mutation_probability = None
        self.crossover_probability = None
        self.speed = None

    def run(self):
        while True:
            print("1. Map Options")
            print("2. Evolutionary algorithm options")
            print("0. Exit")
            options_choice = input("Your option: ")

            if options_choice == "1":
                print("Map Options:\n")
                print("1. Create a random map")
                print("2. Load a map")
                print("3. Save a map")
                print("4. Visualise map")
                map_option = input("> ")

                if map_option == "1":
                    self.loaded_map = True
                    fill = input("Fill factor (enter=0.2)= ")
                    if len(fill) != 0:
                        fill = float(fill)
                    else:
                        fill = 0.2
                    self.controller.repository.load_random_map(fill)

                elif map_option == "2":
                    self.loaded_map = True
                    self.controller.repository.load_map()

                elif map_option == "3":
                    if self.loaded_map:
                        self.controller.repository.save_map()
                    else:
                        print("The map was not loaded yet")
                elif map_option == "4":
                    if self.loaded_map:
                        self.gui.just_the_drone(self.controller.repository.map,(self.controller.repository.map.n, self.controller.repository.map.m))
                    else:
                        print("The map was not loaded yet")
                else:
                    print("Incorrect map option!")

            elif options_choice == "2":
                if not self.loaded_map:
                    print("Map not yet loaded")
                    continue

                print("1. Parameters setup")
                print("2. Run the solver once")
                print("3. Run the solver many times and compute mean and standard deviation")
                print("4. Visualise the statistics")
                print("5. View the drone on a path")
                algorithm_option = input("> ")

                if algorithm_option == "1":
                    self.parameters_setup = True
                    self.program_solved = False
                    self.battery = input("Battery (enter=30)= ")
                    if len(self.battery) != 0:
                        self.battery = int(self.battery)
                    else:
                        self.battery = 30

                    self.going_back = input("Going back (y/n)=")
                    self.going_back = self.going_back == "y"

                    self.population_size = input("Population size (enter=100)= ")
                    if len(self.population_size) != 0:
                        self.population_size = int(self.population_size)
                    else:
                        self.population_size = 100

                    self.individual_size = input(f"Individual size (enter={self.battery*2})= ")
                    if len(self.individual_size) != 0:
                        self.individual_size = int(self.individual_size)
                    else:
                        self.individual_size = self.battery*2

                    self.number_of_runs = input("Number of runs (enter=10000)= ")
                    if len(self.number_of_runs) != 0:
                        self.number_of_runs = int(self.number_of_runs)
                    else:
                        self.number_of_runs = 10000

                    self.mutation_probability = input("Probability of mutation (enter=0.05)= ")
                    if len(self.mutation_probability) != 0:
                        self.mutation_probability = int(self.mutation_probability)
                    else:
                        self.mutation_probability = 0.05

                    self.crossover_probability = input("Probability of crossover (enter=0.8)= ")
                    if len(self.crossover_probability) != 0:
                        self.crossover_probability = float(self.crossover_probability)
                    else:
                        self.crossover_probability = 0.8

                    self.speed = input("Speed of drone in seconds per move (enter=0.5)= ")
                    if len(self.speed) != 0:
                        self.speed = float(self.speed)
                    else:
                        self.speed = 0.5

                elif algorithm_option == "2":
                    if not self.parameters_setup:
                        print("The parameters are not set up")
                        continue
                    if self.program_solved:
                        print("Program already solved")
                        continue
                    start = time.time()
                    self.path, self.fitness_avg, self.solution_fitness = self.controller.solver(self.population_size,self.individual_size,self.number_of_runs,self.battery,self.going_back,self.mutation_probability,self.crossover_probability)
                    end = time.time()
                    print("Evolutionary algorithm:",end-start)
                    print("Moves:",len(self.path)-1)
                    nr_cells = self.solution_fitness
                    if self.path[0] == self.path[-1]:
                        nr_cells = self.solution_fitness-100
                    print("Discovered cells",nr_cells)
                    self.program_solved = True

                elif algorithm_option == "3":
                    if not self.parameters_setup:
                        print("The parameters are not set up")
                        continue
                    values = []
                    for i in range(30):
                        seed(i)
                        _,_,fitness = self.controller.solver(self.population_size,self.individual_size,self.number_of_runs,self.battery,self.going_back,self.mutation_probability,self.crossover_probability)
                        values.append(fitness)
                    avg = statistics.mean(values)
                    stdev = statistics.stdev(values)
                    print(f"Average solution fitness was found to be {avg} and it has a stdev of {stdev}")
                    pyplot.plot(values)
                    pyplot.ylim([0, None])
                    pyplot.savefig("plot.png")
                    pyplot.close()

                elif algorithm_option == "4":
                    if not self.program_solved:
                        print("Program was not solved yet")
                        continue
                    pyplot.plot(self.fitness_avg)
                    pyplot.savefig("fitness.png")
                    pyplot.close()

                elif algorithm_option == "5":
                    self.gui.movingDrone(self.controller.repository.map,self.path,self.speed)

                else:
                    print("Incorrect choice")

            elif options_choice == "0":
                break
            else:
                print("Incorrect choice")