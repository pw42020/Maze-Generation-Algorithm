import pygame
from random import randint
from cube import Cube
from PriorityQueue import PriorityQueue
import math


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Random Maze Generation")
        self.clock = pygame.time.Clock()
        self.size = 120
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # creating WIDTH/size by HEIGHT/size grid 
        self.grid = [[Cube((i,j), math.inf) for i in range(self.WIDTH//self.size)] for j in range(self.HEIGHT//self.size)]
        self.traverse = [[['0','0','0','0'] for i in range(self.WIDTH//self.size)] for j in range(self.HEIGHT//self.size)] # traversal grid for Dijkstra
        # left wall, right wall, up wall, down wall

        # starting position for flags
        self.sflag = (0, 0)
        self.fflag = ((len(self.grid) - 1), (len(self.grid) - 1)) 

    def genMaze(self):
        # pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, self.size, 1)) # horizontal row
        # pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, 1, self.size)) # vertical row

        for j in range(len(self.grid)):
            # horizontal walls:
            if j != 0:
                start, end = 0, 0
                maxcount = max([cube.value for cube in self.grid[j-1]]) + 1
                i = 0
                numDone = []
                for i in range(len(self.grid[j])):
                    if self.grid[j-1][i].value not in numDone or i == len(self.grid[j]) - 1:
                        numDone.append(self.grid[j-1][i].value)
                        if i != 0:
                            # randomly choosing at least one point the numbers have to connect
                            end = i - 1
                            numconnects = randint(1, end - start + 1) # find number of connections (at least one)
                            lis = []
                            while len(lis) != numconnects:
                                connect = randint(start, end)
                                if connect not in lis:
                                    lis.append(connect)
                            for k in lis:
                                self.grid[j][k].value = self.grid[j - 1][k].value
                            start = i
                    if i == len(self.grid[j]) - 1 and self.grid[j-1][i].value != self.grid[j-1][i-1].value:
                        self.grid[j][i].value = self.grid[j-1][i].value

                # animation
                for i in range(len(self.grid[j])):
                    if self.grid[j][i].value != self.grid[j - 1][i].value:
                        # setting traversal grid 
                        self.traverse[j][i] = ['1' if k == 2 else self.traverse[j][i][k] for k in range(len(self.traverse[j][i]))]
                        self.traverse[j - 1][i] = ['1' if k == 3 else self.traverse[j][i][k] for k in range(len(self.traverse[j][i]))]
                        pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, self.size, 1)) # horizontal row
                        self.grid[j][i].value = maxcount
                        maxcount += 1
            # vertical connection
            if j != len(self.grid) - 1:
                if j == 0: # need as initializer, all other items in every row should be initialized as -1
                    for k in range(self.WIDTH//self.size):
                        self.grid[j][k].value = k
                for i in range(1, len(self.grid[j])):
                    connect = randint(0, 1)
                    if connect:
                        if j > 0:
                            if self.grid[j][i].value == self.grid[j - 1][i].value: # already horizontal connection
                                self.makeValuesTheSame(self.grid[j][i].value, self.grid[j][i - 1].value, j)
                            else:
                                self.grid[j][i].value = self.grid[j][i - 1].value
                        else:
                            self.grid[j][i].value = self.grid[j][i - 1].value
                    else:
                        # setting traversal grid
                        self.traverse[j][i] = ['1' if k == 0 else self.traverse[j][i][k] for k in range(len(self.traverse[j][i]))]
                        self.traverse[j][i - 1] = ['1' if k == 1 else self.traverse[j][i][k] for k in range(len(self.traverse[j][i]))]
                        pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, 1, self.size)) # vertical row
            else:
                for i in range(1, len(self.grid[j])):
                    if self.grid[j][i] == self.grid[j - 1][i]: # already horizontal connection
                        self.makeValuesTheSame(self.grid[j][i], self.grid[j][i - 1], j)
                    else:
                        self.grid[j][i].value = self.grid[j][i - 1].value

    def makeValuesTheSame(self, oldval, newval, j):
        doAgainAbove = False
        doAgainBelow = False
        if oldval == newval: # stopping hitting recursion limit
            return
        for i in range(len(self.grid[j])):
            if self.grid[j][i].value == oldval:
                self.grid[j][i].value = newval
            if j > 0:
                if self.grid[j - 1][i].value == oldval:
                    doAgainAbove = True
            if j != len(self.grid) - 1:
                if self.grid[j + 1][i].value == oldval:
                    doAgainBelow = True
        if doAgainAbove:
            self.makeValuesTheSame(oldval, newval, j - 1)
        if doAgainBelow:
            self.makeValuesTheSame(oldval, newval, j + 1)

    # returning a function of all neighbors if they can be accessed by the square of cordinate pos
    def neighbors(self, pos):
        lis = []

        # if square to the right is not separated by a wall
        coords = (pos[0] + 1, pos[1])
        if pos[0] + 1 < len(self.grid):
            print(self.traverse[coords[1]][coords[0]], self.traverse[pos[1]][pos[0]])
        if pos[0] + 1 < len(self.grid) and self.traverse[coords[1]][coords[0]][0] ==  '0' and self.traverse[pos[1]][pos[0]][1] == '0':
            lis.append(coords)
        print(coords)
        # if square to the left is not separated by a wall
        coords = (pos[0] - 1, pos[1])
        if pos[0] - 1 < len(self.grid):
            print(self.traverse[coords[1]][coords[0]], self.traverse[pos[1]][pos[0]])
        if pos[0] - 1 >= 0 and self.traverse[coords[1]][coords[0]][1] ==  '0' and self.traverse[pos[1]][pos[0]][0] == '0':
            lis.append(coords)
        print(coords)
        # if square one down is not separated by a wall
        coords = (pos[0], pos[1] + 1)
        if pos[1] + 1 < len(self.grid):
            print(self.traverse[coords[1]][coords[0]], self.traverse[pos[1]][pos[0]])
        if pos[1] + 1 < len(self.grid) and self.traverse[coords[1]][coords[0]][2] ==  "0" and self.traverse[pos[1]][pos[0]][3] == "0":
            lis.append(coords)
        print(coords)
        # if square one up is not separated by a wall
        coords = (pos[0], pos[1] - 1)
        if pos[1] - 1 < len(self.grid):
            print(self.traverse[coords[1]][coords[0]], self.traverse[pos[1]][pos[0]])
        if pos[1] - 1 >= 0 and self.traverse[coords[1]][coords[0]][3] ==  "0" and self.traverse[pos[1]][pos[0]][2] == "0":
            lis.append(coords)
        print(coords)
        return lis

    def dijkstra(self):
        distance = 0
        cell = self.sflag
        pqlis = []
        for j, row in enumerate(self.grid):
            for i in range(len(row)):
                if (i, j) == self.sflag:
                    self.grid[j][i].distance = 0
                    pqlis.append(self.grid[j][i])
                else:    
                    pqlis.append(self.grid[j][i])
        pq = PriorityQueue()
        pq.buildHeap([(cube.distance, cube) for cube in pqlis])

        nextVert = (-1,-1)
        while not pq.isEmpty() and nextVert != self.fflag:
            
            currentVert = pq.delMin()
            neighbors = self.neighbors(currentVert.coords)
            print(neighbors)
            
            print('----')
            for nextVert in neighbors:
                cube = self.grid[nextVert[1]][nextVert[0]] #[::-1] reverses tuple
                newDist = currentVert.distance + 1
                # Taking a pause here
                # for future me: Currently just realized self.neighbors returns the coordinates required, but you would need to search for
                # them in pq unless you completely restructure how you've handled your grid and traverse class (likely make it all Cubes)
                if newDist < cube.distance:
                    cube.distance = newDist
                    cube.setPrevious(currentVert)
                    pq.decreaseKey(cube, newDist)
                
                if cube.coords == self.fflag:
                    print(cube.coords, self.fflag)
                    break
        print("Finished!")
        vert = self.grid[nextVert[1]][nextVert[0]]
        while vert.prev != None:
            i = vert.coords[0]
            j = vert.coords[1]
            print(i, j)

            pygame.draw.rect(self.window, self.BLUE, (i*self.size, j*self.size, self.size, self.size)) # vertical row
            vert = vert.prev
        
        pygame.draw.rect(self.window, self.BLUE, (self.sflag[0]*self.size, self.sflag[1]*self.size, self.size, self.size)) # vertical row


    def run(self):

        start = True
        self.window.fill("black")
        simg = pygame.image.load("images/start.png")
        fimg = pygame.image.load("images/finish.png")
        startimg = pygame.transform.scale(simg, (self.size, self.size))
        finishimg = pygame.transform.scale(fimg, (self.size, self.size))
        while True:
            self.clock.tick(60)

            if start:
                self.genMaze()
                self.dijkstra()
                start = False
            self.window.blit(startimg, (self.sflag[0]*self.size, self.sflag[1]*self.size))
            self.window.blit(finishimg, (self.fflag[0]*self.size, self.fflag[1]*self.size))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()