# Maze Generation and Pathfinding Algorithm Visualizer
Generates a maze using 5 different algorithms (Unless the user wants to draw their own barricades). Finds path from A to B using 5 different pathfinding algorithms.
- Based on/Inspired by TechWithTims A* Pathfinding Visualizer

# CONTROLS
H - Print help in console, showing these controls

C - Clear Grid

### MAZE GENERATION 

1 - Generate Maze Using Random DFS Algorithm

2 - Generate Maze Using Prims Algorithm

3 - Generate Maze Using Kruskals Algorithm

4 - Generate Maze Using Aldous Broder Algorithm

5 - Generate Maze Using Hunt and Kill Algorithm

N - Do not generate maze, draw own barricades using Left and Right Click

### AFTER MAZE GENERATED/NO MAZE

Left click #1: Pick Start

Left click #2: Pick End

**IF NO MAZE:** Any subsequent left clicks will draw barricades

Right click to erase barricade/start/end

### PATHFINDING ALGORITHMS - Once start and end defined

Q - A* Pathfinding

W - Dijkstra's Algorithm

E - Breadth-First Search

R - Depth-First Search

T - Greedy Best-First Search

# RANDOM DFS
Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search

    Choose the initial cell, mark it as visited and push it to the stack

      While the stack is not empty

        Pop a cell from the stack and make it a current cell

        If the current cell has any neighbours which have not been visited

          Push the current cell to the stack

          Choose one of the unvisited neighbours

          Remove the wall between the current cell and the chosen cell

          Mark the chosen cell as visited and push it to the stack

![Random DFS](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/RandomDFS%20Maze.gif)

# PRIMS ALGORITHM
Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm

    Start with a grid full of walls.
    
    Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
    
    While there are walls in the list:
    
      Pick a random wall from the list. If only one of the two cells that the wall divides is visited, then:
      
        Make the wall a passage and mark the unvisited cell as part of the maze.
        
        Add the neighboring walls of the cell to the wall list.
        
      Remove the wall from the list.
      
![Randomized Prims](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/Prims%20Maze.gif)

# KRUSKALS ALGORITHM

Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Kruskal's_algorithm

    Create a list of all walls, and create a set for each cell, each containing just that one cell.
    For each wall, in some random order:
      If the cells divided by this wall belong to distinct sets:
        Remove the current wall.
        Join the sets of the formerly divided cells.
        
![Randomized Kruskals](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/Kruskals%20Maze.gif)

# ALDOUS BRODER

source:  http://weblog.jamisbuck.org/2011/1/17/maze-generation-aldous-broder-algorithm

**WARNING: Algorithm very slow/frustrating to watch. More of a brute force approach.**

    Choose a vertex. Any vertex.

      Choose a connected neighbor of the vertex and travel to it. If the neighbor has not yet been visited, add the traveled edge to the spanning tree.

      Repeat step 2 until all vertexes have been visited.
      
![Aldous Broder](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/AldousBroder%20Maze.gif)

      
# HUNT AND KILL

source: https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm

    Choose a starting location.

    Perform a random walk, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.

    Enter “hunt” mode, where you scan the grid looking for an unvisited cell that is adjacent to a visited cell. If found, carve a passage between the two and let the formerly unvisited cell be the new starting location.

    Repeat steps 2 and 3 until the hunt mode scans the entire grid and finds no unvisited cells.
        
![Hunt and Kill](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/HuntAndKill%20maze.gif)

# A* Pathfinding Algorithm

algorithm explained https://youtu.be/JtiK0DOeI4A?t=198

![A* Pathfinding](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/A*%20Pathfinder.gif)

# Dijkstra's Algorithm

source: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm

    Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.

    Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other nodes. Set the initial node as current.[16]

    For the current node, consider all of its unvisited neighbours and calculate their tentative distances through the current node. Compare the newly calculated tentative distance to the current assigned value and assign the smaller one. For example, if the current node A is marked with a distance of 6, and the edge connecting it with a neighbour B has length 2, then the distance to B through A will be 6 + 2 = 8. If B was previously marked with a distance greater than 8 then change it to 8. Otherwise, the current value will be kept.

    When we are done considering all of the unvisited neighbours of the current node, mark the current node as visited and remove it from the unvisited set. A visited node will never be checked again.

    If the destination node has been marked visited (when planning a route between two specific nodes) or if the smallest tentative distance among the nodes in the unvisited set is infinity (when planning a complete traversal; occurs when there is no connection between the initial node and remaining unvisited nodes), then stop. The algorithm has finished.

    Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new "current node", and go back to step 3.
    
![Dijkstras](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/Dijkstras%20Pathfinder.gif)

# Breadth-First Search (BFS)

source: https://hurna.io/academy/algorithms/maze_pathfinder/bfs.html

    Add the start node in the queue and mark as visited.

    While there is a node waiting in the queue:

    1. Take the node at the front of the line (queue).

    2. Add to the queue all available neighbors, note the parent and mark as visited

    Done: backtrack from goal to start using parent link in order to get the shortest path.
    
![BFS](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/BFS%20Pathfinder.gif)

# Depth-First Search (DFS)

source: https://hurna.io/academy/algorithms/maze_pathfinder/dfs.html

    Add the start node in the stack and mark as visited.
    
    While there is a node waiting in the stack:
    
    1. Take the node at the top of the stack.
    
    2. Add on the stack all available neighbors in order, note the parent and mark as visited
    
    Done: backtrack from goal to start using parent link in order to get the path.

![DFS](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/DFS%20Pathfinder.gif)

# Greedy Best-First Search

source: https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS

    Much like DFS/BFS, except:
    
    If the successor's heuristic is better than its parent, the successor is set at the front of the queue (with the parent reinserted directly behind it), and the loop restarts.
    
    Else, the successor is inserted into the queue (in a location determined by its heuristic value). The procedure will evaluate the remaining successors (if any) of the parent.


![Greedy Best-First Search](https://github.com/shanesmith66/MazePathfinder/blob/main/Maze:Pathfinding%20Gifs/Greedy%20Best-First%20Search.gif)



