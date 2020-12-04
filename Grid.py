import pygame
from queue import PriorityQueue, LifoQueue
import random

WIDTH = 750
WALL_WIDTH = 10
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # square window
pygame.display.set_caption("Maze Generation + Path Finding Algorithm Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False
        self.walls = [True, True, True, True]  # top, bottom, right, left

    def get_pos(self):  # returns pos of current node
        return self.row, self.col

    def is_closed(self):  # closes node for pathfinding
        return self.color == RED

    def is_open(self):  # opens node for pathfinding
        return self.color == GREEN

    def is_barrier(self):  # represents drawn barrier (not maze) -- might delete
        return self.color == BLACK

    def is_start(self):  # returns true if start node
        return self.color == ORANGE

    def is_end(self):  # true if end node
        return self.color == TURQUOISE

    def is_visited(self):
        return self.visited

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = BLUE

    def make_visited(self):  # marks a node as visited
        self.visited = True

    def highlight(self):
        self.color = GREEN

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_visited(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_visited(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_visited(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_visited(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])