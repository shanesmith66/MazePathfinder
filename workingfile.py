import pygame
from queue import PriorityQueue, LifoQueue
import random

WIDTH = 750 + 6
WALL_WIDTH = 5
WIN = pygame.display.set_mode((WIDTH, WIDTH))
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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def check_walls(self):
        return self.walls

    def update_paths(self, grid):
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
        return self.neighbors

    def __lt__(self, other):
        return False


class Wall:
    def __init__(self, node):
        self.x = node.x
        self.y = node.y
        self.width = node.width
        self.height = node.height
        self.color = BLACK

    def draw_walls(self, grid, win):
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



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def run_astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    print("fscore[start] = ", f_score[start])
    start.update_paths(grid)

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for path in current.paths:

            # skip over pathways which contain walls
            if path.x > current.x:  # RIGHT
                if path.is_wall(3):
                    continue

            elif path.x < current.x:  # LEFT
                if path.is_wall(1):
                    continue

            if path.y > current.y:  # UP
                if path.is_wall(0):
                    continue

            elif path.y < current.y:  # DOWN
                if path.is_wall(2):
                    continue

            pygame.time.delay(20)

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[path]:
                came_from[path] = current
                g_score[path] = temp_g_score
                f_score[path] = temp_g_score + h(path.get_pos(), end.get_pos())
                if path not in open_set_hash:
                    count += 1
                    open_set.put((f_score[path], count, path))
                    open_set_hash.add(path)
                    path.make_open()

        if len(current.paths) == 0:
            print("No available paths")

        draw()

        if current != start:
            current.make_closed()

    return False


# function which generates the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            node.make_barrier()
            node.make_walls(True)

            # create border
            # if i == 0 or i == rows-1 or j == 0 or j == rows-1:
            #     node.make_barrier()

            # node.make_barrier()

            grid[i].append(node)

    return grid


def remove_walls(a, b):
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


# Create a list of all walls, and create a set for each cell, each containing just that one cell.
# For each wall, in some random order:
# If the cells divided by this wall belong to distinct sets:
# Remove the current wall.
# Join the sets of the formerly divided cells.

def kruskals(grid, draw, rows):
    all_walls = [wall for row in grid for wall in row]  # create list of "walls" (just cells)
    all_walls.extend([wall for row in grid for wall in row])
    all_cells = [{cell} for row in grid for cell in row]  # create list of sets of each cell
    random.shuffle(all_walls)
    for wall in all_walls:
        wall.update_paths(grid)
        for cell_set in all_cells:
            if wall in cell_set:
                wall_index = all_cells.index(cell_set)
        wall_set = all_cells[wall_index]
        neighbor = random.choice(wall.paths)
        if neighbor in wall_set:
            continue
        else:
            wall_set.add(neighbor)


        # for cell_set in all_cells:
        #     if wall in cell_set:
        #         neighbor_index = all_cells.index(cell_set)
        #         neighbor_set = all_cells[neighbor_index]

        wall.reset()
        neighbor.reset()
        remove_walls(wall, neighbor)
        draw()


    print(all_cells)


    # # all_walls = [wall for row in grid for wall in row]  # create list of "walls" (just cells)
    # # all_cells = [{cell} for row in grid for cell in row]  # create list of sets of each cell
    # # while len(all_walls) > 0 and len(all_cells) > 1:
    # #     edge = random.choice(all_walls)  # choose random cell from list of walls
    # #     edge_set = {edge}
    # #     edge_index = all_cells.index(edge_set)  # get the index of this cell from the list of sets of cells
    # #     edge.update_paths(grid)  # get the neighbors from randomly chosen sell (visited + nonvisited)
    # #     random.shuffle(edge.paths)
    # #     edge2 = None
    # #     for path in edge.paths:
    # #         if wall_between(path, edge):
    # #             edge2 = path
    # #
    # #    # edge2 = random.choice(edge.neighbors)  # choose neighbor randomly
    # #     if edge2:
    # #         if not all_cells[edge_index].issubset({edge2}):  # if the cells belong to distinct sets
    # #             edge.reset()  # reset them both, remove wall between them
    # #             edge2.reset()
    # #             remove_walls(edge2, edge)
    # #             new_set = all_cells[edge_index].union({edge2}) # merge the sets
    # #             all_walls.append(new_set)
    # #             edge2 = {edge2}
    # #             if edge2 in all_walls:
    # #                 all_walls.remove(edge2)
    # #             if edge_set in all_walls:
    # #                 all_walls.remove(edge_set)  # remove the cell from the set
    # #             draw()
    # # print("all cells = ", all_cells)
    #
    #
    #
    # walls_down = 0
    # total_cells = sum(len(row) for row in grid)
    # all_cells = [{cell} for row in grid for cell in row]  # create list of sets of each cell
    #
    # while walls_down < total_cells-1:
    #     current_set = random.sample(all_cells, 1)[0]
    #     curr = current_set.pop()
    #     current_set.add(curr)
    #     curr.update_neighbors(grid)
    #     neighbor = random.choice(curr.neighbors)
    #     neighbor_set = {neighbor}
    #     if neighbor:
    #         if wall_between(curr, neighbor):
    #             if neighbor_set in all_cells:
    #                 neighbor_set = all_cells[all_cells.index({neighbor})]
    #             if not neighbor_set.issubset(current_set):
    #                 new_set = current_set.union(neighbor_set)
    #                 all_cells.remove(current_set)
    #                 if neighbor_set in all_cells:
    #                     all_cells.remove(neighbor_set)
    #                 print("current set = ", current_set)
    #                 curr.reset()
    #                 neighbor.reset()
    #                 remove_walls(curr, neighbor)
    #                 all_cells.append(new_set)
    #                 walls_down += 1
    #    draw()



    # While (# Walls Down < Total # Cells - 1)
    #     Choose random cell current
    # Choose random neighbor of current that has a wall up between it and current
    # If such a neighbor exists
    # Find the labels of current and neighbor
    # If they are different, union them, knock down the wall, and add to # Walls Down



# Pick a random cell as the current cell and mark it as visited.
# While there are unvisited cells:
# Pick a random neighbour.
# If the chosen neighbour has not been visited:
#   Remove the wall between the current cell and the chosen neighbour.
#   Mark the chosen neighbour as visited.
# Make the chosen neighbour the current cell.

def aldous_broder(grid, draw, rows):
    curr = grid[random.randint(0, rows-1)][random.randint(0, rows-1)]
    unvisited_cells = [node for row in grid for node in row]
    curr.make_visited()
    curr.reset()
    unvisited_cells.remove(curr)
    while len(unvisited_cells) > 0:
        curr.update_paths(grid)
        curr.reset()
        curr.make_visited()
        neighbor = random.choice(curr.paths)
        if not neighbor.is_visited():
            neighbor.make_visited()
            neighbor.reset()
            remove_walls(curr, neighbor)
            unvisited_cells.remove(neighbor)
        curr = neighbor
        curr.highlight()
        pygame.time.delay(10)
        draw()




def prims(grid, draw, rows):
    curr = grid[random.randint(0, rows-1)][random.randint(0, rows-1)]
    curr.make_visited()
    curr.reset()
    wall_list = {neighbor for neighbor in curr.neighbors}
    while len(wall_list) > 0:
        cell = random.sample(wall_list, 1)[0]
        visited = cell.visited_neighbors(grid)
        cell.make_visited()
        cell.reset()
        wall_list.remove(cell)
        if len(visited) > 0:
            next = random.choice(visited)
            next.make_visited()
            next.reset()
            remove_walls(cell, next)
            if next in wall_list:
                wall_list.remove(next)

            cell.update_neighbors(grid)
            for neighbor in cell.neighbors:
                wall_list.add(neighbor)
        cell.highlight()
        draw()
        pygame.time.delay(20)
        cell.reset()




# Random DFS maze algorithm
def random_dfs(grid, draw):
    stack = LifoQueue()
    curr = grid[1][1]
    curr.highlight()
    curr.make_visited()
    stack.put(curr)

    while not stack.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr.reset()
        curr = stack.get()
        curr.highlight()
        curr.update_neighbors(grid)
        pygame.time.delay(20)
        if len(curr.neighbors) > 0:
            stack.put(curr)
            next = random.choice(curr.neighbors)
            remove_walls(curr, next)
            next.reset()
            next.make_visited()
            stack.put(next)
        draw()
    curr.reset()

    return grid


# function that draws the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


# draws each node onto the grid
def draw(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw(win)

    # draw_grid(win, rows, width)
    draw_walls(win, grid, rows, width)
    pygame.display.update()


def draw_walls(win, grid, rows, width):
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
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None
    end = None

    # start = grid[1][1]
    # start.make_start()
    # end = grid[ROWS-2][ROWS-2]
    # end.make_end()

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                # elif node != end and node != start:
                #     print("walls = ", node.walls)

                else:
                    print("Top Wall = {}, R Wall = {}, B Wall = {}, L Wall = {}, ".format(node.is_wall(0),
                                                                                          node.is_wall(1),
                                                                                          node.is_wall(2),
                                                                                          node.is_wall(3)))

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1 and not start and not end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    random_dfs(grid, lambda: draw(win, grid, ROWS, width))

                if event.key == pygame.K_2 and not start and not end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    prims(grid, lambda: draw(win, grid, ROWS, width), ROWS)

                if event.key == pygame.K_3 and not start and not end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    kruskals(grid, lambda: draw(win, grid, ROWS, width), ROWS)

                if event.key == pygame.K_4 and not start and not end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    aldous_broder(grid, lambda: draw(win, grid, ROWS, width), ROWS)

                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)

                    run_astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
