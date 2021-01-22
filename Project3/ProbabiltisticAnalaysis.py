import ProbablisticHunting as Ph
import numpy as np
import matplotlib.pyplot as plt
import datetime as t

"""
This class is to analyze 
"""


class ProbabilisticAnalysis:

    def __init__(self, terrainprob, diffProbDict):
        self.terrainprob = terrainprob
        self.diffProbDict = diffProbDict

    # Avg number of search count/actions for each terrian type and for each agent
    # Normal plot graph
    def disp_data1(self, data, varnames, xlable, ylabel, title):
        """
        This method is used to visualize data by displaying the graph
        :param data: data to be plotted
        :param varnames: variables to be plotted
        :param xlable: x label
        :param ylabel: y label
        :param title: title
        """
        fig = plt.figure()  # Initializing figure
        ax1 = fig.add_subplot()
        ax1.set_xlabel(xlable)
        ax1.set_ylabel(ylabel)
        ax1.set_title(title)
        datakeys = ["Plain", "Hills", "Forest", "Caves"]

        for index, var in enumerate(varnames):
            toplot = list(map(lambda key: data.get(key)[index], data.keys()))
            ax1.plot(datakeys, toplot, label=var)  # Plotting the figure
        ax1.legend(title="Agent")
        ax1.grid(True)

    # Creating axis on figure, average no of search counts/actions per agent
    # Bar graph plot
    def disp_data2(self, data, xlable, ylabel, title):
        """
        This method is used to visualize data by displaying the graph
        :param data: data to be plotted
        :param varnames: variables to be plotted
        :param xlable: x label
        :param ylabel: y label
        :param title: title
        """
        fig = plt.figure()  # Initializing figure
        ax1 = fig.add_subplot()
        ax1.set_xlabel(xlable)
        ax1.set_ylabel(ylabel)
        ax1.set_title(title)
        datakeys = data.keys()
        datavalues = data.values()
        ax1.bar(datakeys, datavalues)

    # Agent 1 and Agent 2 to find target on same map with multiple targets
    def samemap(self, size, interations):
        start_time = t.datetime.now()
        print("Comparing Agent 1 and Agent 2 for fixed Map with Multiple Targets:: ")
        ph = Ph.ProbabilisticHunting(size, self.terrainprob, self.diffProbDict)  # Hunting class object
        targets = set()
        ph.create_landscape()  # Creating landscape
        agent1targetdict = {0: [], 1: [], 2: [], 3: []}
        agent2targetdict = {0: [], 1: [], 2: [], 3: []}
        averageserachcountfortarget = {0: [], 1: [], 2: [], 3: []}
        averageserachcount = {"Agent1": [], "Agent2": []}
        for i in range(0, interations):
            print("iteration :: " + str(i))
            while True:
                newtarget = ph.settarget()  # Getting same target for all the maps, changing on each iteration
                if targets == ph.cells:
                    targets.clear()
                    targets.add(newtarget)
                    # ph.landscape[c[0]][c[1]])
                elif newtarget not in targets:
                    targets.add(newtarget)
                    break
            ph.probabilitydictionary()
            agnet1searchcount = ph.gamerule1()[1]  # Rule 1
            ph.probabilitydictionary()
            agnet2searchcount = ph.gamerule2()[1]  # Rule 2
            agent1targetdict.get(ph.landscape[newtarget[0]][newtarget[1]]).append(agnet1searchcount)
            agent2targetdict.get(ph.landscape[newtarget[0]][newtarget[1]]).append(agnet2searchcount)
        for val in agent1targetdict:  # Counting for agent 1
            if agent1targetdict.get(val):
                averageserachcountfortarget[val].append(np.mean(agent1targetdict.get(val)))
                averageserachcount["Agent1"].append(averageserachcountfortarget[val][0])
            if agent2targetdict.get(val):  # Counting for agent 2
                averageserachcountfortarget[val].append(np.mean(agent2targetdict.get(val)))
                averageserachcount["Agent2"].append(averageserachcountfortarget[val][1])
        for val in averageserachcount:  # Averaging
            if averageserachcount[val]:
                averageserachcount[val] = np.mean(averageserachcount.get(val))
        for val in averageserachcountfortarget:  # Averaging
            if not averageserachcountfortarget.get(val):
                averageserachcountfortarget[val] = [0, 0]
        self.disp_data1(averageserachcountfortarget, ["Agent1", "Agent2"], "Terrain types", "Search Count", "Comparison"
                        + " of Agent1 and Agent 2 for Fixed Map")
        self.disp_data2(averageserachcount, "Agents", "Search Count", "Comparison"
                        + " of Agent1 and Agent 2 for Fixed Map")
        print((t.datetime.now() - start_time).seconds)
        plt.show()

    # Agent 1 and Agent 2 to find target on multiple maps, changing target on each iteration
    def multiple_map(self, size, interations):
        start_time = t.datetime.now()
        print("Comparing Agent 1 and Agent 2 for Multiple Maps:: ")
        ph = Ph.ProbabilisticHunting(size, self.terrainprob, self.diffProbDict)
        targets = set()
        agent1targetdict = {0: [], 1: [], 2: [], 3: []}
        agent2targetdict = {0: [], 1: [], 2: [], 3: []}
        averageserachcountfortarget = {0: [], 1: [], 2: [], 3: []}
        averageserachcount = {"Agent1": [], "Agent2": []}
        for i in range(0, interations):  # Iterating
            print("iteration :: " + str(i))
            ph.create_landscape()
            newtarget = ph.settarget()  # New target set
            targets.add(newtarget)
            ph.probabilitydictionary()
            agnet1searchcount = ph.gamerule1()[1]  # Rule 1
            ph.probabilitydictionary()
            agnet2searchcount = ph.gamerule2()[1]  # Rule 2
            agent1targetdict.get(ph.landscape[newtarget[0]][newtarget[1]]).append(agnet1searchcount)
            agent2targetdict.get(ph.landscape[newtarget[0]][newtarget[1]]).append(agnet2searchcount)
        for val in agent1targetdict:  # Agent 1 target count
            if agent1targetdict.get(val):
                averageserachcountfortarget[val].append(np.mean(agent1targetdict.get(val)))
                averageserachcount["Agent1"].append(averageserachcountfortarget[val][0])
            if agent2targetdict.get(val):  # Agent 2 target count
                averageserachcountfortarget[val].append(np.mean(agent2targetdict.get(val)))
                averageserachcount["Agent2"].append(averageserachcountfortarget[val][1])
        for val in averageserachcount:  # Averaging
            if averageserachcount[val]:
                averageserachcount[val] = np.mean(averageserachcount.get(val))
        for val in averageserachcountfortarget:  # Averaging
            if not averageserachcountfortarget.get(val):
                averageserachcountfortarget[val] = [0, 0]
        self.disp_data1(averageserachcountfortarget, ["Agent1", "Agent2"], "Terrain types", "Search Count", "Comparison"
                        + " of Agent1 and Agent 2 for Multiple Map")
        self.disp_data2(averageserachcount, "Agents", "Actions", "Comparison"
                        + " of Agent1 and Agent 2 for Multiple Map")
        plt.show()

    # Comparing all agents to find stable target on multiple maps, changing target on each iteration
    def compareall(self, size, interations):
        start_time = t.datetime.now()
        print("Comparing all agents for multiple maps:: ")
        ph = Ph.ProbabilisticHunting(size, self.terrainprob, self.diffProbDict)
        targets = set()
        agent1targetdict = {0: [], 1: [], 2: [], 3: []}  # Agent 1
        agent2targetdict = {0: [], 1: [], 2: [], 3: []}  # Agent 2
        agent3targetdict = {0: [], 1: [], 2: [], 3: []}  # Agent 3
        agent4targetdict = {0: [], 1: [], 2: [], 3: []}  # Agent 4
        agent5targetdict = {0: [], 1: [], 2: [], 3: []}  # Agent 5
        averageactionsfortarget = {0: [], 1: [], 2: [], 3: []}
        averageactions = {"Agent1": [], "Agent2": [], "Agent3": [], "Agent4": [], "Agent5": []}
        for i in range(0, interations):
            print("iteration :: " + str(i))  # Printing the iteration number
            ph.create_landscape()
            newtarget = ph.settarget()  # Setting target
            targets.add(newtarget)
            ph.probabilitydictionary()  # create new dictionary
            Agents1actions = ph.gamerule1()[2]  # Agent 1 actions
            ph.probabilitydictionary()  # create new dictionary
            Agents2actions = ph.gamerule2()[2]  # Agent 2 actions
            ph.probabilitydictionary()
            Agents3actions = ph.gamerule3()[2]  # Agent 3 actions
            ph.probabilitydictionary()
            Agents4actions = ph.gamerule4()[2]  # Agent 4 actions
            ph.probabilitydictionary()
            Agents5actions = ph.gamerule5()[2]  # Agent 5 actions
            targetterrain = ph.landscape[newtarget[0]][newtarget[1]]  # Assigning target
            agent1targetdict.get(targetterrain).append(Agents1actions)
            agent2targetdict.get(targetterrain).append(Agents2actions)
            agent3targetdict.get(targetterrain).append(Agents3actions)
            agent4targetdict.get(targetterrain).append(Agents4actions)
            agent5targetdict.get(targetterrain).append(Agents5actions)
        for val in agent1targetdict:
            if agent1targetdict.get(val):
                averageactionsfortarget[val].append(np.mean(agent1targetdict.get(val)))
                averageactions["Agent1"].append(averageactionsfortarget[val][0])
            if agent2targetdict.get(val):
                averageactionsfortarget[val].append(np.mean(agent2targetdict.get(val)))
                averageactions["Agent2"].append(averageactionsfortarget[val][1])
            if agent3targetdict.get(val):
                averageactionsfortarget[val].append(np.mean(agent3targetdict.get(val)))
                averageactions["Agent3"].append(averageactionsfortarget[val][2])
            if agent4targetdict.get(val):
                averageactionsfortarget[val].append(np.mean(agent4targetdict.get(val)))
                averageactions["Agent4"].append(averageactionsfortarget[val][3])
            if agent5targetdict.get(val):
                averageactionsfortarget[val].append(np.mean(agent5targetdict.get(val)))
                averageactions["Agent5"].append(averageactionsfortarget[val][4])
        for val in averageactions:  # Averaging
            if averageactions[val]:
                averageactions[val] = np.mean(averageactions.get(val))
        for val in averageactionsfortarget:
            if not averageactionsfortarget.get(val):
                averageactionsfortarget[val] = [0, 0, 0, 0, 0]
        self.disp_data1(averageactionsfortarget, ["Agent1", "Agent2", "Agent3", "Agent4", "Agent5"], "Terrain types",
                        "Actions", "Comparison"
                        + " of all agents")
        self.disp_data2(averageactions, "Agents", "Actions", "Comparison"
                        + " of all agents")
        print((t.datetime.now() - start_time).seconds)
        plt.show()

    # Comparing all agents to find moving target on multiple maps, target is set to original postion for each agent
    def compareallformovingtarget(self, size, interations):
        start_time = t.datetime.now()
        print("Comparing all agents for moving targets:: ")
        ph = Ph.ProbabilisticHunting(size, self.terrainprob, self.diffProbDict)
        averageactions = {"Agents1": [], "Agents2": [], "Agents3": [], "Agents4": [], "Agents5": []}
        for i in range(0, interations):
            print("iteration :: " + str(i))
            ph.create_landscape()
            newtarget = ph.settarget()
            ph.probabilitydictionary()
            Agents1actions = ph.mtgamerule1()[2]
            ph.probabilitydictionary()
            ph.target = newtarget
            Agents2actions = ph.mtgamerule2()[2]
            ph.probabilitydictionary()
            ph.target = newtarget
            Agents3actions = ph.mtgamerule3()[2]
            ph.probabilitydictionary()
            ph.target = newtarget
            Agents4actions = ph.mtgamerule4()[2]
            ph.probabilitydictionary()
            ph.target = newtarget
            Agents5actions = ph.mtgamerule5()[2]
            averageactions["Agents1"].append(Agents1actions)
            averageactions["Agents2"].append(Agents2actions)
            averageactions["Agents3"].append(Agents3actions)
            averageactions["Agents4"].append(Agents4actions)
            averageactions["Agents5"].append(Agents5actions)
        for val in averageactions:
            averageactions[val] = np.mean(averageactions.get(val))
        self.disp_data2(averageactions, "Agents", "Actions", "Comparison"
                        + " of all agents")
        print((t.datetime.now() - start_time).seconds)
        plt.show()

    # Comparing search counts for agent 1 and agent 2
    # to find moving target on multiple maps, target is set to original postion for each agent
    def comparetwoagnetsformovingtarget(self, size, interations):
        start_time = t.datetime.now()
        print("Comparing all agents for moving targets:: ")
        ph = Ph.ProbabilisticHunting(size, self.terrainprob, self.diffProbDict)
        averageactions = {"Agents1": [], "Agents2": []}
        for i in range(0, interations):
            print("iteration :: " + str(i))
            ph.create_landscape()
            newtarget = ph.settarget()
            ph.probabilitydictionary()
            Agents1actions = ph.mtgamerule1()[1]
            ph.probabilitydictionary()
            ph.target = newtarget
            Agents2actions = ph.mtgamerule2()[1]
            averageactions["Agents1"].append(Agents1actions)
            averageactions["Agents2"].append(Agents2actions)
        for val in averageactions:
            averageactions[val] = np.mean(averageactions.get(val))
        self.disp_data2(averageactions, "Agents", "Search counts", "Comparison"
                        + " of agent 1 and agent 2")
        print((t.datetime.now() - start_time).seconds)
        plt.show()


"""
Main class is used to iterate over agents with same map, multiple map, comparing each agent 
"""


def main():
    print("Scenarios to Analyse")
    print("1 - Compare Agent 1 and Agent 2 for multiple targets across fixed map")
    print("2 - Compare Agent 1 and Agent 2 across multiple maps")
    print("3 - Compare all Agents across multiple maps")
    print("4 - Compare Agent 1 and Agent 2 Agents multiple maps with moving targets")
    print("5 - Compare all Agents across multiple maps with moving targets")
    print()
    analysistype = int(input("Enter the scenario to analyse from above options (1, 2, 3, 4, 5) "))
    size = int(input("Enter the size: "))
    iterations = int(input("Enter the number of iterations: "))
    terrainprob = [0.2, 0.3, 0.3, 0.2]  # Terrain distribution according to probabilities
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}  # Probabilities used under each unopened block to search target
    pa = ProbabilisticAnalysis(terrainprob, diffProbDict)  # Object creation with terrain and difficulty probability
    if analysistype == 1:
        pa.samemap(size, iterations)  # Agent 1 and Agent 2 to find target on same map
    elif analysistype == 2:
        pa.multiple_map(size, iterations)  # Agent 1 and Agent 2 to find target for on multiple maps
    elif analysistype == 3:
        pa.compareall(size, iterations)  # Comparing all agents to find stable target on multiple maps
    elif analysistype == 4:
        pa.comparetwoagnetsformovingtarget(size, iterations)  # Comparing agent 1 and agent 2 to find moving target
        # on multiple maps
    elif analysistype == 5:
        pa.compareallformovingtarget(size, iterations)  # Comparing all agents to find moving target on multiple maps


if __name__ == '__main__':
    # Runs the main function
    main()
