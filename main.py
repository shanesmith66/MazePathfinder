import pygame
import algorithms
import Grid

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

WIDTH = 750 + 6
WALL_WIDTH = 5
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Generation & Path Finding Algorithm Visualizer")
pygame.init()


def main(win, width):
    """
    Main Game Loop
    :param win: Window being used
    :param width: Width/Height of Window
    :return: None
    """

    # initialize default values
    ROWS = 25
    grid = Grid.make_grid(ROWS, width)
    start = None
    end = None
    maze = False
    color = BLACK
    path = False

    run = True
    while run:
        Grid.draw(win, grid, ROWS, width, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left Click after a maze has been generated/declined to pick a start (first click) and end (second click)
            if pygame.mouse.get_pressed()[0] and maze:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = Grid.get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start and color == WHITE:
                    node.make_barrier()

            # Erase any barriers drawn by the user using right click
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = Grid.get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:

                # Press N for no maze generation. Can simply draw barriers yourself.
                if event.key == pygame.K_n and not start and not end and not maze:
                    color = WHITE
                    maze = True
                    grid = Grid.make_grid(ROWS, width, barrier=False)

                # press 1 to generate a maze using the recursive backtracking / random dfs algorithm
                if event.key == pygame.K_1 and not start and not end and not maze:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    maze = algorithms.random_dfs(grid, lambda: Grid.draw(win, grid, ROWS, width))

                # press 2 to generate a maze using randomized prims algorithm (minimum spanning tree algorithm)
                if event.key == pygame.K_2 and not start and not end and not maze:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    maze = algorithms.prims(grid, lambda: Grid.draw(win, grid, ROWS, width), ROWS)

                # press 3 to generate a maze using the randomize kruskal's algorithm (similar to prims)
                if event.key == pygame.K_3 and not start and not end and not maze:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    maze = algorithms.kruskals(grid, lambda: Grid.draw(win, grid, ROWS, width), ROWS)

                # press 4 to generate a maze using the aldous broder algorithm
                # WARNING: very slow and frustrating to watch
                if event.key == pygame.K_4 and not start and not end and not maze:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    maze = algorithms.aldous_broder(grid, lambda: Grid.draw(win, grid, ROWS, width), ROWS)

                # press 5 to generate a maze using the hunt and kill algorithm
                if event.key == pygame.K_5 and not start and not end and not maze:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    maze = algorithms.hunt_and_kill(grid, lambda: Grid.draw(win, grid, ROWS, width), ROWS)

                # PATHFINDING ALGORITHMS QWERT

                # Press Q To Solve the maze using the A* Pathfinding Algorithm
                if event.key == pygame.K_q and start and end and not path:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)

                    path = algorithms.astar(lambda: Grid.draw(win, grid, ROWS, width, color), grid, start, end)

                # Press W To Solve the maze using Dijkstra's Algorithm
                if event.key == pygame.K_w and start and end and not path:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)

                    path = algorithms.dijkstras(lambda: Grid.draw(win, grid, ROWS, width, color), grid, start, end)

                # Press E To Solve the maze using Breadth-First Search
                if event.key == pygame.K_e and start and end and not path:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)
                            node.make_unvisited()

                    path = algorithms.BFS(lambda: Grid.draw(win, grid, ROWS, width, color), grid, start, end)

                # Press R To Solve the maze using Depth-First Search
                if event.key == pygame.K_r and start and end and not path:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)
                            if not node.is_barrier():
                                node.make_unvisited()

                    path = algorithms.dfs_pathfinder(lambda: Grid.draw(win, grid, ROWS, width, color), grid, start, end)

                # Press t To Solve the maze using Greedy Best-First Search
                if event.key == pygame.K_t and start and end and not path:
                    for row in grid:
                        for node in row:
                            node.update_paths(grid)
                            node.make_unvisited()

                    path = algorithms.greedy_best_first(lambda: Grid.draw(win, grid, ROWS, width, color), grid, start, end)

                # Press C to clear the maze/path back to the original black slate
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    maze = False
                    color = BLACK
                    path = False
                    grid = Grid.make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)