from Model.Environment import Environment
from View.Gui import Gui

if __name__ == '__main__':
    environment = Environment()
    environment.loadEnvironment("test2.map")
    g = Gui(environment)
    g.start_game()