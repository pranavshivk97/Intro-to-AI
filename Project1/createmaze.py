import datetime as t
import numpy as np
import math as m


# Function creates a maze with a specific probability of blockages.
def create_maze(size, prob):
    num = [[np.random.choice(np.arange(2), 1, p=[1 - prob, prob]) for i in range(size)] for j in range(size)]
    num_arr = np.array(num)
    num_arr[0][0] = 0  # Start point initialized
    num_arr[size - 1][size - 1] = 0  # Goal point initialized
    return num_arr


# Function creates a thinned maze with thinning factor p.
def maze_thinning(p, maze):
    blocked = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                blocked.append((i, j))
    num_obstacles_to_remove = m.floor(p * len(blocked))
    indexlist = np.random.choice(np.arange(len(blocked)), num_obstacles_to_remove, replace=False)
    for i in indexlist:
        maze[blocked[i][0]][blocked[i][1]] = 0
    return maze


# Creating graph with maze cells
def create_graph(maze):
    # dictionary for graphs
    start_time = t.datetime.now()
    graph = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] not in [1, 3]:  # 1 is blockage , 3 is fire
                edges = []
                # corner
                if check_corner(i, j, maze):
                    if (i, j) == (0, 0):
                        edges = get_neighbour(maze, [(0, 1), (1, 0)], i, j)  # Starting point neighbors
                    elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(-1, 0), (0, -1)], i, j)  # Destination point neighbors
                    elif (i, j) == (0, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(0, -1), (1, 0)], i, j)  # Right most top corner neighbors
                    elif (i, j) == (maze.shape[0] - 1, 0):
                        edges = get_neighbour(maze, [(-1, 0), (0, 1)], i, j)  # Left most down corner neighbors
                # Middle part
                elif check_middle(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1), (1, 0)], i, j)
                # top layer excluding corners
                elif check_top(i, j, maze):
                    edges = get_neighbour(maze, [(0, -1), (0, 1), (1, 0)], i, j)
                # left layer excluding corners
                elif check_left(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, 1), (1, 0)], i, j)
                # bottom layer excluding corners
                elif check_bottom(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1)], i, j)

                # right layer excluding corners
                elif check_right(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (1, 0)], i, j)
                graph[(i, j)] = edges
    return graph


# Creating relaxed graph with maze cells
# With this relaxation user can mover diagonally also
def create_relaxedgraph(maze):
    # dictionary for relaxedgraphs
    regraph = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] not in [1, 3]:  # 1 is blockage , 3 is fire
                edges = []
                # corner
                if check_corner(i, j, maze):
                    if (i, j) == (0, 0):
                        # Starting point neighbors
                        edges = get_neighbour(maze, [(0, 1), (1, 0), (1, 1)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                        # Destination point neighbors
                        edges = get_neighbour(maze, [(-1, 0), (0, -1), (-1, -1)], i, j)
                    elif (i, j) == (0, maze.shape[1] - 1):
                        # Right most top corner neighbors
                        edges = get_neighbour(maze, [(0, -1), (1, 0), (1, -1)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, 0):
                        # Left most bottom corner neighbors
                        edges = get_neighbour(maze, [(-1, 0), (0, 1), (-1, 1)], i, j)
                # Middle part
                elif check_middle(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1), (1, 0),
                                                 (-1, -1), (-1, 1), (1, -1), (1, 1)], i, j)
                # top layer excluding corners
                elif check_top(i, j, maze):
                    edges = get_neighbour(maze, [(0, -1), (0, 1), (1, 0), (1, -1), (1, 1)], i, j)
                # left layer excluding corners
                elif check_left(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, 1), (1, 0), (-1, 1), (1, 1)], i, j)
                # bottom layer excluding corners
                elif check_bottom(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)], i, j)

                # right layer excluding corners
                elif check_right(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (1, 0), (1, -1), (-1, -1)], i, j)
                regraph[(i, j)] = edges
    return regraph


# Finding the neighbour of a specific node from the maze. Proper explanation in create_graph function
def get_neighbour(maze, step, i, j):
    neighbour = []
    for item in step:
        if maze[i + item[0]][j + item[1]] not in [1, 3]:
            neighbour.append(((i + item[0]), (j + item[1])))
    return neighbour


# Checking agent position if it lies in any of the four corners
def check_corner(i, j, maze):
    if (i, j) in [(0, 0), (maze.shape[0] - 1, maze.shape[1] - 1), (0, maze.shape[1] - 1),
                  (maze.shape[0] - 1, 0),
                  (maze.shape[0] - 1, maze.shape[0] - 1)]:
        return True
    else:
        return False


# Excluding the rightmost, left most, down and top one layer each and searching agent location in the middle part
def check_middle(i, j, maze):
    if 0 < i < maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in the first row excluding corners
def check_top(i, j, maze):
    if i == 0 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in first column excluding corners
def check_left(i, j, maze):
    if j == 0 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False


# Checking agent location in last row excluding corners
def check_bottom(i, j, maze):
    if i == maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in last column excluding corners
def check_right(i, j, maze):
    if j == maze.shape[1] - 1 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False
