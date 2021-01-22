import numpy as np
import random
import math


class Field:
    """
    class to create the field in which the dog bots and the sheep are in
    """

    def __init__(self):
        """
        initializes the class with the layout of the field and the positions of the bots and the sheep
        """
        # set the field layout
        self.field = np.zeros((7, 7))

        # set empty positions for the bots and the sheep
        self.d1_pos = []
        self.d2_pos = []
        self.s_pos = []

        # to keep track of the previous positions of the dog bots and sheep
        self.d1_posns, self.d2_posns, self.s_posns = [], [], []

        # runs the configuration provided in the example
        self.paper_config()
        # sets random indices for the field
        # self.set_rand_index()

    def paper_config(self):
        """
        sets the field according to the configuration provided in the question; can also be modified to set
        different locations
        """
        # set indices for the bots and sheep
        self.d1_pos, self.d2_pos, self.s_pos = (0, 6), (6, 3), (4, 0)
        # self.d1_pos, self.d2_pos, self.s_pos = (3, 2), (2, 3), (6, 0)
        # store in the list
        self.d1_posns, self.d2_posns, self.s_posns = [self.d1_pos], [self.d2_pos], [self.s_pos]
        # display the field
        self.set_pos()

    def set_rand_index(self):
        """
        sets random indices for the bots and field
        """
        # set random indices for the bots and sheep
        # self.d1_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        self.d1_pos, self.d2_pos = (3, 4), (4, 3)
        # self.d2_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        self.s_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))

        # if any of the positions coincide, reassign all
        while self.d1_pos == self.d2_pos or self.d1_pos == self.s_pos or self.d2_pos == self.s_pos:
            self.d1_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
            self.d2_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
            self.s_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        print(self.d1_pos, self.d2_pos, self.s_pos)

        # store the current position
        self.d1_posns, self.d2_posns, self.s_posns = [self.d1_pos], [self.d2_pos], [self.s_pos]
        # display the field
        self.set_pos()

    def set_pos(self):
        """
        displays the field with updated locations
        1 - Dog Bot 1, 2 - Dog Bot 2, 3 - Sheep
        """
        # set the position of the bots and sheep in the field
        self.field[self.d1_pos] = 1
        self.field[self.d2_pos] = 2
        self.field[self.s_pos] = 3
        # print the positions
        print("DOG BOT 1 Positions: ", self.d1_posns)
        print("DOG BOT 2 Positions: ", self.d2_posns)
        print("SHEEP Positions: ", self.s_posns)
        # display the field
        print(self.field)

    def neighbors(self, pos, obstacles):
        """
        returns neighboring cells based on the position, if there are obstacles (other bot or sheep)
        in the neighboring cells, won't return those
        :param pos: current position
        :param obstacles: dog bot and sheep
        """
        # get the indices of the current position
        i, j = pos[0], pos[1]
        # if the sheep and dog bots are not coinciding
        if self.field[i][j] not in obstacles:
            # check the corners
            if pos in [(0, 0), (6, 6), (0, 6), (6, 0)]:
                # top left corner
                if pos == (0, 0):
                    # get neighbors for that location
                    neighbors = self.get_neighbor([(0, 1), (1, 0)], i, j, obstacles)
                # bottom right corner
                elif pos == (6, 6):
                    # get neighbors for that location
                    neighbors = self.get_neighbor([(6, 5), (5, 6)], i, j, obstacles)
                # top right corner
                elif pos == (0, 6):
                    # get neighbors for that location
                    neighbors = self.get_neighbor([(1, 6), (0, 5)], i, j, obstacles)
                # bottom left corner
                elif pos == (6, 0):
                    # get neighbors for that location
                    neighbors = self.get_neighbor([(5, 0), (6, 1)], i, j, obstacles)
            # check the middle of the field
            elif 0 < i < 6 and 0 < j < 6:
                # get neighboring cells
                neighbors = self.get_neighbor([(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)], i, j, obstacles)
            # check if it is the top edge
            elif i == 0 and 0 < j < 6:
                # get neighboring cells
                neighbors = self.get_neighbor([(i + 1, j), (i, j - 1), (i, j + 1)], i, j, obstacles)
            # check if left edge
            elif j == 0 and 0 < i < 6:
                # get neighboring cells
                neighbors = self.get_neighbor([(i - 1, j), (i + 1, j), (i, j + 1)], i, j, obstacles)
            # check if right edge
            elif i == 6 and 0 < j < 6:
                # get neighboring cells
                neighbors = self.get_neighbor([(i - 1, j), (i, j - 1), (i, j + 1)], i, j, obstacles)
            # check if bottom edge
            elif j == 6 and 0 < i < 6:
                # get neighboring cells
                neighbors = self.get_neighbor([(i + 1, j), (i - 1, j), (i, j - 1)], i, j, obstacles)

        # return the list of neighboring cells
        return neighbors

    def sheep(self):
        """
        function to move the sheep
        """
        # get the neighboring cells for the sheep ([1, 2] denotes the positions where the dog bots are located currently
        neighbors = self.neighbors(self.s_pos, [1, 2])
        print(neighbors)
        # if there are no neighbors, meaning either the sheep is pinned at a corner or the goal
        if not neighbors:
            # stay at the same position
            print("Sheep is at the same position")
            mov = self.s_pos
        # otherwise, if neighbors exist, there are cells for the sheep to move to
        else:
            # randomly choose from one of the neighbors
            mov = random.choice(neighbors)
        # if the chosen move coincides with the positions of the dog bots
        while mov == self.d1_pos or mov == self.d2_pos:
            # randomly choose from one of the neighbors again
            mov = random.choice(neighbors)
        # set the current position of the sheep to tha location
        self.s_pos = mov
        # print the sheep's current location
        print("Sheep moved to ", self.s_pos)
        # add to the list of occupied positions
        self.s_posns.append(self.s_pos)
        # for all the positions except the current one
        for pos in self.s_posns[:-1]:
            # set to 0, denoting that the sheep is no longer in these positions
            self.field[pos] = 0
        # display the field with the current sheep position
        self.set_pos()

    def get_neighbor(self, steps, i, j, obstacles):
        """
        returns the list of neighbors based on the possible moves:
        """
        # initialize an empty list for the neighbors
        neighbor = []
        # for all the possible moves
        for s in steps:
            # if the cell isn't occupied by any of the obstacles
            if self.field[s[0]][s[1]] not in obstacles:
                # add the cell to the list
                neighbor.append((s[0], s[1]))

        # return the list of neighbors
        return neighbor

    def dog1(self, d1):
        """
        function to move the dog bot 1
        """
        # if the Manhattan distance between the dog and sheep is greater than 0 (not near the sheep)
        if self.manhat_dist(self.d1_pos, (self.s_pos[0], self.s_pos[1] - 1)) > 0:
            # get the list of neighbors ([2, 3] denotes the current positions of the other dog bot and the sheep
            neighbors = self.neighbors(self.d1_pos, [2, 3])
            print(neighbors)
            # use a dict to store the Manhattan distances of the neighbors to the cell above
            # the current location of the sheep
            dist = {}
            # for all the neighboring cells
            for neighbor in neighbors:
                # get the Manhattan distance from the neighbor to the cell above the sheep
                d = self.manhat_dist(neighbor, d1)
                # store it as the value in the dict with the key as the neighbor position
                dist[neighbor] = d
            print(dist)
            # choose the neighbor, based on the minimum distance, among the current list of neighbors
            pos = min(dist.items(), key=lambda l: l[1])[0]
            # set the position of dog bot 1 to this position
            self.d1_pos = pos

            # print the current position
            print("Current position: ", self.d1_pos)

            # add the current position of dog bot 1 to the list of positions
            self.d1_posns.append(self.d1_pos)
            # for all other positions besides the current one
            for pos in self.d1_posns[:-1]:
                # set to 0 to indicate the bot is no longer in those positions
                self.field[pos] = 0

            # display the field with the current positions
            self.set_pos()
            # return the current position
            return self.d1_pos
        else:
            # otherwise print that the dog bot has reached the position
            print("Dog 1 is at position")

    def dog2(self, d2):
        """
        function to move the dog bot 2
        """

        # if the bot 2 is not near the cell to the left of the sheep
        if self.manhat_dist(self.d2_pos, (self.s_pos[0] - 1, self.s_pos[1])) > 0:
            # get the list of neighboring cells ([1, 3] denotes the current positions of the other dog bot and the sheep
            neighbors = self.neighbors(self.d2_pos, [1, 3])
            print(neighbors)
            # create a dict to store the Manhattan distances of the neighboring cells
            dist = {}
            # for all the neighboring cells
            for neighbor in neighbors:
                # get the Manhattan distance
                d = self.manhat_dist(neighbor, d2)
                # store it in the dictionary
                dist[neighbor] = d
            print(dist)
            # get the neighboring cell with the minimum Manhattan distance to the cell to the left
            # of the sheep's current position
            pos = min(dist.items(), key=lambda l: l[1])[0]
            # set the current position of dog bot 2 to this position
            self.d2_pos = pos

            # print the current position
            print("Current position: ", self.d2_pos)

            # add the current position to the list of positions it has been on
            self.d2_posns.append(self.d2_pos)
            print(self.d2_posns)
            # for all other cells except the current one
            for pos in self.d2_posns[:-1]:
                # set to 0 to indicate that the dog bot is no longer in those positions
                self.field[pos] = 0

            # display the field with the updated positions
            self.set_pos()
            # return the current position of dog bot 2
            return self.d2_pos
        else:
            # otherwise print that the bot is at the position
            print("Dog 2 is at position")

    def manhat_dist(self, pos1, pos2):
        """
        function to compute the Manhattan distance between two positions
        :param pos1: first position to consider
        :param pos2: second position to consider
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def game_over(self):
        """
        returns if the game is over (if the sheep has been cornered)
        """
        return (self.d1_pos == (5, 6) and self.d2_pos == (6, 5) and self.s_pos == (6, 6)) or (
                self.d1_pos == (6, 5) and self.d2_pos == (5, 6) and self.s_pos == (6, 6))


def board_layout():
    """
    main function
    """
    # create the field layout
    field = Field()
    # initialize number of rounds to 0
    rounds = 0

    # until the Manhattan distance between the sheep and dog bots is 1 (above, below, left or right to the sheep)
    while field.manhat_dist(field.s_pos, field.d1_pos) > 0 and field.manhat_dist(field.s_pos, field.d2_pos) > 0:
        # if the sheep is cornered
        if field.game_over():
            # print total number of rounds needed
            print("Total number of rounds needed to pin the sheep: ", rounds)
            # terminate the loop
            break
        # otherwise
        else:
            print("======")
            print("ROUND ", rounds + 1)
            print("======\n")
            print("DOG BOT 1")
            # move the dog bot 1 to the position nearest to the cell above the sheep
            field.dog1((field.s_pos[0], field.s_pos[1] - 1))
            print("DOG BOT 2")
            # move the dog bot 2 to the position nearest to the cell to the left of the sheep
            field.dog2((field.s_pos[0] - 1, field.s_pos[1]))
            print("SHEEP")
            # move the sheep
            field.sheep()
            print("\n")
            # increment number of rounds and continue the loop
            rounds += 1
    # return the number of rounds needed
    return rounds


if __name__ == '__main__':
    # board_layout()
    # writes the results obtained for the random indices
    file = open("rounds_results.txt", 'a')
    file.write(str(board_layout()))
    file.write('\n')
    file.close()

    with open('rounds_results.txt', 'r') as f:
        # reads from the file and prints the average number of rounds
        lines = f.readlines()
        counter1 = []
        for l in lines:
            counter1.append(int(l))

    file = open("rounds_results_paper.txt", 'a')
    # writes the results for the example configuration
    file.write(str(board_layout()))
    file.write('\n')
    file.close()

    with open('rounds_results_paper.txt', 'r') as f:
        # read from the file and print the average
        lines = f.readlines()
        counter = []
        for l in lines:
            counter.append(int(l))

    # print the avergaes for example config and random indices
    print("Average rounds for the configuration given in the example: ", round(sum(counter) / len(counter)))
    # print("Average rounds for setting random locations: ", round(sum(counter1) / len(counter1)))
