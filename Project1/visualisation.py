import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec


# This function helps to display the maze.
# matplotlib library is imported and to generate a figure.
# Configured the maze with required specifications
# This is called in analysis.py and maze_thinning.py
def display_maze(item, size, title):
    fig = plt.figure()                                       # Initializing a figure
    ax = fig.add_subplot()
    ax.matshow(item, cmap=cm.binary)
    ax.set_title(title)                                      # Adding title
    ax.set_xticks(np.arange(-0.5, size, 1))
    ax.set_yticks(np.arange(-0.5, size, 1))
    ax.set_xticklabels(np.arange(0, size + 1, 1), rotation=90, horizontalalignment="right")
    ax.set_yticklabels(np.arange(0, size + 1, 1), horizontalalignment="right")
    ax.grid(color='k', linestyle='-', linewidth=2)


# Size vs Path Length  specific for probability of 0.3
# This is called in analysis.py
def disp_path_for_probab3(data, startsize, endsize, step):
    fig = plt.figure()                                          # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Path")
    ax1.set_title("Size vs Path Length with probability 0.3")
    size_list = []                                              # List to append the sizes of maze
    for size in range(startsize, endsize + step, step):
        size_list.append(size)
    algo_list = ["bfs", "dfs", "dijk", "bibfs"]                 # List of search algorithms
    for algo in algo_list:
        d = data.get(0.3)                                       # Fixed probability of 0.3 and getting graphs
        path = list(map(lambda key: (d.get(key)).get(algo + "_path"), d.keys()))
        ax1.scatter(size_list, path, label=algo)
    ax1.legend(title="Search Algorithms")
    ax1.grid(True)


# Size vs Time  specific for probability of 0.3
# This is called in analysis.py
def disp_time_for_probab3(data, startsize, endsize, step):
    fig = plt.figure()                                      # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Time (micro sec)")
    ax1.set_title("Size vs Time with probability 0.3")
    size_list = []                                          # List to append the sizes of maze
    for size in range(startsize, endsize + step, step):
        size_list.append(size)
    algo_list = ["bfs", "dfs", "dijk", "bibfs"]
    for algo in algo_list:
        d = data.get(0.3)                                   # Fixed probability of 0.3 and getting graphs
        time = list(map(lambda key: (d.get(key)).get(algo + "_time"), d.keys()))
        ax1.scatter(size_list, time, label=algo)
    ax1.legend(title="Search Algorithms")
    ax1.grid(True)


# Size vs Success Rate
# Probability are 0.1, 0.3, 0.4, 0.5, 0.7 and 0.9
# This is called in analysis.py
def disp_stats_for_probab(data, startsize, endsize, step, probability_list):
    fig = plt.figure()                                             # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Success Rate out of 10")
    ax1.set_title("Success Rate vs Size ")
    size_list = []                                          # List to append the sizes of maze
    for size in range(startsize, endsize + step, step):
        size_list.append(size)

    for prob in probability_list:
        d = data.get(prob)                                    # Extract information with index as probability
        success = list(map(lambda key: (d.get(key)).get("TotalSuccessRate"), d.keys()))
        ax1.scatter(size_list, success, label=prob)

    ax1.legend(title="Size vs Success Rate")
    ax1.grid(True)


# Color code, w = white, k = black, c = cyan, y = yellow, red = red, g = green
# Function used to display the maze after the agent is burned or reached destination
# m is maze and si is size
# 'bounds' is used as enumerator for each color node
# This is called in solutions.py
def display_maze_onfire(m, si, flamability, solut):
    cmap = ListedColormap(['w', 'k', 'c', 'y', 'r', 'g'])
    bounds = [0, 1, 2, 3, 4, 5, 6]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1)
    ax = fig.add_subplot(gs[0])
    ax.matshow(m, cmap=cmap, norm=norm)
    ax.set_title(
        "Size :: " + str(si) + " , Flamability:: " + str(flamability) + " , Solution:: " + solut)
    ax.set_xticks(np.arange(-0.5, si, 1))
    ax.set_yticks(np.arange(-0.5, si, 1))
    ax.set_xticklabels(np.arange(0, si + 1, 1), rotation=90, horizontalalignment="center")
    ax.set_yticklabels(np.arange(0, si + 1, 1), horizontalalignment="center")
    ax.grid(color='k', linestyle='-', linewidth=2)


# Flamability vs variable(Time/Success rate)
# This is called in solutions.py
def disp_graph_maze_onfire(data, flamabilityList, xlabel, ylabel, title, varlist):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)

    for name in varlist:
        value = list(map(lambda key: (data.get(key)).get(name), data.keys()))
        ax1.plot(flamabilityList, value, label=name)
    ax1.legend(title="Solutions")
    ax1.grid(True)


# This is called in maze_thinning.py
def dispdata(data, name, sizelist, title):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel(name)
    ax1.set_title(title)
    val = list(map(lambda key: (data.get(key)).get(name), data.keys()))
    ax1.scatter(sizelist, val, label=name)
    ax1.legend(title="Size vs " + name)
    ax1.grid(True)


# This is called in maze_thinning.py
def disp_data(data, varname, xlable, ylabel, title):
    fig = plt.figure()                               # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    thiningfactors = list(data.keys())
    processmap = {"Manhattan": "M", "Euclidean": "E", "Thining": "TH", "Diagonal": "Dia"}

    for process in list(processmap.keys()):
        pr = processmap.get(process)
        keys = data.keys()
        success = list(map(lambda key: round(data.get(key).get(pr).get(varname)), data.keys()))
        ax1.plot(thiningfactors, success, label=process)
    ax1.legend(title="Process")
    ax1.grid(True)


# This is called in maze_thinning.py
def disp_data2(data, varname, ylabel, xlable, title):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    iterations = range(1, len(data.keys()) + 1)
    success = list(map(lambda key: data.get(key).get(varname), data.keys()))
    ax1.scatter(iterations, success, label=iterations)
    ax1.grid(True)
