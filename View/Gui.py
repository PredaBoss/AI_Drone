from random import randint

import pygame
import time

from Utils.Colors import Colors
from Utils.Directions import Directions


class Gui:
    def __init__(self):
        pass

    def initPyGame(self,dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(Colors.WHITE.value)
        return screen

    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()

    def movingDrone(self,currentMap, path, speed=1, markSeen=True):
        # animation of a drone on a path

        screen = self.initPyGame((currentMap.n * 20, currentMap.m * 20))

        drona = pygame.image.load("drona.png")
        for i in range(len(path)):
            screen.blit(self.image(currentMap), (0, 0))

            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(Colors.GREEN.value)
                for j in range(i + 1):
                    for var in Directions.v.value:
                        x = path[j][0]
                        y = path[j][1]
                        while ((0 <= x + var[0] < currentMap.n and
                                0 <= y + var[1] < currentMap.m) and
                               currentMap.surface[x + var[0]][y + var[1]] != 1):
                            x = x + var[0]
                            y = y + var[1]
                            screen.blit(brick, (y * 20, x * 20))

            screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
            pygame.display.flip()
            time.sleep(speed)
        self.closePyGame()

    def image(self,currentMap, colour=Colors.BLUE.value, background=Colors.WHITE.value):
        # creates the image of a map

        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if currentMap.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def just_the_drone(self,current_map, drone_position):
        screen = self.initPyGame((current_map.n * 20, current_map.m * 20))
        screen.blit(self.image(current_map), (0, 0))
        drone = pygame.image.load("drona.png")
        screen.blit(drone, (drone_position[1] * 20, drone_position[0] * 20))
        for _ in range(1000):
            pygame.display.flip()
        self.closePyGame()