import random
from queue import PriorityQueue, LifoQueue, Queue
import pygame
from Grid import remove_walls, wall_between

def h(p1, p2):
    """
    Heuristic Function: Manhattan distance
    :param p1: position of node 1
    :param p2: position of node 2
    :return: Manhatten distance between both nodes
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    """
    Reconstructs path found in all pathfinding algorithms by using a dict/hash map which indicates the node each node
    came from.
    :param came_from:
    :param current:
    :param draw:
    :return:
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def dijkstras(draw, grid, start, end):
    """
    Dijkstras Pathfinding Algorithm. Guaranteed to be the shortest path.
    Stores distance from start to use PriorityQueue. Chooses lowest distance node. Visits all possible nodes until end
    is found.
    Uses came_from dict to reconstruct pathway
    :param draw: draws animations onto the screen
    :param grid: grid being used
    :param start: starting node
    :param end: target end node
    :return: True if path found, false if no possible path
    """
    open_set = PriorityQueue()
    open_set.put((0, start))
    distances = {node: float("inf") for row in grid for node in row}
    distances[start] = 0
    came_from = {}
    start.update_paths(grid)

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_distance, curr = open_set.get()

        pygame.time.delay(20)

        if curr == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        if curr_distance > distances[curr]:
            continue

        for path in curr.paths:

            if wall_between(curr, path) or path.is_barrier():
                continue

            distance = curr_distance + 1

            if distance < distances[path]:
                came_from[path] = curr
                curr_distance += 1
                distances[path] = distance
                open_set.put((distance, path))
                path.make_open()

        if len(curr.paths) == 0:
            print("No available paths")

        draw()

        if curr != start:
            curr.make_closed()

    return False


def BFS(draw, grid, start, end):
    """
    Finds path from start to end node using the classic BFS algorithm. Not guaranteed to be the shortest path.
    Uses a queue to store nodes.
    Returns True upon success
    :param draw: draws animations of search onto the screen
    :param grid: grid being used
    :param start: starting node
    :param end: ending node
    :return: True upon path found, false if no possible path
    """
    came_from = {}
    queue = Queue()
    queue.put(start)
    start.make_visited()

    while not queue.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = queue.get()

        pygame.time.delay(20)

        if curr == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        curr.update_neighbors(grid)

        for neighbor in curr.neighbors:

            if wall_between(neighbor, curr) or neighbor.is_barrier():
                continue

            neighbor.make_visited()
            came_from[neighbor] = curr
            queue.put(neighbor)
            neighbor.make_open()

        draw()

        if curr != start:
            curr.make_closed()

    return False


def dfs_pathfinder(draw, grid, start, end):
    """
    Classic Depth-First Search Algorithm to find a path. Not guaranteed to be the shortest path
    Uses a stack to store nodes unlike the BFS algorithm which uses a queue.
    Returns true if path found
    Reconstructs path using reconstruct_path function
    :param draw: draws animations onto the screen
    :param grid: grid being used
    :param start: starting node
    :param end: target end node
    :return: True if path found, otherwise false
    """
    stack = LifoQueue()
    start.make_visited()
    stack.put(start)
    came_from = {}

    while not stack.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = stack.get()

        pygame.time.delay(20)

        if curr == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        curr.update_neighbors(grid)

        for neighbor in curr.neighbors:

            if wall_between(neighbor, curr) or neighbor.is_barrier():
                continue

            neighbor.make_visited()
            came_from[neighbor] = curr
            stack.put(neighbor)
            neighbor.make_open()

        draw()

        if curr != start:
            curr.make_closed()

    return False


def greedy_best_first(draw, grid, start, end):
    """
    Finds a path to the target destination. NOT GUARANTEED TO BE THE SHORTEST PATH
    Weighted DFS/BFS algorithm. Uses a priority queue and a heuristic function (manhatten distance) in order to choose
    which node it will visit next.
    Returns true if path founds. Backtracks using the came_from hash map to reconstruct the path
    :param draw: draws animations onto the screen
    :param grid: grid being used
    :param start: starting node
    :param end: target end node
    :return: True if path found, otherwise false if no possible path
    """
    open_set = PriorityQueue()
    came_from = {}
    open_set.put((h(start.get_pos(), end.get_pos()), start))

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = open_set.get()[1]

        curr.make_visited()

        pygame.time.delay(20)

        if curr == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        curr.update_neighbors(grid)

        for neighbor in curr.neighbors:

            if wall_between(neighbor, curr) or neighbor.is_barrier():
                continue

            neighbor.make_visited()
            came_from[neighbor] = curr
            open_set.put((h(neighbor.get_pos(), end.get_pos()), neighbor))
            neighbor.make_open()

        draw()

        if curr != start:
            curr.make_closed()

    return False


def astar(draw, grid, start, end):
    """
    A* Pathfinding Algorithm: Finds the shortest path from start node to target node in an extremely effective way
    Uses a PriorityQueue with an f score, where f =  h + g
    h = heuristic function(manhatten distance from current node to target node)
    g = amount of steps taken/cost from the start node to the current node
    Once target node has been reached, backtracks using the came_from hash map and the reconstruct_path funciton
    :param draw: draw function used to draw animations to the screen
    :param grid: grid being used
    :param start: start node
    :param end: end node
    :return: True upon success, false if no possible path
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
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
            if wall_between(current, path) or path.is_barrier():
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





def kruskals(grid, draw, rows):
    """
    Randomize Kruskals Algorithm For Maze Generation:
    Create a list of all walls, and create list of sets of each cell, each containing just that one cell.
    For each wall, in some random order:
    If the cells divided by this wall belong to distinct sets:
    Remove the current wall.
    Join the sets of the formerly divided cells.
    :param grid: grid being used
    :param draw: draw function in order to draw animations as they happen
    :param rows: rows in grid: unused, could be used to randomize/ set a static starting point
    :return: True upon success
    """
    all_walls = [wall for row in grid for wall in row]  # create list of "walls" (just cells)
    all_cells = [{cell} for row in grid for cell in row]  # create list of sets of each cell

    while len(all_cells) > 1:  # loop until all sets are joined

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        wall = random.choice(all_walls)  # pick a random wall
        wall.update_paths(grid)  # update the walls available paths

        # get index of current wall
        for cell_set in all_cells:
            if wall in cell_set:
                wall_index = all_cells.index(cell_set)

        wall_set = all_cells[wall_index]
        neighbor = random.choice(wall.paths)

        # if the neighbor is in the current walls set already, do nothing
        if neighbor in wall_set:
            continue
        # otherwise, remove the wall between the cell and its neighbor, union their sets and remove the old set
        else:
            for cell_set in all_cells:
                if neighbor in cell_set:
                    neighbor_index = all_cells.index(cell_set)
            neighbor_set = all_cells[neighbor_index]
            all_cells[wall_index] = wall_set.union(neighbor_set)
            all_cells.remove(neighbor_set)

            wall.reset()
            neighbor.reset()
            remove_walls(wall, neighbor)
            draw()

    return True





def aldous_broder(grid, draw, rows):
    """
    WARNING: ALGORITHM EXTREMELY SLOW/FRUSTRATING TO WATCH
    Pick a random cell as the current cell and mark it as visited.
    While there are unvisited cells:
    Pick a random neighbour.
    If the chosen neighbour has not been visited:
      Remove the wall between the current cell and the chosen neighbour.
      Mark the chosen neighbour as visited.
    Make the chosen neighbour the current cell.
    :param grid: grid being used
    :param draw: draws animations to the screen
    :param rows: rows in grid
    :return: True upon maze successfully created
    """
    curr = grid[random.randint(0, rows - 1)][random.randint(0, rows - 1)]
    unvisited_cells = [node for row in grid for node in row]
    curr.make_visited()
    curr.reset()
    unvisited_cells.remove(curr)
    while len(unvisited_cells) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr.update_paths(grid)
        curr.reset()
        # curr.make_visited()
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
    curr.reset()

    return True





def hunt_and_kill(grid, draw, rows):
    """
    Choose a starting location.
        Perform a random walk, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
        Enter “hunt” mode, where you scan the grid looking for an unvisited cell that is adjacent to a visited cell.
        If found, carve a passage between the two and let the formerly unvisited cell be the new starting location.
    Repeat steps 2 and 3 until the hunt mode scans the entire grid and finds no unvisited cells.
    :param grid: grid being used
    :param draw: draws animations to the screen
    :param rows: Unused: could be used to set a randomized start point, currently using top left corner
    :return: True upon successful maze creation
    """
    curr = grid[1][1]
    unvisited_cells = [node for row in grid for node in row]
    unvisited_cells.remove(curr)

    while len(unvisited_cells) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr.reset()
        curr.make_visited()
        curr.update_neighbors(grid)
        if len(curr.neighbors) > 0:
            neighbor = random.choice(curr.neighbors)
            remove_walls(curr, neighbor)
            unvisited_cells.remove(neighbor)
            curr = neighbor

        else:
            for row in grid:
                curr = None
                for cell in row:
                    cell.highlight()
                    draw()
                    if cell.is_visited():
                        cell.update_neighbors(grid)
                        if len(cell.neighbors) > 0:
                            curr = random.choice(cell.neighbors)
                            remove_walls(cell, curr)
                            unvisited_cells.remove(curr)
                            cell.reset()
                            break
                    cell.reset()
                if curr is not None:
                    break
        curr.highlight()
        draw()
        curr.reset()

    return True


def prims(grid, draw, rows):
    """
    Prims minimum spanning tree algorithm randomized for maze generation
    SOURCE: Wikipedia
    Start with a grid full of walls.
    Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
    While there are walls in the list:
    Pick a random wall from the list. If only one of the two cells that the wall divides is visited, then:
    Make the wall a passage and mark the unvisited cell as part of the maze.
    Add the neighboring walls of the cell to the wall list.
    Remove the wall from the list.
    :param grid: grid being used
    :param draw: draws animations to the screen
    :param rows: rows in grid
    :return: True upon maze creation
    """
    curr = grid[random.randint(0, rows - 1)][random.randint(0, rows - 1)]
    curr.make_visited()
    curr.reset()
    wall_list = {neighbor for neighbor in curr.neighbors}
    while len(wall_list) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

    return True


def random_dfs(grid, draw):
    """
    Random DFS Algorithm (Iterative Implementation:
    Source: Wikipedia
    Choose the initial cell, mark it as visited and push it to the stack
    While the stack is not empty
    Pop a cell from the stack and make it a current cell
    If the current cell has any neighbours which have not been visited
    Push the current cell to the stack
    Choose one of the unvisited neighbours
    Remove the wall between the current cell and the chosen cell
    Mark the chosen cell as visited and push it to the stack
    :param grid: grid being used
    :param draw: draws animations to the screen
    :return: True upon successful maze generation
    """

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

    return True
