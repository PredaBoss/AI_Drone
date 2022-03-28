import math
import queue
import random
from math import sqrt


class Service:
    def __init__(self):
        self.dx = [1,-1,0,0]
        self.dy = [0,0,1,-1]

    def verify_pos(self, pos):
        if pos[0] <0 or pos[0]>400 or pos[1]<0 or pos[1]>400:
            return None
        return (int(pos[1]/20),int(pos[0]/20))

    def searchAStar(self,mapM, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        start = (initialX, initialY)
        end = (finalX, finalY)
        found, parent = self.bfs(mapM, start, end, lambda current,distances: self.euclideanDistance(current, end) + distances[current[0]][current[1]])
        if not found:
            return []

        path = []
        cell = end
        while cell != -1:
            path.append(cell)
            cell = parent[cell]

        path.reverse()
        return path

    def searchGreedy(self,mapM, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        start = (initialX, initialY)
        end = (finalX,finalY)
        found, parent = self.bfs(mapM,start,end,lambda current,distances: self.euclideanDistance(current, end))
        if not found:
            return []

        path = []
        cell = end
        while cell!=-1:
            path.append(cell)
            cell = parent[cell]

        path.reverse()
        return path

    def bfs(self, mapM, start, end, priorityFunction):

        inf = mapM.n + mapM.m
        distances = [[inf for _ in range(mapM.m)] for _ in range(mapM.n) ]
        distances[start[0]][start[1]] = 0

        found = False
        visited = set()
        toVisit = queue.PriorityQueue()
        toVisit.put((priorityFunction(start,distances), start))
        parent = {start: -1}

        while (not toVisit.empty()) and (not found):
            node = toVisit.get(block=False)[1]

            if node in visited:
                continue
            visited.add(node)

            if node==end:
                found=True
                return found, parent

            for child in self.getNeighbors(mapM,node):
                if child in visited:
                    continue
                distances[child[0]][child[1]] = distances[node[0]][node[1]] + 1
                toVisit.put((priorityFunction(child,distances),child))
                parent[child] = node
        return found, parent

    def getSimulatedAnnealingAnswer(self,mapM, initialX, initialY, finalX, finalY):
        start = (initialX,initialY)
        end = (finalX,finalY)
        return self.simulatedAnnealing(mapM, start, end, 1000, lambda current: self.euclideanDistance(current,  end))

    def simulatedAnnealing(self, mapM, start, end, temperature, priorityFunction):
        where = start
        path = []
        k = 0
        while where != end:
            path.append(where)
            k = k+1
            current_temperature = temperature / k

            neighbours = self.getNeighbors(mapM, where)
            neighbor = neighbours[random.randint(0,len(neighbours)-1)]
            if priorityFunction(neighbor) < priorityFunction(where):
                where = neighbor
                continue

            r = random.uniform(0,1)
            probability = math.exp(-abs(priorityFunction(neighbor)-priorityFunction(where)) / current_temperature)
            if r < probability:
                where = neighbor

        path.append(end)
        return path


    def getNeighbors(self, mapM, node):
        neighbors = []
        for i in range(4):
            nx = node[0]+self.dx[i]
            ny = node[1]+self.dy[i]
            if nx<0 or ny<0 or nx>19 or ny>19:
                continue
            if mapM.surface[nx][ny] == 0:
                neighbors.append((nx,ny))
        return neighbors


    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]

    @staticmethod
    def euclideanDistance(x, y):
        return sqrt((y[0] - x[0]) * (y[0] - x[0]) + (y[1] - x[1]) * (y[1] - x[1]))
