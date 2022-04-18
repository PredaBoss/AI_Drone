from enum import Enum


class Directions(Enum):
    UP = 0
    DOWN = 2
    LEFT = 1
    RIGHT = 3
    v = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    Opposite = {0:1, 1:0, 2:3, 3:2}
    mapLengh = 20