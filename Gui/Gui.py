from random import randint

import pygame
import time

from Constants.Colors import Colors
from Board.DMap import DMap
from Drone.Drone import Drone


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

        pygame.display.set_caption("Choose a sleep time for the drone")
        start_screen = pygame.display.set_mode((400, 200))

        width = start_screen.get_width()
        height = start_screen.get_height()

        smallfont = pygame.font.SysFont('Corbel', 35)
        text1 = smallfont.render('0.01', True, Colors.WHITE.value)
        text2 = smallfont.render('0.10', True, Colors.WHITE.value)
        text3 = smallfont.render('1.00', True, Colors.WHITE.value)

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
                        self.run_game(0.01)
                        return
                    if 20+button_width <= mouse[0] <= 20+2*button_width and height //4 <= mouse[1] <= height//4 + button_height:
                        self.run_game(0.1)
                        return
                    if 30+button_width <= mouse[0] <= 30+3*button_width and height //4 <= mouse[1] <= height//4 + button_height:
                        self.run_game(1.0)
                        return

    def run_game(self,delay):
        pygame.display.set_caption("drone exploration")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(Colors.WHITE.value)
        screen.blit(self.e.image(), (0, 0))

        self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
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

            time.sleep(delay)
            response = self.d.moveDSF(self.m)
            if response == -1:
                self.end_game(counter)
                return
            counter = counter+1

            self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
            screen.blit(self.m.image(self.d.x, self.d.y), (400, 0))
            pygame.display.flip()

        pygame.quit()

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