import math
import pygame
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))   # <--- This line is to initialize the pygame window          
pygame.display.set_caption("A* path finder algorithm")  # <--- This line is to set the title of the pygame window
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE 
        self.neighbors = []
        self.width = width 
        self.total_rows = total_rows   

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
    
    def make_closed(self):
        self.color = RED 
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) # <--- This line is to draw the rectangle

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # <--- This line is to check if the spot below the selected spot is not a barrier
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # <--- This line is to check if the spot above the selected spot is not a barrier
            self.neighbors.append(grid[self.row -1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():# <--- This line is to check if the spot on the right of the selected spot is not a barrier
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col -1].is_barrier():# <--- This line is to check if the spot on the left of the selected spot is not a barrier
            self.neighbors.append(grid[self.row][self.col -1])

    def __lt__(self, other):
        return False    
        

def h(p1, p2):
        p1 = x1, y1
        p2 = x2, y2
        return abs(x1 - x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # <--- This line is to put the start spot in the open set
    come_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row} # <--- This line is to set the g score of all the spots to infinity
    g_score[start] = 0
    f_score = {spot : float("inf") for row in grid for spot in row} # <--- This line is to set the f score of all the spots to infinity
    f_score[start] = h(start.get_pos(), end.get_pos())

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows) 
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # <--- This line is to draw the horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # <--- This line is to draw the vertical lines

def draw(win, grid, rows, width):
    win.fill(WHITE) # <--- This line is to fill the background with white color

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update() # <--- This line is to update the pygame window

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)
    start = None
    end = None
    run = True
    started = False

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # <--- This line is to quit the pygame window
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # <--- This line is to get the left mouse button
                pos = pygame.mouse.get_pos() # <--- This line is to get the position of the mouse
                row, col = get_clicked_pos(pos, rows, width)# <--- This line is to get the row and column of the mouse
                spot = grid[row][col]# <--- This line is to get the spot of the mouse
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
                

            elif pygame.mouse.get_pressed()[2]: # <--- This line is to get the right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                        end = None   

            if event.type == pygame.KEYDOWN: # <--- This line is to get the key pressed
                if event.key == pygame.K_SPACE and not started: # <--- This line is to check if the key pressed is spacebar
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) # <--- This line is to update the neighbors of the spot
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end) # <--- This line is to call the algorithm function   
    pygame.quit() # <--- This line is to quit the pygame window

main(WIN, WIDTH)



