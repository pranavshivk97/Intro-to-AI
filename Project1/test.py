import datetime as t
import createmaze as b
import numpy as np
import algorithm as al
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from matplotlib import colors
import math as m


def bibfs(graph, src, dest):
    start_time = t.datetime.now()
    # keep track of visited nodes
    fvisited = []
    bvisited = []
    # queue for implementing BFS; add src node to the queue
    f_queue, b_queue = [src], [dest]

    fpath = {}
    bpath = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
    # Run until the queue is empty
    while f_queue and b_queue:
        # Remove one node from the queue and check if it has been visited or not
        test(f_queue, fvisited, fpath, graph)
        test(b_queue, bvisited, bpath, graph)
        if set(fvisited) & set(bvisited):
            tpath1 = get_path(fpath, src, list(set(fvisited) & set(bvisited)).pop())
            tpath2 = get_path(bpath, dest, list(set(fvisited) & set(bvisited)).pop())
            tpath2.pop()
            tpath2.reverse()
            path = tpath1 + tpath2
            timetaken = (t.datetime.now() - start_time).microseconds
            return ["S", dest, path, timetaken]

    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", fpath, bpath, timetaken]


def test(queue, visited, path, graph):
    node = queue.pop(0)
    neighbors = graph.get(node)
    for neighbor in neighbors:
        if neighbor not in visited and neighbor not in queue:
            # visit neighbors and add to queue
            queue.append(neighbor)
            path[neighbor] = node
    visited.append(node)


def get_path(path, src, dest):
    pathtaken = [dest]
    child = dest
    parent = dest
    while parent != src:
        parent = path.get(child)
        pathtaken.append(parent)
        child = parent
    pathtaken.reverse()
    return pathtaken


def let_there_be_fire(graph, src, dest):
    # Extract the keys (nodes) of the graph
    graph_keys = list(graph.keys())
    length = len(graph_keys)
    for i in range(length):
        # Generate a random number from 0 to length-1
        num = np.random.choice(np.arange(length), 1, replace=False)[0]
        print(num)
        print(b.dfs(graph, src, graph_keys[num])[0])
        if num != 0 and num != length - 1 and b.dfs(graph, src, graph_keys[num])[0] == 'S' and num is not None:
            firenode = graph_keys[num]
            return firenode


def spread_fire(graph, onfire, q):
    loc = onfire.copy()
    for node in graph.keys():
        if node not in loc:
            neighbours = graph.get(node)
            n_onfire = 0
            for n in neighbours:
                if n in loc:
                    print("node-----> " + str(node) + "node--->" + str(n))
                    n_onfire = n_onfire + 1
            if n_onfire > 0:
                prob = 1 - ((1 - q) ** n_onfire)
                if np.random.choice(np.arange(2), 1, p=[1 - prob, prob])[0] == 1:
                    onfire.append(node)


# def idfs(graph, src, dest, maxdepth):
#     start_time = t.datetime.now()
#     visited = []
#     # keep track of visited nodes
#     stack = [src]  # queue for implementing BFS; add src node to the queue
#     path = {}
#     if src == dest:
#         timetaken = (t.datetime.now() - start_time).microseconds
#         return ["S", dest, path[dest], timetaken]
#     # Run until the queue is empty
#     while stack:
#         # Remove one node from the queue and check if it has been visited or not
#         node = stack.pop()
#
#         if node == dest:
#             path = get_path(path, src, dest)
#             timetaken = (t.datetime.now() - start_time).microseconds
#             return ["S", node, path, timetaken]
#
#             # get neighbors and restrict it to a desired level
#         if maxdepth >= 0:
#             neighbors = graph[node]
#             for neighbor in neighbors:
#                 # if neighbor not in visited and neighbor not in stack:
#                 # visit neighbors and add to queue
#                 if neighbor not in visited and neighbor not in stack:
#                     stack.append(neighbor)
#                     path[neighbor] = node
#
#             maxdepth = maxdepth - 1
#
#         visited.append(node)
#     timetaken = (t.datetime.now() - start_time).microseconds
#     return ["F", None, None, timetaken]


gr = {(0, 0): [(0, 1), (1, 0)], (0, 1): [(0, 0), (0, 2), (1, 1)], (0, 2): [(0, 1), (0, 3), (1, 2)],
      (0, 3): [(0, 2), (0, 4)], (0, 4): [(0, 3), (1, 4)], (1, 0): [(0, 0), (1, 1), (2, 0)],
      (1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)], (1, 2): [(0, 2), (1, 1), (2, 2)], (1, 4): [(0, 4), (2, 4)],
      (2, 0): [(1, 0), (2, 1), (3, 0)], (2, 1): [(1, 1), (2, 0), (2, 2), (3, 1)],
      (2, 2): [(1, 2), (2, 1), (2, 3), (3, 2)], (2, 3): [(2, 2), (2, 4), (3, 3)], (2, 4): [(1, 4), (2, 3), (3, 4)],
      (3, 0): [(2, 0), (3, 1), (4, 0)], (3, 1): [(2, 1), (3, 0), (3, 2), (4, 1)], (3, 2): [(2, 2), (3, 1), (3, 3)],
      (3, 3): [(2, 3), (3, 2), (3, 4), (4, 3)], (3, 4): [(2, 4), (3, 3), (4, 4)], (4, 0): [(3, 0), (4, 1)],
      (4, 1): [(3, 1), (4, 0)], (4, 3): [(3, 3), (4, 4)], (4, 4): [(3, 4), (4, 3)]}


# print(idfs(gr,(0,0),(4,4),2))

# IDDFS to search if target is reachable from v.
# It uses recursive DLS()
def idfs(gr1, s, tar, maxDepth):
    global vv
    global path
    currentnode = s
    print(currentnode)
    if currentnode == tar:
        return True

    # If reached the maximum depth, stop recursing.
    elif maxDepth <= 0:
        return False
    else:
        if currentnode not in vv:  # Recursive call to find the destination till required depth
            for i in gr1[currentnode]:
                if i not in vv:
                    path[i] = currentnode
                    vv.add(currentnode)
                    if idfs(gr1, i, tar, maxDepth - 1):
                        return True
    return False


def callidfs(graph, src, des, size):
    global vv
    global path
    for j in range(5, len(graph.keys()),5):
        print(j)
        path = {}
        vv = set([])
        sol = idfs(graph, src, des, j)
        print(sol)
        if sol:
            print("success")
            print(path)
            print(get_path(path, src, des))
            break


m = b.create_maze(7,0.3)
gr = b.create_graph(m)
callidfs(gr, (0,0), (6,6), 7)
print(al.bfs(gr , (0,0), (6,6)))



