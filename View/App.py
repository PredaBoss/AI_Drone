from Controller.Controller import Controller
from Domain.Map import Map
from Utils.Constants import Constants
from View.Gui import Gui


class App:
    def __init__(self):
        self.battery = Constants.battery.value

        self.map = Map(Constants.mapLength.value, Constants.mapLength.value, self.battery)
        if Constants.randomMap.value:
            self.map.randomMap()
        else:
            self.map.loadMap()

        self.controller = Controller(self.map)
        self.gui = Gui()
        self.solution = None

    def run(self):
        for _ in range(Constants.nr_of_iterations.value):
            found_solution = self.controller.iteration()
            if self.solution is None or self.solution.efficiency() < found_solution.efficiency():
                self.solution = found_solution

        print("Discovered cells:", self.solution.efficiency())
        self.gui.movingDrone(self.map, self.solution.path)