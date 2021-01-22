import matplotlib.pyplot as plt
import numpy as np
import datetime as t
import algorithm as al
import createmaze as mz
import visualisation as vis
import statistics as st


# Function to start a fire node in the maze
def let_there_be_fire(graph, src, dest):
    # Extract the keys (nodes) of the graph
    graph_keys = list(graph.keys())
    length = len(graph_keys)
    indexlist = np.random.choice(np.arange(length), length, replace=False)
    for num in indexlist:
        if num != 0 and num != length - 1 and al.dfs(graph, src, graph_keys[num])[0] == 'S' and num is not None:
            firenode = graph_keys[num]
            return firenode


# Function to spread the fire in the maze with specified probability
# 'flamability' is probability, 'a' is source and 'b' is destination thses, 'onfire' is nodes on fire
# 'a' and 'b' are added to avoid fire at src and destination
def spread_fire(graph, onfire, flamability, a, b):
    loc = onfire.copy()
    for node in graph.keys():
        if node not in loc and node not in [a, b]:
            neighbours = graph.get(node)
            n_onfire = 0  # variable to count the nodes on fire
            for n in neighbours:
                if n in loc:
                    n_onfire = n_onfire + 1  # Incrementing the count for each node on fire
            if n_onfire > 0:  # Spreading fire on the given probability
                prob = 1 - ((1 - flamability) ** n_onfire)
                if np.random.choice(np.arange(2), 1, p=[1 - prob, prob])[0] == 1:
                    onfire.append(node)  # adding the new nodes on fire to the previous fire node list


# foolhardy
# Solution 1
# Agent follows the searched path without changing or recomputing it.
# 'f1' is the starting point of fire
# Using Bidirectional BFS to find the shortest path from Algorithm class
# 'q1' is flamability
# 'dsflag' this is display flag to diplay mazes if required
def sol1(maze1, size1, graph1, src1, dest1, f1, q1, dsflag):
    start1 = t.datetime.now()
    result1 = al.bibfs(graph1, src1, dest1)
    maze1[0][0] = 2  # mark starting point
    maze1[size1 - 1][size1 - 1] = 5  # mark ending point
    nodes_on_fire = []
    maze1[f1[0]][f1[1]] = 3
    nodes_on_fire.append(f1)
    result1[2].pop(0)
    for i in range(len(result1[2])):
        step1 = result1[2].pop(0)
        maze1[step1[0]][step1[1]] = 2
        if step1 == dest1:  # If step is equal to destination
            if dsflag:
                vis.display_maze_onfire(maze1, size1, q1, "SOLUTION 1")
            return True, (t.datetime.now() - start1).microseconds
        spread_fire(graph1, nodes_on_fire, q1, src1, dest1)
        for j in nodes_on_fire:
            maze1[j[0]][j[1]] = 3
        if step1 in nodes_on_fire:
            maze1[step1[0]][step1[1]] = 4
            nodes_on_fire.remove(step1)
            if dsflag:  # This is display flag to display mazes if required
                vis.display_maze_onfire(maze1, size1, q1, "SOLUTION 1")
            return False, 0


# intelligent but cheater
# Solution 2
# Agent follows the searched path and changes path by recomputing.
# Recomputing takes places when any of the given path node is on fire
# 'f2' is the starting point of fire
# 'q2' is flamability
# 'dsflag' this is display flag to diplay mazes if required
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol2(maze2, size2, graph2, src2, dest2, f2, q2, dsflag):
    success2 = False
    totaltime2 = 0
    start2 = t.datetime.now()  # Noting time
    maze2[0][0] = 2
    maze2[size2 - 1][size2 - 1] = 5
    nodes_on_fire = []
    maze2[f2[0]][f2[1]] = 3
    nodes_on_fire.append(f2)
    step2 = src2
    while True:
        result2 = al.bibfs(mz.create_graph(maze2), step2, dest2)  # calling bi-bfs to get result
        if not result2[2]:
            break
        step2 = result2[2].pop(1)
        maze2[step2[0]][step2[1]] = 2
        if step2 == dest2:  # Checking Destination
            success2 = True
            totaltime2 = (t.datetime.now() - start2).microseconds
            break
        spread_fire(graph2, nodes_on_fire, q2, src2, dest2)
        for i in nodes_on_fire:  # Nodes on fire
            maze2[i[0]][i[1]] = 3
        if step2 in nodes_on_fire:
            maze2[step2[0]][step2[1]] = 4
            nodes_on_fire.remove(step2)
            break
    if dsflag:  # This is display flag to display mazes if required
        vis.display_maze_onfire(maze2, size2, q2, "SOLUTION 2")
    return success2, totaltime2


# realistically intelligent
# Solution 3
# Agent follows the searched path and senses the neighbors for fire of every node of the path to take each step
# If the neighbor of the shortest path nodes are or fire or the path nodes are on fire it recomputes a
# different path
# 'f3' is the starting point of fire
# 'q3' is flamability
# 'dsflag' this is display flag to display mazes if required
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol3(maze3, size3, graph3, src3, dest3, f3, q3, dsflag):
    def feelthefire(gr, st, fire, level):  # gr =  graph, src = source, fire = nodes on fire, level = depth
        currentnode = st
        if currentnode in fire:
            return True

        # If reached the maximum depth, stop recursing.
        elif level <= 0:
            return False
        else:
            if currentnode not in ff:
                for neigh in gr[st]:
                    if neigh not in ff:
                        ff.add(currentnode)
                        if feelthefire(gr, neigh, fire, level - 1):
                            return True
        return False

    start3 = t.datetime.now()
    success3 = False
    totaltime3 = 0
    result3 = al.bibfs(graph3, src3, dest3)
    maze3[0][0] = 2  # mark starting point
    maze3[size3 - 1][size3 - 1] = 5  # mark ending point
    nodes_on_fire = []
    maze3[f3[0]][f3[1]] = 3
    nodes_on_fire.append(f3)
    prevnode = src3
    while True:
        step3 = result3[2].pop(1)
        if step3 == dest3:
            maze3[step3[0]][step3[1]] = 2
            success3 = True
            totaltime3 = (t.datetime.now() - start3).microseconds
            break
        ff = set([])
        check = feelthefire(graph3, prevnode, nodes_on_fire, 3)  # CHeck if there is fire
        if check:
            result3 = al.bibfs(mz.create_graph(maze3), prevnode, dest3)
            if not result3[2]:
                break
            step3 = result3[2].pop(1)
        prevnode = step3
        maze3[step3[0]][step3[1]] = 2
        spread_fire(graph3, nodes_on_fire, q3, src3, dest3)  # Spread fire calling
        for i in nodes_on_fire:
            maze3[i[0]][i[1]] = 3
        if step3 in nodes_on_fire:
            maze3[step3[0]][step3[1]] = 4
            break

    if dsflag:
        vis.display_maze_onfire(maze3, size3, q3, "SOLUTION 3")
    return success3, totaltime3


# Generating Total time taken and Success Rate for flame probability
def generate_result():
    resultstore = {}
    timelist = ["Totaltimetaken_Sol_1", "Totaltimetaken_Sol_2", "Totaltimetaken_Sol_3"]
    timetitle = "Flamability vs Average Time Taken"
    succestitle = "Flamability vs Average Number of Success"
    successratelist = ["TotalSuccessRate_Sol_1", "TotalSuccessRate_Sol_2", "TotalSuccessRate_Sol_3"]
    for inter in range(0, 2):
        flamabilityList = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
        s = 70  # Selected Maze size
        sr = (0, 0)
        des = (s - 1, s - 1)
        print("Moving............")
        result = {}
        for q in flamabilityList:
            successcount1, successcount2, successcount3 = 0, 0, 0
            timetakenS1, timetakenS2, timetakenS3 = [], [], []
            counter = 0
            while counter < 10:  # Total 10 iterations
                m1 = mz.create_maze(s, 0.3)  # Create maze function
                gr1 = mz.create_graph(m1)  # Then create graph
                m2 = m1.copy()  # maze
                gr2 = gr1.copy()  # graph
                m3 = m1.copy()  # maze
                gr3 = gr1.copy()  # graph
                fireStart = let_there_be_fire(gr1, sr, des)  # initializes fire
                if al.bibfs(gr1, sr, des)[0] == 'S' and fireStart is not None:

                    # Solution 1
                    rs1 = sol1(m1, s, gr1, sr, des, fireStart, q, False)  # m1 and gr1 used
                    if rs1[0]:
                        successcount1 += 1
                        timetakenS1.append(rs1[1])

                    # Solution 2
                    rs2 = sol2(m2, s, gr2, sr, des, fireStart, q, False)  # m2 and gr2 used
                    if rs2[0]:
                        successcount2 += 1
                        timetakenS2.append(rs2[1])

                    # Solution 3
                    rs3 = sol3(m3, s, gr3, sr, des, fireStart, q, False)  # m3 and gr3 used
                    if rs3[0]:
                        successcount3 += 1
                        timetakenS3.append(rs3[1])
                    counter += 1

            result[q] = {"TotalSuccessRate_Sol_1": successcount1,
                         "Totaltimetaken_Sol_1": st.mean(timetakenS1) if len(timetakenS1) > 0 else 0,
                         "TotalSuccessRate_Sol_2": successcount2,
                         "Totaltimetaken_Sol_2": st.mean(timetakenS2) if len(timetakenS2) > 0 else 0,
                         "TotalSuccessRate_Sol_3": successcount3,
                         "Totaltimetaken_Sol_3": st.mean(timetakenS3) if len(timetakenS3) > 0 else 0}

        # Flamability vs Average Number of Success
        vis.disp_graph_maze_onfire(result, flamabilityList, "Flamability", "Number of Success", succestitle,
                                   successratelist)
        # Flamability vs Average Time Taken
        vis.disp_graph_maze_onfire(result, flamabilityList, "Flamability", "Time Taken (micro sec)", timetitle,
                                   timelist)


# Generating sample mazes for specific flamability and sizes
def generate_sample():
    flamability = 0.3
    s = 10  # Selected Maze size
    sr = (0, 0)
    des = (s - 1, s - 1)
    num = 0
    while num != 1:
        m1 = mz.create_maze(s, 0.3)  # Create maze function
        gr1 = mz.create_graph(m1)  # Then create graph
        m2 = m1.copy()  # maze
        gr2 = gr1.copy()  # graph
        m3 = m1.copy()  # maze
        gr3 = gr1.copy()  # graph
        fire_St = let_there_be_fire(gr1, sr, des)  # initializes fire
        if al.bibfs(gr1, sr, des)[0] == 'S' and fire_St is not None:
            # Solution 1
            sol1(m1, s, gr1, sr, des, fire_St, flamability, True)  # m1 and gr1 used

            # Solution 2
            sol2(m2, s, gr2, sr, des, fire_St, flamability, True)  # m2 and gr2 used

            # Solution 3
            sol3(m3, s, gr3, sr, des, fire_St, flamability, True)  # m3 and gr3 used
            num = 1

    # Show maze
    plt.show()


# generate_result()
# generate_result()

# Generating samples
generate_sample()

plt.show()
