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
        self.used_in_has_unvisited = set()
        self.has_unv = {}
        self.dx = [1,-1,0,0]
        self.dy = [0,0,1,-1]

    def has_unvisited(self,x,y,detectedMap,used_in_has_unvisited = None):

        if used_in_has_unvisited is None:
            used_in_has_unvisited = set()
        used_in_has_unvisited.add((x,y))

        for i in range(4):
            if not self.used_in_has_unvisited.__contains__((x + self.dx[i], y + self.dy[i])):
                if x + self.dx[i] >= 0 and x + self.dx[i] <= 19 and y + self.dy[i] >= 0 and y + self.dy[i] <= 19:
                    if (not self.added.__contains__((x + self.dx[i],y + self.dy[i]))):
                        if detectedMap.surface[x + self.dx[i]][y + self.dy[i]] == -1:
                            return True
                        if detectedMap.surface[x + self.dx[i]][y + self.dy[i]] == 0:
                            if not used_in_has_unvisited.__contains__((x + self.dx[i],y + self.dy[i])):
                                if self.has_unvisited(x + self.dx[i],y + self.dy[i],detectedMap,used_in_has_unvisited):
                                    return True
        return False


    def add_in_stk(self, detectedMap):
        for i in range(4):
            if self.x + self.dx[i] >= 0 and self.x + self.dx[i] <= 19 and self.y + self.dy[i] >= 0 and self.y + self.dy[i] <= 19:
                if (not self.added.__contains__((self.x + self.dx[i],self.y + self.dy[i]))) and detectedMap.surface[self.x + self.dx[i]][self.y + self.dy[i]] == 0:
                    if self.has_unvisited(self.x + self.dx[i], self.y + self.dy[i], detectedMap):
                        self.stk.append((self.x,self.y))
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
        try:
            nxt = self.stk.pop()
            while not self.has_unvisited(nxt[0],nxt[1],detectedMap):
                nxt2 = self.stk.pop()
                if nxt2 != (self.x, self.y):
                    nxt = nxt2
                    break
                nxt = self.stk.pop()

            self.x, self.y = nxt
        except IndexError:
            self.x = None
            self.y = None
            return -1