from Board.Map import Map
from Gui.Gui import Gui

if __name__ == '__main__':
    map = Map()
    g = Gui(map)
    g.start_game()