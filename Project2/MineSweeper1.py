import random
import sys
import tkinter as tk
import math
import matplotlib.pyplot as plt
import datetime as t
from threading import Thread

# increasing recusrion limit
sys.setrecursionlimit(100000)


class MineSweeper1(object):
    """
    In this class, Actual computation and minesweeper generation takes place
    This class creates the basic layout of the minesweeper board using the constructor. It checks if the opened cell is
    safe (S) or a mine (M) and updates the information for each cell accordingly, until all the cells are opened.
    """

    # Constructor with 3 arguments, size of minesweeper, the mine density and the mode
    def __init__(self, size, mdensity, mode):
        self.size = size
        self.mode = mode
        self.mdensity = mdensity

        # Creates the minesweeper board
        self.cells = set((x, y)
                         for x in range(self.size)
                         for y in range(self.size))

        # Getting number of mines
        mines_number = self.getmines()
        self._mines = set()     # to keep track of the mines detected by the agent
        # Setting mines at random locations
        while len(self._mines) < mines_number:
            self._mines.add((random.randrange(size),
                             random.randrange(size)))

        # For each square, gives the set of its neighbours
        # ni = not identified
        # neighbour =  List of neighbors
        # neighbours =  Length of neighbors
        # Status = Status of cell (It can be C = Covered, M = Mined, S = Safe)
        # Clue = Provides number of mines around specific locations
        self.data = {}  # data to keep track of required parameters
        for (x, y) in self.cells:  # for all the cells in the board, get their neighbors and update each cell's data
            neighbour = self.getneighbour(x, y)
            self.data[x, y] = {"neighbour": neighbour, "neighbours": len(neighbour), "status": "C", "clue": "ni"}
        # Environment data:
        self.empty_remaining = size * size - mines_number  # number of non-mines
        # Maintain list of opened cells.
        self.opened = set()
        # flags the identified mine.
        self.flagged = set()
        # Maintain list of safe cells to generate hints.
        self.safe = []
        # Keep track of mines for which all neighbors have been identified
        self.solved = set()
        # If it was a mine, it will be 'mine' instead of a number.
        self.mines_busted = set()

    def open(self, xy):
        """
        Opens the cell at (x, y) location and checks whether it is a mine or safe
        """
        if xy in self.opened:       # if the cell is already open, do nothing
            return

        self.opened.add(xy)  # add to the list of opened cells
        if xy in self._mines:  # if mine, update status to M
            self.mines_busted.add(xy)       # add to mines busted
            self.data.get(xy)["status"] = "M"
        else:
            # Updating the clue
            self.data.get(xy)["status"] = "S"  # otherwise update status as safe
            # Updating clue based on mines found in the cell's neighbors
            self.data.get(xy)["clue"] = len(self.data[xy].get("neighbour") & self._mines)
            self.empty_remaining -= 1  # decrease number of non-mines by 1
            # Checking the condition of winning for test mode, displays the winning scenario
            if self.empty_remaining <= 0 and self.mode == "T":
                self.win()

    def flag(self, xy):
        """
        function to flag (mark) the cell denoted by xy
        """
        self.flagged.add(xy)    # adds the cell to the flagged set

    def getneighbour(self, x, y):
        """
        returns the list of neighbors for the cell (x, y)
        """
        # Check to the left and right of that cell to retrieve its neighbors and return them
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh

    def getmines(self):
        """
        returns the number of mines based on the user input size of the minesweeper board
        """
        # Number of mines is determined by  (mine density * size of the board)
        return math.floor(self.mdensity * (self.size ** 2))

    def updateinformation(self):
        """
        updates the information for the cells in the board
        """
        # for all the cells in the board except the busted mines and flagged cells
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":  # if the clue for the cell is not ni (not identified)
                # Number of hidden cells around (x, y)
                hidden = 0
                # List of hidden cells around (x, y)
                hiddenlist = set()
                # Number of safe cells around (x, y)
                safe = 0
                # List of safe cells around (x, y)
                safelist = set()
                # Number of mine cells around (x, y)
                mine = 0
                # List of mine cells around (x, y)
                minelist = set()

                # Iterating over each neighbor of (x, y) to update the above mentioned list
                for n in self.data.get((x, y)).get("neighbour"):
                    if self.data.get(n).get("status") == "C":       # if the status of the cell is covered
                        hidden += 1         # increase number of hidden cells
                        hiddenlist.add(n)   # add the cell to the hidden list
                    elif self.data.get(n).get("status") == "S":  # if the status of the cell is safe, add to safelist
                        safe += 1  # update no of safe cells
                        safelist.add(n)
                    elif self.data.get(n).get("status") == "M":  # if the cell is a mine, add to minelist
                        mine += 1  # update no of mines detected
                        minelist.add(n)

                # If total number of remaining mines around cell (x,y) equals to total number of hidden cells around
                # (x, y), then it implies that all hidden cells around x, y are mines.
                if hiddenlist:  # if cells exist in hiddenlist
                    # if the clue minus current number of mines detected is equal to the current number of hidden cells
                    if self.data.get((x, y)).get("clue") - mine == hidden:
                        for sn in hiddenlist:
                            self.data.get(sn)["status"] = "M"       # update all those cells as mines
                            # Adding identified mines and flagging it
                            self.flag(sn)
                    # If all mines around x,y have been identified, then all the remaining hidden cells around x, y
                    # are safe.
                    elif (self.data.get((x, y)).get("neighbours") - self.data.get((x, y)).get("clue")) - safe == hidden:
                        for sn in hiddenlist:
                            self.data.get(sn)["status"] = "S"
                            # Adding identified safe cells to the list
                            if sn not in self.opened and sn not in self.safe:
                                self.safe.append(sn)
                else:   # otherwise add cell to the solved list
                    self.solved.add((x, y))
        # Based on updated information, calling method to generate hint
        return self.generatehint()

    def generatehint(self):
        """
        function to generate a hint for the game to proceed, returns the next step for the agent to take
        """

        # If safe list is not empty, give first element in safe list as a hint
        if self.safe:  # if safe
            step = self.safe.pop(0)  # remove the first element from the list
        else:
            # get remaining cells excluding the opened and flagged cells
            permittedsteps = self.cells - self.opened - self.flagged  # get remaining cells excluding the opened and flagged cells
            step = random.choice(list(permittedsteps))  # from these cells, choose one randomly

        return step

    def win(self):
        """
        Display final score after game is completed. final score is #mines flagged/# mines
        """
        # Total number of mines busted by user while playing
        if self.mines_busted:
            print("You finished with %s tripped mines. Final score %s" % (
                len(self.mines_busted), len(self.flagged) / len(self._mines)))


class MineSweeperPlay(MineSweeper1):
    """
    Play the Minesweeper game!
    This class automates the Minesweeper gameplay for the above class using the Tkinter library.
    If the mode is Test, the result is displayed.
    """

    # Constructor
    def __init__(self, *args, **kw):
        # Calling MAIN CLASS
        MineSweeper1.__init__(self, *args, **kw)  # use the __init__ function from the above class to create the board

    def letsplay(self):
        """
        plays the game; starts timer and runs until all cells are opened and returns the time taken in microseconds
        """
        start_time = t.datetime.now()  # Noting time taken for the game to complete
        while self.empty_remaining > 0:  # until all cells are opened
            step = self.updateinformation()     # update the information for the cell
            self.open(step)                     # and open that cell
        # return the final results
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
        for xy in self.cells:       # for all the cells
            squares[xy] = button = tk.Button(table, padx=0, pady=0)     # create buttons for all cells
            row, column = xy
            # expand button to North, East, West, South
            button.grid(row=row, column=column, sticky="news")

            # Scaling the size of button based on the size of minesweeper board
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

        # Updating information for button if it is opened and setting it with a sunken effect
        if xy in self.opened:
            button.config(relief=tk.SUNKEN)

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


def disp_data(data, varnames, xlabel, ylabel, title):
    """
    This method is used to visualize data by displaying the graph
    :param data: data to be plotted
    :param varnames: variables to be plotted
    :param xlabel: x label
    :param ylabel: y label
    :param title: title
    """

    # using the matplotlib library to plot the graphs
    fig = plt.figure()  # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    thiningfactors = list(data.keys())      # get the keys from the data dictionary

    for var in varnames:        # for all the variables to be plotted
        success = list(map(lambda key: round(data.get(key).get(var)), data.keys()))
        ax1.plot(thiningfactors, success, label=var)
    ax1.legend(title="Mines")       # create legends for the graphs
    ax1.grid(True)      # add grid to the graphs


def main(cls):
    """
    Main function to either play the Minesweeper game, or analyze the performance of the player
    """
    # This is used to either analyze the basic minesweeper board or test it
    Mode = input("Select the mode (Analysis/Test) ")
    # if mode is Analysis
    if "analysis".casefold().__eq__(Mode.casefold()):
        # initalize the parameters
        result = {}
        sizes = [30, 40, 50, 60]
        mdenisty = 0.40
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
                game = cls(size, mdenisty, "A")
                # getting the total number of mines, total flagged cells, busted mines and time take once the game is done
                tmines, tflagged, tbusted, timetaken = game.letsplay()
                # Update meanmines, meanflagged, meanbusted, meantimetaken accordingly
                meanmines += tmines
                meanflagged += tflagged
                meanbusted += tbusted
                meantimetaken += round(timetaken / (10 ** 3), 4)
            result[size] = {"meanmines": math.floor(meanmines / iterations), "meanflagged": math.floor(meanflagged / iterations),
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
        game = cls(size, mdensity, "T")
        # Play the game and display the board
        game.letsplay()
        game.display()


if __name__ == '__main__':
    # Runs the main function
    main(MineSweeperPlay)
