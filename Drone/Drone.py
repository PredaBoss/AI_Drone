import time

import pygame
from pygame.constants import *


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stk = []
        self.added = set()
        self.added.add((self.x,self.y))
        self.dx = [1,-1,0,0]
        self.dy = [0,0,1,-1]

    def add_in_stk(self, detectedMap):
        for i in range(4):
            if self.x + self.dx[i] >= 0 and self.x + self.dx[i] <= 19 and self.y + self.dy[i] >= 0 and self.y + self.dy[i] <= 19:
                if (not self.added.__contains__((self.x + self.dx[i],self.y + self.dy[i]))) and detectedMap.surface[self.x + self.dx[i]][self.y + self.dy[i]] == 0:
                    self.stk.append((self.x + self.dx[i],self.y + self.dy[i]))
                    self.added.add((self.x + self.dx[i], self.y + self.dy[i]))

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def moveDSF(self, detectedMap):
        self.add_in_stk(detectedMap)
        if len(self.stk) == 0:
            self.x = None
            self.y = None
            return -1
        nxt = self.stk.pop()
        self.x = nxt[0]
        self.y = nxt[1]