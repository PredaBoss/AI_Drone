from random import randint

import pygame
import time

from Constants.Colors import Colors
from Board.Map import Map
from Drone.Drone import Drone


class Gui:
    def __init__(self, map):

        # we create the map
        self.m = map
        self.m.loadMap("test1.map")

        # we position the drone somewhere in the area
        self.d = Drone(randint(0, 19), randint(0, 19))


    def start_game(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)

        pygame.display.set_caption("Choose a sleep time for the drone")
        start_screen = pygame.display.set_mode((400, 200))

        width = start_screen.get_width()
        height = start_screen.get_height()

        smallfont = pygame.font.SysFont('Corbel', 35)
        text1 = smallfont.render('1.00', True, Colors.WHITE.value)
        text2 = smallfont.render('2.00', True, Colors.WHITE.value)
        text3 = smallfont.render('5.00', True, Colors.WHITE.value)

        button_width = (width-40)//3
        button_height = height//3

        while True:
            start_screen.fill(Colors.WHITE.value)

            pygame.draw.rect(start_screen,Colors.BLUE.value,[10,height//4,button_width,button_height])
            pygame.draw.rect(start_screen,Colors.BLUE.value,[20+button_width,height//4,button_width,button_height])
            pygame.draw.rect(start_screen,Colors.BLUE.value,[30+2*button_width,height//4,button_width,button_height])

            start_screen.blit(text1, (42, 65))
            start_screen.blit(text2, (52+button_width, 65))
            start_screen.blit(text3, (62+2*button_width, 65))

            pygame.display.update()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 10 <= mouse[0] <= 10+button_width and height //4 <= mouse[1] <= height//4 + button_height:
                        self.run_game(1.0)
                        return
                    if 20+button_width <= mouse[0] <= 20+2*button_width and height //4 <= mouse[1] <= height//4 + button_height:
                        self.run_game(2.0)
                        return
                    if 30+button_width <= mouse[0] <= 30+3*button_width and height //4 <= mouse[1] <= height//4 + button_height:
                        self.run_game(5.0)
                        return

    def run_game(self,delay):
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(Colors.WHITE.value)

        # define a variable to control the main loop
        running = True
        counter = 0
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    running = False

            screen.blit(self.d.mapWithDrone(self.m.image()), (0, 0))
            pygame.display.flip()

        path = self.dummysearch()
        screen.blit(self.displayWithPath(self.m.image(), path), (0, 0))
        pygame.display.flip()
        time.sleep(delay)

        pygame.quit()

    def searchAStar(self,mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]

        pass

    def searchGreedy(self,mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        pass

    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    def displayWithPath(self,image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(Colors.GREEN.value)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    def end_game(self, counter):
        time.sleep(1)

        end_screen = pygame.display.set_mode((600, 200))
        pygame.display.set_caption('End of the game')

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("The game has ended! You made {0} steps.".format(counter)
                           , True, Colors.BLUE.value, Colors.WHITE.value)

        textRect = text.get_rect()
        textRect.center = (300, 100)

        while True:
            end_screen.fill(Colors.WHITE.value)
            end_screen.blit(text, textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                pygame.display.update()