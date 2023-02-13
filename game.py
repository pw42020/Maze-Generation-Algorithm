import pygame
from random import randint
from cube import Cube
from PriorityQueue import PriorityQueue


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Random Maze Generation")
        self.clock = pygame.time.Clock()
        self.size = 30
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # creating WIDTH/size by HEIGHT/size grid 
        self.grid = [[i for i in range(self.WIDTH//self.size)] for j in range(self.HEIGHT//self.size)]

        # starting position for flags
        self.sflag = (0, 0)
        self.fflag = ((len(self.grid) - 1)*self.size, (len(self.grid) - 1)*self.size) 

    def genMaze(self):
        # pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, self.size, 1)) # horizontal row
        # pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, 1, self.size)) # vertical row

        for j in range(len(self.grid)):
            # horizontal walls:
            if j != 0:
                start, end = 0, 0
                maxcount = max(self.grid[j - 1]) + 1
                for i in range(len(self.grid[j])):
                    if self.grid[j - 1][start] != self.grid[j - 1][i]:
                        # randomly choosing at least one point the numbers have to connect
                        end = i
                        numconnects = randint(1, end - start + 1) # find number of connections (at least one)
                        lis = []
                        while len(lis) != numconnects:
                            connect = randint(start, end)
                            if connect not in lis:
                                lis.append(connect)
                        for k in lis:
                            self.grid[j][k] = self.grid[j - 1][k]
                # animation
                for i in range(len(self.grid[j])):
                    if self.grid[j][i] != self.grid[j - 1][i]:
                        pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, self.size, 1)) # horizontal row
                        self.grid[j][i] = maxcount
                        maxcount += 1
            print(self.grid[j])
            # vertical connection
            for i in range(1, len(self.grid[j])):
                connect = randint(0, 8)
                if connect:
                    if j > 0:
                        if self.grid[j][i] == self.grid[j - 1][i]: # already horizontal connection
                            self.makeValuesTheSame(self.grid[j][i], self.grid[j][i - 1], j)
                        else:
                            self.grid[j][i] = self.grid[j][i - 1]
                    else:
                        self.grid[j][i] = self.grid[j][i - 1]
                else:
                    pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, 1, self.size)) # vertical row
        # print('-------')
        # for row in self.grid:
        #     print(row)

        # debug code: printing numbers down
        # font = pygame.font.SysFont("arial black", 20)
        # TEXT_COL = (255, 255, 255)
        # for j, row in enumerate(self.grid):
        #     for i in range(len(row)):
        #         text = str(row[i])
        #         img = font.render(text, True, TEXT_COL)
        #         self.window.blit(img, (i*self.size, j*self.size))

    # recursive algorithm to make all the numbers the same if multiple columns are connected in a row
    def makeValuesTheSame(self, oldval, newval, j):
        doAgainAbove = False
        doAgainBelow = False
        if oldval == newval: # stopping hitting recursion limit
            return
        for i in range(len(self.grid[j])):
            if self.grid[j][i] == oldval:
                self.grid[j][i] = newval
            if j > 0:
                if self.grid[j - 1][i] == oldval:
                    doAgainAbove = True
            if j != len(self.grid) - 1:
                if self.grid[j + 1][i] == oldval:
                    doAgainBelow = True
        if doAgainAbove:
            self.makeValuesTheSame(oldval, newval, j - 1)
        if doAgainBelow:
            self.makeValuesTheSame(oldval, newval, j + 1)


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
                start = False
            self.window.blit(startimg, self.sflag)
            self.window.blit(finishimg, self.fflag)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    

            pygame.display.update()

    # returning a function of all neighbors if they can be accessed by the square of cordinate pos
    def neighbors(self, pos):
        lis = []
        checkCoords = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        for coord in checkCoords:
            if self.grid[coord[1]][coord[0]] == self.grid[pos[1]][pos[0]]:
                lis.append(coord)
        return lis

    def dijkstra(self):
        distance = 0
        cell = self.sflag
        queue = [Cube(self.neighbors(cell), distance + 1)]
        queue.sort().reverse()

        while len(queue)!= 0 and cell != self.fflag:
            
            coords = queue[0]


if __name__ == "__main__":
    game = Game()
    game.run()