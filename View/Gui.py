from random import randint

import pygame
import time
from pygame.constants import KEYDOWN

from Model.Colors import Colors
from Model.DMap import DMap
from Controller.Drone import Drone


class Gui:
    def __init__(self,environment):
        # we create the environment
        self.e = environment
        # print(str(e))

        # we create the map
        self.m = DMap()

        # we position the drone somewhere in the area
        self.d = Drone(randint(0, 19), randint(0, 19))


    def start_game(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(Colors.WHITE.value)
        screen.blit(self.e.image(), (0, 0))

        self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                    break
            time.sleep(0.1)
            response = self.d.moveDSF(self.m)
            if response == -1:
                time.sleep(1)
                print("End of the game!")
                break
            self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
            screen.blit(self.m.image(self.d.x, self.d.y), (400, 0))
            pygame.display.flip()

        pygame.quit()