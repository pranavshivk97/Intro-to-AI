from random import randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap
import copy as cp


class ProbabilisticHunting:
    """
    This class initializes the landscape. Assign initial probabilities
    It also contains code for agents for stationary target and moving target.
    Methods of agents are called from analysis class to compare agents and draw conclusion.
    """

    # constructor for the landscape  initilaize the parameters for the landscape creation
    def __init__(self, size, probabilities, diffProbDict):
        # size of the landscape
        self.size = size
        # pobabilities of the specific type of terrain in landscape
        self.probabilities = probabilities
        # location of target
        self.target = (0, 0)
        # landscape represented as size x size array
        self.landscape = np.empty((self.size, self.size), dtype=int)
        # dictionary conataining probability of locating the target in a specific cell
        self.targetLocprobabdict = {}
        self.cells = set([])
        # pobabilities of not finding target in specific terrain type
        self.diffProbDict = diffProbDict

    # setting target at randomly choosen location (x,y)
    def settarget(self):
        self.target = randint(0, self.size - 1), randint(0, self.size - 1)
        return self.target

    # Landscape creation
    # num holds a square matrix, rows and columns equal to total size provided by user
    # cells is set of cells in matrix
    def create_landscape(self):
        """
        creates the landscape
        """
        num = [[np.random.choice(np.arange(4), 1, p=self.probabilities)[0] for i in range(self.size)] for j in
               range(self.size)]
        self.cells = set((x, y) for x in range(self.size) for y in range(self.size))
        num_arr = np.array(num)
        self.landscape = num_arr

    def getmanhtdis(self, a, b):
        """
        returns the Manhattan distance between the specified cells
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Updating initial probabilities database
    def probabilitydictionary(self):
        """
        creates a dictionary of probabilities for all the cells in teh board
        """
        # sets the probabilities to 1/size^2
        [[self.targetLocprobabdict.update({(x, y): (1 / self.size ** 2)}) for y in range(self.size)]
         for x in range(self.size)]

    def getcelltosearch(self, valuedict, maxormin):
        """
        gets the cell to search for the target from valuedict
        based on choosing maximum or minimum of value of key
        """
        if maxormin:
            # if max, get the maximum probability among all the cells
            value = max(valuedict.values())
        else:
            # otherwise, get the minimum probability among all the cells
            value = min(valuedict.values())
        # get the list of cells based on the above value
        choices = list(filter(lambda x: valuedict[x] == value, valuedict))
        # randomly choose one of them
        tosearch = choices[randint(0, len(choices) - 1)]
        # and return that as the cell to search
        return tosearch

    def istargetfound(self, celltosearch, difficultprob):
        """
        Check in cell searched contains target,
        if so target can be returned based on probability of terrain of the cell
        """
        success = 0
        # if the cell to be searched is the target
        if celltosearch == self.target:
            # assigns 0 or 1 based on whether the target is found
            success = np.random.choice(np.arange(2), 1, p=[difficultprob, 1 - difficultprob])[0]
        # return that value
        return success

    def getobservation(self, cellsearched, difficultprob):
        """
        return the probability for the observation.
        observbation = target mot present in cell or target present in cell but not found
        """
        # return the probability of the observation from the cell being searched
        observation = 1 - self.targetLocprobabdict.get(cellsearched) + difficultprob * self.targetLocprobabdict.get(
            cellsearched)
        return observation

    # Update the probability for each cell in landscape based on the observation
    # required for all the agents
    def updateprobabilities(self, cellsearched, difficultprob):
        """
        update the probbailities for the cell after failure search result
        cellsearched :: cell searched
        """
        # get the observation from the current cell
        observation = self.getobservation(cellsearched, difficultprob)
        # for every cell in the board
        for cell in self.targetLocprobabdict.keys():
            # if the cell is the that was searched last
            if cell is cellsearched:
                # get the probability from the cell being searched
                p = self.diffProbDict.get(self.landscape[cellsearched[0]][cellsearched[1]])
                # update the probability in the dictionary
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                # otherwise update the probability
                prob = self.targetLocprobabdict.get(cell) / observation
            self.targetLocprobabdict.update({cell: prob})

    def gettargetfoundprobabilities(self):
        """
        return the dictionary conatining the probbailities of finding the target in the cell
        """
        targefoundprobabdict = {}
        # for each cell in the landscape
        for cell in self.targetLocprobabdict.keys():
            # set the probability for all the cells in the board based on the false positive rates
            foundprob = self.targetLocprobabdict.get(cell) * (
                    1 - self.diffProbDict.get(self.landscape[cell[0]][cell[1]]))
            targefoundprobabdict[cell] = foundprob
        return targefoundprobabdict

    def getcellscores(self, currentlocation):
        """
        This function return dictionary conatining the score for cells with maximum probability of finding the target.
        score = Manhattan distance of cell from current location/probabilitiy of fininding the target in the cell
        """
        # dictionary of scores
        cellscores = {}
        # get the dictionary containing the probability of finding the target in the cell
        targefoundprobabdict = self.gettargetfoundprobabilities()
        # take the cell with the maximum value from this dictionary
        maxprobcell = max(targefoundprobabdict.values())
        # get the list of cells which have this probability
        choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
        for cell in choices:
            # calaculate the score using the Manhattan distance for each of these cells and return
            score = (1 + self.getmanhtdis(currentlocation, cell)) / maxprobcell
            cellscores[cell] = score
        return cellscores

    # This one of the implementation of improved agents with one step lookahead prespective
    def getcellusingonesteplookahead(self):
        """
        This function returns "best" cell to search based on one step look ahead computation.
        First cells with maximum probabilities are listed.
        Then for each of these cells observation is calculated assuming that  target in not found in the cell.
        Cells with maximum look-ahead with corresponding choices are listed.
        Out of these cells, cell with minimum score for its look-ahead choices is selected as best cell
        """
        # updated probabilties of finding the target in the cell
        targefoundprobabdict = self.gettargetfoundprobabilities()
        # getting max value
        maxprobcell = max(targefoundprobabdict.values())
        # list of cells with maximum choices
        choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
        # create copy of probability dictionary to compute the look ahead probabilities
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        # initiating max prob for comparison with maximum from lookahead proababilies
        maxprob = 0
        # initiating min score for comparison with score of choices of cells with max lookahead probabilities
        minscore = 0
        # holds list of cells with maximum lookahead probabilities
        bestcells = {}
        celltosearch = ()
        # creates list of cells with maximum lookahead probabilities
        for cell in choices:
            prob, choices = self.onesteplookahead(cell, copylocprobdict)
            if prob >= maxprob:
                bestcells[cell] = {"prob": prob, "choices": choices}
                maxprob = prob
        # for cells in bestcells score for future choices is compare
        # and cell which has future cell with minimum score is selected
        for cell in bestcells.keys():
            prob = bestcells.get(cell).get("prob")
            choices = bestcells.get(cell).get("choices")
            minscoreforcell = min([(1 + self.getmanhtdis(cell, step)) / prob for step in choices])
            if minscore == 0 or minscoreforcell < minscore:
                minscore = minscoreforcell
                celltosearch = cell
        return celltosearch

    def onesteplookahead(self, cell, copylocprobdict):
        """
        This function computes probability
        for a given cell and current probability finding dictionary.
        Once computed it return the max probability and future cells choices for given cell with that max probability
        """
        tempprobdict = copylocprobdict
        # get the probabilities from the cells in the landscape
        p = self.diffProbDict.get(self.landscape[cell[0]][cell[1]])
        # get the observation from that cell
        observation = self.getobservation(cell, p)
        for c in tempprobdict.keys():
            # if the cell is present in the dict
            if c is cell:
                # update the probability of that cell using p and the observation
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                # otherwise, update the probability using only the observation
                prob = self.targetLocprobabdict.get(cell) / observation
            probtofind = prob * (1 - self.diffProbDict.get(self.landscape[c[0]][c[1]]))
            # update the cell's probability in the dictionary
            tempprobdict.update({c: probtofind})
        # find the max probability in the dict
        maxvalue = max(tempprobdict.values())
        # and get the cells having this probability
        choices = list(filter(lambda x: tempprobdict[x] == maxvalue, tempprobdict))
        return maxvalue, choices

    def getcellusingonesteplookaheadscore(self, currentcell):
        """
        This function returns "best" cell to search based on one step look ahead computation.
        First cells with minimum score based on current finding probabilties are listed.
        For each listed cell with minimum score, score for future choices corresponding to that cell are calculated.
        Out of listed cells, cells with minimum score for its look-ahead choices is selected as best cell
        """
        # cells and scores for the cells max finding probabilities
        cellscores = self.getcellscores(currentcell)
        # minscore from the dictionary
        minscore = min(cellscores.values())
        # cells with minimum score
        choices = list(filter(lambda x: cellscores[x] == minscore, cellscores))
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        minscore = 0
        celltosearch = ()
        # calculated future score for the cells with minimum score
        # cell which will have cell with future minimum score is seclected
        for cell in choices:
            minscoreforceell = self.onesteplookaheadscore(cell, copylocprobdict)
            if minscore == 0 or minscoreforceell < minscore:
                minscore = minscoreforceell
                celltosearch = cell
        return celltosearch

    def getcellusingonesteplookaheadscorei(self):
        """
        This function returns "best" cell to search based on one step look ahead computation.
        This is kind of greedy algorithm in the sense in calculates the look ahead probilities and score each cell.
        The cell with a future choice with minium score is selected as best as returned.
        """
        # create copy of probability dictionary to compute the look ahead probabilities and score
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        minscore = 0
        celltosearch = ()
        for cell in self.targetLocprobabdict.keys():
            # min score for the choice
            minscoreofchoice = self.onesteplookaheadscore(cell, copylocprobdict)
            if minscore == 0 or minscoreofchoice < minscore:
                minscore = minscoreofchoice
                # cell with choice with minimum score is selected
                celltosearch = cell
        return celltosearch

    def onesteplookaheadscore(self, cell, copylocprobdict):
        """
        This function is used by "getcellusingonesteplookaheadscorei" to calculate
        look ahead probilities and score each cell.
        """
        # copy of probability dictionary
        tempprobdict = copylocprobdict
        # terrain probability of cell
        p = self.diffProbDict.get(self.landscape[cell[0]][cell[1]])
        # calculating observation for the cell
        observation = self.getobservation(cell, p)
        # calculating updated probability dictionary for givenb cell
        for c in tempprobdict.keys():
            if c is cell:
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                prob = self.targetLocprobabdict.get(cell) / observation
            probtofind = prob * (1 - self.diffProbDict.get(self.landscape[c[0]][c[1]]))
            tempprobdict.update({c: probtofind})
        maxprobcell = max(tempprobdict.values())
        # selected future choices with max probability
        choices = list(filter(lambda x: tempprobdict[x] == maxprobcell, tempprobdict))
        # getting minimum score among the selected future choices for the cell
        minscore = min([(1 + self.getmanhtdis(cell, step)) / prob for step in choices])
        return minscore

    def gamerule1(self):
        """
        Implements agent based on rule1
        Rule1 : Search is just based on target locating probabilities,
        terrain difficulting is not taken in account while searching.
        (Only used for getting observation probability)
        """
        # intitialize the initial location
        currentlocation = (-1, -1)
        # set search count to 0 initially
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get a cell to search
            tosearch = self.getcelltosearch(self.targetLocprobabdict, 1)
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the target cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # if not found, update the probabilities
            self.updateprobabilities(tosearch, p)
            # set the current location to the cell that was just searched
            currentlocation = tosearch

    def gamerule2(self):
        """
        Implements agent based on rule2
        Rule2 : Search is just based on target finding probabilities,
        terrain difficulting is taken in account while searching.
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the probabilities of finding the target in the cells.
            targefoundprobabdict = self.gettargetfoundprobabilities()
            # get a cell to search
            tosearch = self.getcelltosearch(targefoundprobabdict, 1)
            # increment the search count
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the cell currently being searched
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found
            if self.istargetfound(tosearch, p):
                # return the target cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # otherwise update the probabilities
            self.updateprobabilities(tosearch, p)
            # set current location to the cell being searched
            currentlocation = tosearch

    def gamerule3(self):
        """
        Implements agent based on rule3
        Rule3 : closest cell with maximum probability of the finding the target selected every time.
        cell is selcted based on score = Mahanttan dis b/w cell and future choice/probability of finding the target
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get cell score for cell with maximum probability of finding the target
            cellscore = self.getcellscores(currentlocation)
            # cell with minimum score is selected
            tosearch = self.getcelltosearch(cellscore, 0)
            # update searchcount
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the cell currently being searched
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search action
                return tosearch, searchcount, travellingactions + searchcount
            # otherwise update the probabilities
            self.updateprobabilities(tosearch, p)
            # set the current location to the cell that was just searched
            currentlocation = tosearch

    def gamerule4(self):
        """
        Improved agent based one step look ahead approach using finding probabilities and score.
        cell (out of the cell with maximum current probabilitties) which if fails can result
        in best future choice (one with maximum target finding probability and min score)
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the cell to search based on one step look ahead probabilities and scores
            tosearch = self.getcellusingonesteplookahead()
            # update searchcount
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the cell currently being searched
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # otherwise update the probabilities
            self.updateprobabilities(tosearch, p)
            # set the current location to the cell that was just searched
            currentlocation = tosearch

    def gamerule5(self):
        """
        Improved agent based one step look ahead approach using scores.
        cell (out of the cell with minimum score based on current probabilitties) which if fails can result in
        best future choice (one with min score) is selected
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the cell to search based on one step look ahead scores
            tosearch = self.getcellusingonesteplookaheadscore(currentlocation)
            # update searchcount
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the cell currently being searched
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # otherwise update the probabilities
            self.updateprobabilities(tosearch, p)
            # set the current location to the cell that was just searched
            currentlocation = tosearch

    def gamerule6(self):
        """
        Improved agent based one step look ahead greedy approach.
        cell which if fails can result in best future choice (one with min score) is selected.
        here like previous method best cells based on scenario is not shortlisted for one step look
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the cell to search based on one step look ahead scores for each cell
            tosearch = self.getcellusingonesteplookaheadscorei()
            # update searchcount
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the cell currently being searched
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # otherwise update the probabilities
            self.updateprobabilities(tosearch, p)
            # set the current location to the cell that was just searched
            currentlocation = tosearch

    # ############################################################ PART 2
    # ################################################

    def movetarget(self):
        """
        This function is used for the second part of the project to move the target for each search step.
        target is moved by one step to the neighboring cells
        """
        x, y = self.target[0], self.target[1]
        neigh = [(nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                 (nx, ny) in self.cells]
        nextstep = neigh[randint(0, len(neigh) - 1)]
        self.target = nextstep

    def iswithin5(self, currentlocation):
        """
        This function is used check if current location is with in 5 Manhattan distance of the target
        """
        if self.getmanhtdis(currentlocation, self.target) <= 5:
            return True
        return False

    def getcellclust(self, currentlocation):
        """
        This function divide the landscape in two parts: cells within 5 Manhattan distance of current location and
        the cells which are outside 5 Manhattan distance parameter of current location
        """
        within5cells = set()
        outof5cells = set()
        for cell in self.cells:
            if self.getmanhtdis(currentlocation, cell) <= 5:
                within5cells.add(cell)
            else:
                outof5cells.add(cell)
        return within5cells, outof5cells

    def updateprobabilitydictionary(self, listcell, cellsearched, difficultprob, useobservation):
        """
        Update the probabilitiy of locating the target.

        For all cells except the cells inside list cell probabilibity is assigned as zero.

        useobservation is true if cellsearched is in listcell which is "within5cells",
        for this cells observation is computed as there were chances that target is in cellseached

        useobservation is false if listcell is "outof5cells", as we definately know for current situation
        target in not cell searched and probabiliting of locating target is uniformly distributed among cells of list
        "outof5cells"
        """
        # size of listcell
        size = len(listcell)
        # assigning basic probabilities of loacting the target for cells in listcell,
        # while for all other cell probability of locating target as per current observation is zero
        for cell in self.cells:
            if cell in listcell:
                self.targetLocprobabdict.update({cell: (1 / size ** 2)})
            else:
                self.targetLocprobabdict.update({cell: 0})
        # based on useobservation observation is calculated and pribabilities are updated
        if useobservation:
            observation = self.getobservation(cellsearched, difficultprob)
            for cell in listcell:
                # if the cell is the one being currently searched
                if cell is cellsearched:
                    # get the probability from the cell being searched
                    prob = (self.targetLocprobabdict.get(cell) * difficultprob) / observation
                else:
                    # otherwise update the probability
                    prob = self.targetLocprobabdict.get(cell) / observation
                self.targetLocprobabdict.update({cell: prob})

    def mtgamerule1(self):
        """
        Implements agent based on rule1 for moving target
        Rule1 : Search is just based on target locating probabilities,
        terrain difficulting is not taken in account while searching.
        (Only used for getting observation probability)
        """
        # intitialize the current location
        currentlocation = (-1, -1)
        # set search count to 0 initially
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get a cell to search
            tosearch = self.getcelltosearch(self.targetLocprobabdict, 1)
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # set the current location to the cell that was just searched
            currentlocation = tosearch
            # move target
            self.movetarget()
            # check if target is with in 5 Manhattan distance of current location
            if self.iswithin5(currentlocation):
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[0]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, True)
            else:
                # if no set useobservation as false pass cells outside  5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[1]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, False)

    def mtgamerule2(self):
        """
        Implements agent based on rule2 for moving target
        Rule2 : Search is just based on target finding probabilities,
        terrain difficulting is taken in account while searching.
        """
        # intitialize the current location
        currentlocation = (-1, -1)
        # set search count to 0 initially
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the probabilities of finding the target in the cells.
            targefoundprobabdict = self.gettargetfoundprobabilities()
            # get a cell to search
            tosearch = self.getcelltosearch(targefoundprobabdict, 1)
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # set the current location to the cell that was just searched
            currentlocation = tosearch
            # move target
            self.movetarget()
            # check if target is with in 5 Manhattan distance of current location
            if self.iswithin5(currentlocation):
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[0]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, True)
            else:
                # if no set useobservation as false pass cells outside  5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[1]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, False)

    def mtgamerule3(self):
        """
        Implements agent based on rule3 for mocing target
        Rule3 : closest cell with maximum probability of the finding the target selected every time.
        cell is selcted based on score = Mahanttan dis b/w cell and future choice/probability of finding the target
        """
        # intitialize the current location
        currentlocation = (-1, -1)
        # set search count to 0 initially
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get cell score for cell with maximum probability of finding the target
            cellscore = self.getcellscores(currentlocation)
            # get a cell to search
            tosearch = self.getcelltosearch(cellscore, 0)
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # set the current location to the cell that was just searched
            currentlocation = tosearch
            # move target
            self.movetarget()
            # check if target is with in 5 Manhattan distance of current location
            if self.iswithin5(currentlocation):
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[0]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, True)
            else:
                # if no set useobservation as false pass cells outside  5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[1]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, False)

    def mtgamerule4(self):
        """
        Improved agent based one step look ahead approach using scores.
        cell (out of the cell with minimum score based on current probabilitties) which if fails can result in
        best future choice (one with min score) is selected
        """
        # intitialize the current location
        currentlocation = (-1, -1)
        # set search count to 0 initially
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the cell to search based on one step look ahead probabilities and scores
            tosearch = self.getcellusingonesteplookahead()
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # set the current location to the cell that was just searched
            currentlocation = tosearch
            # move target
            self.movetarget()
            if self.iswithin5(currentlocation):
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[0]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, True)
            else:
                # if no set useobservation as false pass cells outside  5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[1]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, False)

    def mtgamerule5(self):
        """
        Improved agent based one step look ahead approach using scores.
        cell (out of the cell with minimum score based on current probabilitties) which if fails can result in
        best future choice (one with min score) is selected
        """
        # set the initial location to (-1, -1)
        currentlocation = (-1, -1)
        # set search counts to 0
        searchcount = 0
        # set travelling action to 0
        travellingactions = 0
        while True:
            # get the cell to search based on one step look ahead scores
            tosearch = self.getcellusingonesteplookaheadscore(currentlocation)
            # increment number of search counts
            searchcount += 1
            # add the Manhattan distance from the current location to the cell to be searched
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            # get the probability from the false negative rates
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            # if target is found in that cell
            if self.istargetfound(tosearch, p):
                # return the cell, search counts, search actions
                return tosearch, searchcount, travellingactions + searchcount
            # set the current location to the cell that was just searched
            currentlocation = tosearch
            # move target
            self.movetarget()
            if self.iswithin5(currentlocation):
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[0]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, True)
            else:
                # if yes set useobservation as true pass cells with in 5 manhattan distance of current location
                # to update probabilities for
                cellstoupdate = self.getcellclust(currentlocation)[1]
                self.updateprobabilitydictionary(cellstoupdate, currentlocation, p, False)

    # Landscape Display GUI based
    # Coloring based on the probabilities assigned to each block
    # white : plain, grey: Hills, green : Forest, charcoal : Caves
    def display_landscape(self):
        """
        displays the landscape
        """
        # define the colors for each cell in the landscape
        cmap = ListedColormap(['#FFFFFF', '#A0A0A0', '#009900', '#404040'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(self.landscape, cmap=cmap, norm=norm)
        ax.set_title(
            "Size :: " + str(self.size))
        ax.set_xticks(np.arange(-0.5, self.size, 1))
        ax.set_yticks(np.arange(-0.5, self.size, 1))
        ax.set_xticklabels(np.arange(0, self.size + 1, 1), rotation=90, horizontalalignment="center")
        ax.set_yticklabels(np.arange(0, self.size + 1, 1), horizontalalignment="center")
        ax.text(self.target[1], self.target[0], "X", ha="center", va="center", color="#990000", fontsize=20)
        ax.grid(color='k', linestyle='-', linewidth=2)


# this method is used to test individual agents. for analysis all agents will be called
# from ProbabiliisticAnalysis class
def main():
    input1 = int(input("Enter the size: "))
    # The map is divided with theses probabilities, equalling total to 1
    # 0.2 : plain, 0.3 : Hills, 0.3 : Forest, 0.2 : Caves
    prob = [0.2, 0.3, 0.3, 0.2]
    # Probabilities of not finding target in specific terrain type
    # 0 : plain, 1: Hills, 2 : Forest, 3 : Caves
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}
    landscape = ProbabilisticHunting(input1, prob, diffProbDict)  # object creation and assigning values
    landscape.create_landscape()
    landscape.settarget()
    landscape.display_landscape()
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 1" + str(landscape.gamerule1()))  # Agent 1
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 2" + str(landscape.gamerule2()))  # Agent 2
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 3" + str(landscape.gamerule3()))  # Agent 3
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 4" + str(landscape.gamerule4()))  # Agent 4
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 5" + str(landscape.gamerule5()))  # Agent 5
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for 6" + str(landscape.gamerule6()))  # Agent 6
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for mt 1" + str(landscape.mtgamerule1()))  # Agent 1
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for mt 2" + str(landscape.mtgamerule2()))  # Agent 2
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for mt 3" + str(landscape.mtgamerule3()))  # Agent 3
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for mt 4" + str(landscape.mtgamerule4()))  # Agent 4
    landscape.probabilitydictionary()
    print()
    print("target cell and actions for mt 5" + str(landscape.mtgamerule5()))  # Agent 4
    plt.show()


# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main()
