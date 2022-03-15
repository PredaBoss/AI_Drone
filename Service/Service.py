import queue
from math import sqrt


class Service:
    def __init__(self):
        self.dx = [1,-1,0,0]
        self.dy = [0,0,1,-1]

    def verify_pos(self, pos):
        if pos[0] <0 or pos[0]>400 or pos[1]<0 or pos[1]>400:
            return None
        return (int(pos[1]/20),int(pos[0]/20))

    def searchAStar(self,mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        start = (initialX, initialY)
        end = (finalX, finalY)
        found, parent = self.bfs(mapM, start, end, lambda current: self.euclideanDistance(current, end) + self.euclideanDistance(start,current))
        if not found:
            return []

        path = []
        cell = end
        while cell != -1:
            path.append(cell)
            cell = parent[cell]

        path.reverse()
        return path

    def searchGreedy(self,mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        start = (initialX, initialY)
        end = (finalX,finalY)
        found, parent = self.bfs(mapM,start,end,lambda current: self.euclideanDistance(current, end))
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
        found = False
        visited = set()
        toVisit = queue.PriorityQueue()
        toVisit.put((priorityFunction(start), start))
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
                toVisit.put((priorityFunction(child),child))
                parent[child] = node
        return found, parent

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
