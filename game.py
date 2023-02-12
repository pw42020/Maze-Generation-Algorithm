import pygame
from random import randint
from cube import Cube


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Random Maze Generation")
        self.clock = pygame.time.Clock()
        self.size = 20
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # creating WIDTH/size by HEIGHT/size grid 
        self.grid = [[i for i in range(self.WIDTH//self.size)] for j in range(self.HEIGHT//self.size)]

        # starting position for flags
        self.sflag = (0, 0)
        self.fflag = ((len(self.grid) - 1)*self.size, (len(self.grid) - 1)*self.size) 
        
        
    def eller(self):
        for j, row in enumerate(self.grid):
            for i in range(len(row)):
                # code that makes the blue then black animation when generating
                if i == (len(self.grid) - 1):
                    pygame.draw.rect(self.window, self.BLACK, (i*self.size, j*self.size, self.size, self.size))
                    pygame.draw.rect(self.window, self.BLUE, (0,(j+1)*self.size, self.size, self.size))
                else:
                    pygame.draw.rect(self.window, self.BLACK, (i*self.size, j*self.size, self.size, self.size))
                    pygame.draw.rect(self.window, self.BLUE, ((i+1)*self.size, j*self.size, self.size, self.size))
            if j != 0:
                maxcount = max(self.grid[j - 1]) + 1
                # horizontal rows
                for i in range(len(row)):
                    self.clock.tick(180)
                    connect = randint(0, 1)
                    if connect:
                        row[i] = self.grid[j - 1][i]
                    else:
                        pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, self.size, 1))
                        row[i] = maxcount
                        maxcount += 1
                #print(maxcount, row)
                    pygame.display.update()
            # vertical rows
            for i in range(1, len(row)):
                connect = randint(0, 1)
                if connect:
                    oldval = row[i - 1]
                    newval = self.grid[j - 1][i]
                    # if top row is connected to bottom row then make all the numbers the same
                    if row[i] == self.grid[j - 1][i]:
                        row = [newval if row[k] == oldval else row[k] for k in range(len(row))]
                    else:
                        row[i] = row[i - 1]
                if not connect:
                    pygame.draw.rect(self.window, self.WHITE, (i*self.size, j*self.size, 1, self.size))
        pygame.draw.rect(self.window, self.BLACK, (i*self.size, j*self.size, self.size, self.size))
                


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
                self.eller()
                start = False
            self.window.blit(startimg, self.sflag)
            self.window.blit(finishimg, self.fflag)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    x, y = pos.x
                    

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