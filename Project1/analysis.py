import statistics
import createmaze as mz
import algorithm as al
import visualisation as vis
import matplotlib.pyplot as plt


# This method is used to generate sample mazes for given size
def generate_sample():
    prob_list = [0.1, 0.3, 0.5]
    startsize = int(input("Enter the Start size "))
    endsize = int(input("Enter the End size "))
    step = int(input("Enter the growth size "))

    for size in range(startsize, endsize + step, step):
        for prob in prob_list:
            print("Sample mazes of " + str(size) + " with " + str(prob) + " will be generated")
            for x in range(0, 2):  # 2 Iterations and mean results
                maze = mz.create_maze(size, prob)
                vis.display_maze(maze, size, "Maze with size " + str(size) + " and probability of " + str(prob))


# Generating dictionary with probability from 0.1 to 0.9 and value holds another dictionary with keys as size and
# value as success count, total cost and time taken for 10 iterations of each search algorithm.
def letsfind():
    startsize = int(input("Enter the starting  size "))
    endsize = int(input("Enter the max size "))
    step = int(input("Enter the growth size "))
    data = {}  # The main dictionary
    probability_list = [0.1, 0.3, 0.5, 0.7, ]  # Probability list
    for probability in probability_list:  # Looping for each probability
        subdict = {}
        for size in range(startsize, endsize + step, step):  # Looping for each size defined
            successcount = 0  # Initializations
            paths_bfs = []
            paths_dfs = []
            paths_dijk = []
            paths_bibfs = []
            time_bfs = []
            time_dfs = []
            time_dijk = []
            time_bibfs = []

            for x in range(0, 2):                                       # 10 Iterations and mean results
                maze = mz.create_maze(size, probability)
                print("Maze Moving to Next")

                graph = mz.create_graph(maze)                            # Create graph through maze
                print("Graph Moving to Next")

                start = (0, 0)                                           # start point
                end = ((maze.shape[0] - 1), (maze.shape[0] - 1))         # End point

                bfs_sol = al.bfs(graph, start, end)  # BFS
                print("BFS  Moving to Next")
                paths_bfs.append(len(bfs_sol[2]))
                time_bfs.append(bfs_sol[3])
                if bfs_sol[0] == "S":
                    successcount = successcount + 1  # Success count incrementing

                dfs_sol = al.dfs(graph, start, end)  # DFS
                print("DFS  Moving to Next")
                paths_dfs.append(len(dfs_sol[2]))
                time_dfs.append(dfs_sol[3])

                dijk_sol = al.dijkstra(graph, start, end)  # DIJKSTRA
                print("Dijkstra Moving to Next")
                paths_dijk.append(len(dijk_sol[2]))
                time_dijk.append(dijk_sol[3])

                bibfs_sol = al.bibfs(graph, start, end)  # BI-BFS
                print("BiBFS Moving to Next")
                paths_bibfs.append(len(bibfs_sol[2]))
                time_bibfs.append(bibfs_sol[3])

            # Dictionary holding size as keys and Means results of each algorithm
            subdict[size] = {
                "TotalSuccessRate": successcount,
                "bfs_path": statistics.mean(paths_bfs),
                "bfs_time": statistics.mean(time_bfs),
                "dfs_path": statistics.mean(paths_dfs),
                "dfs_time": statistics.mean(time_dfs),
                "dijk_path": statistics.mean(paths_dijk),
                "dijk_time": statistics.mean(time_dijk),
                "bibfs_path": statistics.mean(paths_bibfs),
                "bibfs_time": statistics.mean(time_bibfs)}

        data[probability] = subdict  # Adding Probability as keys and Values as the sub dictionary

    vis.disp_stats_for_probab(data, startsize, endsize, step, probability_list)           # success rate vs size
    vis.disp_time_for_probab3(data, startsize, endsize, step)                             # time vs size
    vis.disp_path_for_probab3(data, startsize, endsize, step)                             # Path vs size


# Function calling for Analysis results
letsfind()

# Two sample maze of given size and probability
generate_sample()

# To show the figures
plt.show()
