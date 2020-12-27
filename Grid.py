import pygame

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
        self.walls = [False, False, False, False]  # top, right, bottom, left
        self.paths = []

    def get_pos(self):
        return self.row, self.col

    def make_walls(self, walls):
        if walls:
            self.walls = [True, True, True, True]

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

    def is_visited(self):
        return self.visited

    def is_wall(self, pos):
        return self.walls[pos]

    def remove_wall(self, pos):
        self.walls[pos] = False

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_visited(self):
        self.visited = True

    def make_unvisited(self):
        self.visited = False

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = BLUE

    def highlight(self):
        self.color = GREEN

    def draw(self, win):
        """
        Draws node onto screen
        :param win: screen used
        :return: None
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def check_walls(self):
        """
        :return: Walls around given node
        """
        return self.walls

    def update_paths(self, grid):
        """
        Get possible pathways from a given node, does not matter if visited or not visited (used for some maze
        Generation algorithms)
        :param grid: Grid being used
        :return:
        """
        self.paths = []
        if self.row < self.total_rows - 1:  # DOWN
            self.paths.append(grid[self.row + 1][self.col])

        if self.row > 0:  # UP
            self.paths.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1:  # RIGHT
            self.paths.append(grid[self.row][self.col + 1])

        if self.col > 0:  # LEFT
            self.paths.append(grid[self.row][self.col - 1])

    def update_neighbors(self, grid):
        """
        Get Non-visited neighbors of a given node
        :param grid: Grid being used
        :return: Non-visited neighbors
        """
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_visited():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_visited():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_visited():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_visited():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def visited_neighbors(self, grid):
        """
        Get the visited neighbors of a given node
        :param grid: Grid being used
        :return: Visited Neighbors
        """
        self.neighbors = []
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_visited():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and grid[self.row - 1][self.col].is_visited():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_visited():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and grid[self.row][self.col - 1].is_visited():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        return self.neighbors

    def get_neighbors(self):
        """Returns neighbors of Node"""
        return self.neighbors

    def __lt__(self, other):
        return False


def make_grid(rows, width, barrier=True):
    """
    Generates the grid to be used
    :param rows: Rows in grid
    :param width: Width of grid/win
    :param barrier: Default True: Only false if maze not being generated
    :return:
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if barrier:
                node.make_barrier()
                node.make_walls(True)

            # create border
            # if i == 0 or i == rows-1 or j == 0 or j == rows-1:
            #     node.make_barrier()

            # node.make_barrier()

            grid[i].append(node)

    return grid


def remove_walls(a, b):
    """
    Removes wall between two nodes
    :param a: Node 1
    :param b: Node 2
    :return: None
    """
    x = b.x - a.x
    if x > 0:
        a.remove_wall(1)
        b.remove_wall(3)
    if x < 0:
        a.remove_wall(3)
        b.remove_wall(1)

    y = b.y - a.y
    if y > 0:
        a.remove_wall(2)
        b.remove_wall(0)
    if y < 0:
        a.remove_wall(0)
        b.remove_wall(2)


def wall_between(a, b):
    """
    Checks if there is a wall in between node a and node b
    :param a: Node 1
    :param b: Node 2
    :return: True if wall between the nodes, else false.
    """
    if a.x > b.x:  # RIGHT
        if a.is_wall(3):
            return True

    elif a.x < b.x:  # LEFT
        if a.is_wall(1):
            return True

    if a.y > b.y:  # UP
        if a.is_wall(0):
            return True

    elif a.y < b.y:  # DOWN
        if a.is_wall(2):
            return True

    return False


def draw_grid(win, rows, width):
    """
    Function which draws grid onto screen. Only used if a maze is not generated
    :param win: Window to draw on
    :param rows: Rows in grid
    :param width: Width of win
    :return: None
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, color=BLACK):
    """
    Draws each node/animation onto the grid
    :param win: Window to draw on
    :param grid: Grid to draw on
    :param rows: Rows in Grid
    :param width: Width of Grid
    :param color: Default Black, only white when no maze is being generated (user creates own barriers etc)
    :return:  None
    """
    win.fill(color)

    for row in grid:
        for node in row:
            node.draw(win)

    if color != BLACK:
        draw_grid(win, rows, width)
    else:
        draw_walls(win, grid, rows, width)
    pygame.display.update()


def draw_walls(win, grid, rows, width):
    """
    Draws walls for each Node
    :param win: Window to draw on
    :param grid: Grid to draw on
    :param rows: Rows in Grid
    :param width: Width of Grid
    :return: None
    """
    for row in grid:
        for node in row:
            if node.walls[0]:  # top
                pygame.draw.rect(win, BLACK, (node.x, node.y, node.width, (node.width / WALL_WIDTH)))
            if node.walls[1]:  # right
                pygame.draw.rect(win, BLACK, (node.x + node.width, node.y, (node.width // WALL_WIDTH), node.width))
            if node.walls[2]:  # bot
                pygame.draw.rect(win, BLACK, (
                    node.x, node.y + node.width, node.width + (node.width // WALL_WIDTH), (node.width // WALL_WIDTH)))
            if node.walls[3]:  # left
                pygame.draw.rect(win, BLACK, (node.x, node.y, (node.width // WALL_WIDTH), node.width))


def get_clicked_pos(pos, rows, width):
    """
    Gets clicked Position
    :param pos: Position clicked on grid
    :param rows: Rows in grid
    :param width: Width of window
    :return: Clicked position
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
