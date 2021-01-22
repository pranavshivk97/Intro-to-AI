import random
import sys
import tkinter as tk
import math
import matplotlib.pyplot as plt
import datetime as t
import copy as cp
import numpy as np

# increasing recusrion limit
sys.setrecursionlimit(100000)


class MineSweeper3(object):
    """
    In this class, Actual computation and minesweeper generation takes place
    This class creates the basic layout of the minesweeper board using the constructor. It checks if the opened cell is
    safe (S) or a mine (M) and updates the information for each cell accordingly, until all the cells are opened.
    """

    # Constructor with 4 arguments, size of minesweeper board, mine density, agent to be used and the mode of play
    def __init__(self, size, mdensity, agent, mode):
        self.size = size
        self.mode = mode
        self.agent = agent
        self.mdensity = mdensity
        self.variables = set()
        self.variabledic = {}
        self.solutions = []
        self.constraints = []

        # Create minesweeper board
        self.cells = set((x, y)
                         for x in range(self.size)
                         for y in range(self.size))

        # Getting Number of mines
        mines_number = self.getmines()
        self._mines = set()
        # Setting mines at random location
        while len(self._mines) < mines_number:
            self._mines.add((random.randrange(size),
                             random.randrange(size)))

        # For each square, gives the set of its neighbours
        # ni = not identified
        # neighbour =  List of neighbors
        # neighbours =  Length of neighbors
        # Status = Status of cell(It can be C= Covered, M= Mined, S= Safe)
        # Clue = Provides Number of mines around specific location
        self.data = {}
        for (x, y) in self.cells:
            neighbour = self.getneighbour(x, y)
            self.data[x, y] = {"neighbour": neighbour, "neighbours": len(neighbour), "status": "C", "clue": "ni"}
        # Environment data:
        self.empty_remaining = size * size - mines_number
        # Maintain list of open cells.
        self.opened = set()
        # flagged the identified mine.
        self.flagged = set()
        # Maintain list of safe cells to generate hints.
        self.safe = []
        # track of cells which are completely solved i.e all neighbours are identified.
        self.solved = set()
        # It it was a mine, it will be 'mine' instead of a number.
        self.mines_busted = set()

    def open(self, xy):
        """
        Opens the cell at x, y location and checks if it is a mine or safe
        """
        if xy in self.opened:       # if the cell is already opened, do nothing
            return
        # After opening the block, if the block is not already present in the opened set.
        # Then below condition will add it
        self.opened.add(xy)  # add to the list of opened cells
        if xy in self._mines:  # if mine, update status to M
            self.mines_busted.add(xy)       # add the opened cell to the mines busted list
            self.data.get(xy)["status"] = "M"
        else:
            # Updating the clue
            self.data.get(xy)["status"] = "S"  # otherwise update status to S
            # Updating clue based on mines found in neighbors
            self.data.get(xy)["clue"] = len(self.data[xy].get("neighbour") & self._mines)
            # Reducing the number of non mine cells remaining
            self.empty_remaining -= 1
            # Checking the condition of winning
            if self.empty_remaining <= 0 and self.mode == "T":
                self.win()

    def flag(self, xy):
        """
        Flags the cell xy
        """
        self.flagged.add(xy)        # add the cell to the flagged set

    def getneighbour(self, x, y):
        """
        returns list of neighbors for the cell (x, y)
        """
        # check to the left and right of that cell to get the neighbors of that cell
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh        # return those cells

    def getmines(self):
        """
        returns the number of mines based on the user input size of the minesweeper board
        """
        # number of mines is determined by the mine density times the size of the board
        return math.floor(self.mdensity * (self.size ** 2))

    def createconstraint(self):
        """
        updates the constraint for the cells in the board
        """
        listconst = []
        # for all the cells in the board except the busted mines and flagged cells
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":  # if the clue for the cell is not ni (not identified)
                # List of hidden cells around (x, y)
                hiddenlist = set()
                # count of mine cells around (x, y)
                mine = 0
                # Iterating over each neighbor of (x, y) to update the above mentioned list
                for n in self.data.get((x, y)).get("neighbour"):
                    if self.data.get(n).get("status") == "C":       # if the cell is covered, add it to the hidden list
                        hiddenlist.add(n)
                    elif self.data.get(n).get("status") == "M":  # if the cell is a mine, add to minelist
                        mine += 1  # update number of mines detected
                # if cells exist in the hidden list and the constraint with the elements in hidden list and the value
                # of the difference between the clue and mines doesn;t already exist in the list of constraints
                if hiddenlist and {"const": sorted(list(hiddenlist)),
                                   "val": self.data.get((x, y)).get("clue") - mine} not in listconst:
                    # add to the list of constraints
                    listconst.append(
                        {"const": sorted(list(hiddenlist)), "val": self.data.get((x, y)).get("clue") - mine})
                else:
                    self.solved.add((x, y))     # otherwise add to the solved list
        # return the list of constraints
        return listconst

    def setvariables(self, constr):
        """
        returns a list of all the variables in the constraint equations
        """
        self.variables.clear()      # clear the pre-existing variables, if any
        for const in constr:        # for all the constraints
            [self.variables.add(i) for i in const.get("const")]     # extract the constraint variables and add to a list

    def getconstraint(self):
        """
        returns a deep copy of the list of constraints
        """
        return cp.deepcopy(self.constraints)

    def getsolutions(self):
        """
        return a copy of the solutions for the constraints
        """
        solutions = self.solutions.copy()
        self.solutions.clear()      # clear the pre-existing solutions, if any
        return solutions

    def appendsolution(self, solution):
        """
        adds the current solution to the list of existing solutions
        """
        self.solutions.append(solution)

    def backtrackingsearch(self):
        """
        function to implement the backtracking search
        """
        self.constraints = self.createconstraint()      # create the list of constraints
        self.setvariables(self.getconstraint())         # extract the variables from these constraints
        if self.agent == "IP":      # if the agent is the Improved Probabilistic (IP) agent
            self.getvardictionary()     # get the variables along with their frequencies in the constraints
        self.recursivebacktracking({})          # start the recursive backtracking method

    def recursivebacktracking(self, assignment):
        """
        function for the recursive backtrack search
        """
        # if the number of assigned variables is same as the total number of variables
        if len(assignment.keys()) == len(self.variables):
            return assignment       # return the variables
        # if the agent is the Probabilistic (P)
        if self.agent == "P":
            # pop off the first element from the variables that aren't assigned yet
            var = sorted(list(self.variables - assignment.keys())).pop(0)
        # otherwise if the agent is the Improved Probabilistic (IP) one
        elif self.agent == "IP":
            var = self.customgetvar(assignment)     # choose the most constrained variable in the constraint
        # since the cell can either be safe (0) or a mine (1)
        for value in [0, 1]:
            assignment.update({var: value})     # update the variable with the corresponding value
            c = self.check_constraint(assignment)       # check if the constraint is satisfied or not
            if c:       # if the constraints are satisfied
                result = self.recursivebacktracking(assignment)     # recursively update the assignment dictionary
                if result != "failure":
                    self.appendsolution(result.copy())      # add the result to the exisyting solutions
            assignment.pop(var)     # remove that variable from assignment
        return "failure"        # if nothing works out, return failure

    def check_constraint(self, assignment):
        """
        checks if the constraints are satisfied or violated
        """
        # get the list of constraints
        csp2 = self.getconstraint()

        # for all the variables in the assigned variable dictionary
        for v in assignment:
            # and for all the constraints
            for const in csp2:
                # if the variable exists in the constraint and the value of the variable is 0
                if v in const.get("const") and assignment.get(v) == 0:
                    const.get("const").remove(v)        # remove that variable from the constraint equation
                    # if the number of variables in any constraint equation is less than the constraint equation's value
                    if len(const.get("const")) < const.get("val"):
                        return False        # constraint is violated
                # otherwise, if the variable exists in the constraint equation and the value of the variable is 1
                elif v in const.get("const") and assignment.get(v) == 1:
                    const.get("const").remove(v)        # remove that variable from the constraint
                    const["val"] = const.get("val") - 1     # decrement the value of the constraint
                    if const.get("val") < 0:        # if the value of the ocnstraint is negative
                        return False        # constraint is violated
        return True     # otherwise, the constraint is satisfied

    def giveprobability(self):

        """
        function to give the probabilities of a cell's neighbors
        """
        result = self.getsolutions()        # get the solutions for the constraint equations
        deno = len(result)      # number of constraint variables
        dictprob = {}       # dictionary to store the probabilities for the cells
        # initialize a 2D array of zeros for the solution
        solArray = np.zeros((len(result), len(self.variables)), int)
        if result:
            for index, sol in enumerate(result):
                # store the solutions of the equations in solArray
                solArray[index] = [sol.get(i) for jndex, i in enumerate(sol)]

            if self.mode == "IP":  # for triply improved agent
                solArray = self.validsolution(solArray)

            for i, var in enumerate(result[0]):
                # calculate the probabilities for the cell's neighbors
                prob = round(np.sum(solArray[:, i]) / deno, 2)
                dictprob.update({var: prob})        # add to dictprob and return it
        return dictprob

    def processprobability(self, dictprob):
        """
        function to check if a mine is safe/mine based on the probability and decide the next step
        for the agent to follow
        """
        # for all the cell's neighbors' probabilities
        for cell in dictprob:
            # if the probability is 0, mark as safe (S)
            if dictprob.get(cell) == 0:
                if cell not in self.safe:       # if the cell is not already in the safe list
                    self.data.get(cell)["status"] = "S"     # mark as Safe
                    self.safe.append(cell)      # add to safe list
            elif dictprob.get(cell) == 1:       # otherwise if the probability is 1
                self.data.get(cell)["status"] = "M"     # mark as a mine (M)
                self.flag(cell)         # add to the flagged list
        if self.safe:       # if elements exist in the safe list
            nextstep = self.safe.pop(0)     # remove the first element and set as the next step the agent should follow
            step = nextstep
        elif not self.safe:     # otherwise if the safe list is empty
            if dictprob:        # if dictprob holds values
                minprob = min(dictprob.values())        # choose the minimum probability
                # check for cells with that minimum probability
                res = list(filter(lambda x: dictprob[x] == minprob, dictprob))
                step = res.pop(0)       # get the first element from those cells and set to next step
            else:
                # otherwise, get the permitted steps by chekcing the remaining covered (hidden) cells
                permittedsteps = self.cells - self.opened - self.flagged
                step = random.choice(list(permittedsteps))  # from these cells, choose one randomly
        return step

    def probabilisticsolver(self):
        """
        function to implement the probablistic solver using knowledge base
        """
        # recursively update the values of the constraint variables
        self.backtrackingsearch()
        probabs = self.giveprobability()        # get the probabilities of the variables
        suggestion = self.processprobability(probabs)       # get a suggestion based on whether the cell is safe or a mine
        return suggestion

    def validsolution(self, solArray):
        """
        extracts the valid solutions from the entire solution set
        """
        validSolArray = []
        # for all the rows of the solution array
        for i in range(solArray.shape[0]):
            # if the sum of values along the columns is less than or equal to the number of covered cells
            if np.sum(solArray[i, :]) <= (len(self._mines) - (len(self.flagged) + len(self.mines_busted))):
                validSolArray.append(solArray[i, :])        # add to the valid solution array
        return np.array(validSolArray)      # return the valid solution array

    def getvardictionary(self):
        """
        function to create a dictionary storing the constraint variables and their frequencies
        """
        varsortdic = {}
        variablesset = self.variables       # get the list of variables
        for var in variablesset:        # for each variable
            for const in self.getconstraint():      # for each constraint in the list of constraints
                # if the variable exists in the constraint equation
                if var in const.get("const"):
                    # if the variable already exists in the sorted variable dictionary
                    if var in varsortdic.keys():
                        # get the variable's value from the dictionary and update it's value
                        temp = varsortdic.get(var)
                        varsortdic.update({var: (temp + const.get("val"))})
                    else:
                        # otherwise, add the variable adn its corresponding value to the dictionary
                        varsortdic.update({var: const.get("val")})
            self.variabledic = varsortdic

    def customgetvar(self, assignments):
        """
        function to choose the most constrained variable
        """
        # create a copy of the variable dictionary
        variabledic = cp.deepcopy(self.variabledic)
        # for all the assigned variables
        for var in assignments:
            # if that variable exists in the variable dictionary
            if var in variabledic:
                variabledic.pop(var)        # remove the variable from the dictionary
        # get the maximum value of the keys from the dictionary
        # and get the variables which have this value. These are the most constrained variables
        maxconstvar = max(variabledic.values())
        res = list(filter(lambda x: variabledic[x] == maxconstvar, variabledic))
        return res.pop(0)       # return the first element from these

    def win(self):
        """
        Display final score after game is completed. final score is #mines flagged/# mines
        """
        # Total number of mines busted by user while playing
        if self.mines_busted:
            print("You finished with %s tripped mines. Final score %s" % (
                len(self.mines_busted), len(self.flagged) / len(self._mines)))


class MineSweeper3Play(MineSweeper3):
    """
    Play the Minesweeper game!
    This class automates the playing of minesweeper based on hints for the above class using the Tkinter library.
    Based on 'Test' it also displays the results
    """

    # Constructor
    def __init__(self, *args, **kw):
        # Calling MAIN CLASS
        MineSweeper3.__init__(self, *args, **kw)  # use the __init__ function from the above class to create the board

    def letsplay(self):
        """
        plays the game; starts timer and runs until all cells are opened and returns the time taken in microseconds
        """
        start_time = t.datetime.now()  # Noting time taken to complete
        while self.empty_remaining > 0:  # until all cells are opened
            step = self.probabilisticsolver()
            self.open(step)
        return len(self._mines), len(self.flagged), len(self.mines_busted), (t.datetime.now() - start_time).microseconds

    def display(self):
        """
        displays the GUI for the game, using the Tkinter library
        """

        # Creating window and adding properties to it
        window = tk.Tk()
        table = tk.Frame(window)
        table.pack()
        squares = {}

        # Build buttons
        for xy in self.cells:       # create buttons for all the cells
            squares[xy] = button = tk.Button(table, padx=0, pady=0)
            row, column = xy
            # expand button to North, East, West, South
            button.grid(row=row, column=column, sticky="news")

            # Scaling the size of button based on the sie of minesweeper
            scale = math.floor(50 // (1 if self.size // 10 == 0 else self.size // 10))
            table.grid_columnconfigure(column, minsize=scale)
            table.grid_rowconfigure(row, minsize=scale)
            # needed to restore bg to default when unflagging
            self.refresh(xy, squares)

        # Displaying final score
        window.title("You finished with %s tripped mines. Final score %s" % (
            len(self.mines_busted), len(self.flagged) / len(self._mines)))
        window.mainloop()

    def refresh(self, xy, squares):
        """
        Update the GUI for given square
        """
        button = squares[xy]

        # Fetching and setting visual data for the cell
        text, fg, bg = self.getvisualdataforcell(xy)
        button.config(text=text, fg=fg, bg=bg)

        # Updating information for button if it is opened
        if xy in self.opened:
            button.config(relief=tk.SUNKEN)     # set the button to be sunken once it is opened

    def getvisualdataforcell(self, xy):
        """
        Fetching Visual data for cell based on its status
        """
        # If cell is opened and it is mine, it will be marked as a mine. Else, the clue will be displayed.
        if xy in self.opened:
            if xy in self._mines:
                return u'\N{SKULL AND CROSSBONES}', None, 'red'

            mn = self.data.get(xy).get("clue")
            if mn >= 0:
                # Standard minesweeper colors
                fg = {0: 'black', 1: 'blue', 2: 'dark green', 3: 'red',
                      4: 'dark blue', 5: 'dark red',
                      }.get(mn, 'black')
                return str(mn), fg, 'white'

        # if xy is in flagged
        elif xy in self.flagged:
            # display a white flag
            return u'\N{WHITE FLAG}', None, 'green'
        # For remaining cells, they will be just green
        elif xy in self._mines:
            self.flagged.add(xy)
            return u'\N{WHITE FLAG}', None, 'green'
        else:
            # display green cell
            return '', None, 'green'


def disp_data(data, varnames, xlable, ylabel, title):
    """
    This method is used to visualize data by displaying the graph
    :param data: data to be plotted
    :param varnames: variables to be plotted
    :param xlable: x label
    :param ylabel: y label
    :param title: title
    """
    # using matplotlib to initiaalize parameters in order to plot the graphs
    fig = plt.figure()  # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    thiningfactors = list(data.keys())

    for var in varnames:
        # get the data to plot
        success = list(map(lambda key: round(data.get(key).get(var)), data.keys()))
        ax1.plot(thiningfactors, success, label=var)
    ax1.legend(title="Mines")       # set the legend for the graphs
    ax1.grid(True)      # set a grid for the graphs


def main(cls):
    """
    Main function to either play the Minesweeper game, or analyze the performance of the player
    """
    # This is used to either analyze the basic minesweeper board or test it
    Mode = input("Select the mode (Analysis/Test) ")
    # if mode is Analysis
    if "analysis".casefold().__eq__(Mode.casefold()):
        # initialize the parameters for the board
        result = {}
        sizes = [8, 10, 12, 15]
        mdenisty = 0.2
        # (P:Probabilictic / IP:Improved Probabilistic)
        agent = "IP"
        iterations = 5
        print("Generating Data")
        # for the sizes defined above
        for size in sizes:
            # Avg total number of mines
            meanmines = 0
            # Avg total number of flagged mines
            meanflagged = 0
            # Avg total number of busted mines
            meanbusted = 0
            # Avg time taken
            meantimetaken = 0
            # Plays the game "iterations" number of times
            for i in range(0, iterations):
                game = cls(size, mdenisty, agent, "A")
                # Get the total number of mines, flagged cells, mines busted and time taken once the game is completed
                tmines, tflagged, tbusted, timetaken = game.letsplay()
                # Update meanmines, meanflagged, meanbusted, meantimetaken accordingly
                meanmines += tmines
                meanflagged += tflagged
                meanbusted += tbusted
                meantimetaken += round(timetaken / (10 ** 3), 4)
            result[size] = {"meanmines": math.floor(meanmines / iterations),
                            "meanflagged": math.floor(meanflagged / iterations),
                            "meanbusted": math.floor(meanbusted / iterations),
                            "meantimetaken": math.floor(meantimetaken / iterations)}
        print("Plotting Data")
        # displays the graph for the parameters mentioned above
        disp_data(result, ["meanmines", "meanflagged", "meanbusted"], "Sizes", "Numbers", "Size vs efficiency")
        disp_data(result, ["meantimetaken"], "Sizes", "Time( MilliSeconds )", "Size vs Time taken")
        plt.show()
    else:  # if the mode is Test
        # Ask user for input size
        size = int(input("Enter the size "))
        mdensity = float(input("Enter the mine density (0 - 1) "))
        agent = input("Enter the Agent type (P:Probabilictic/IP:Improved Probabilistic) ")
        game = cls(size, mdensity, agent, "T")
        # Play the game and display the board
        game.letsplay()
        game.display()


if __name__ == '__main__':
    # Runs the main function
    main(MineSweeper3Play)
