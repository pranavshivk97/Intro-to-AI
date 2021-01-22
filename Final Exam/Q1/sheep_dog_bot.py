import numpy as np
import random


class Field:
    """
    class that creates the field environment
    """
    def __init__(self):
        """
        initializes the parameters for the field
        """
        # creates the field with dimensions 7x7
        self.field = np.zeros((7, 7))
        # to set the initial positions of dog bots and sheep
        self.d1_pos = []
        self.d2_pos = []
        self.s_pos = []

        # keep track of the positions of the dog bots and the sheep
        self.d1_posns, self.d2_posns, self.s_posns = [], [], []

        # sets initial positions based on the configuration given in the question
        # self.paper_config()
        # function to set random indices
        self.set_rand_index()

    def paper_config(self):
        """
        sets initial conditions as given in the question
        """
        # initial positions for dog bots and sheep
        self.d1_pos, self.d2_pos, self.s_pos = (0, 6), (6, 3), (4, 0)
        # self.d1_pos, self.d2_pos, self.s_pos = (0, 6), (6, 0), (0, 0)
        # store these locations in the corresponding lists
        self.d1_posns, self.d2_posns, self.s_posns = [self.d1_pos], [self.d2_pos], [self.s_pos]
        # set the field based on these parameters
        self.set_pos()

    def set_rand_index(self):
        """
        sets random indices for dog bots and sheep
        """
        self.d1_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        self.d2_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        self.s_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))

        # if the locations of 2 are the same, reassign them
        while self.d1_pos == self.d2_pos or self.d1_pos == self.s_pos or self.d2_pos == self.s_pos:
            self.d1_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
            self.d2_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
            self.s_pos = (random.choice(np.arange(0, 7)), random.choice(np.arange(0, 7)))
        print(self.d1_pos, self.d2_pos, self.s_pos)

        self.d1_posns, self.d2_posns, self.s_posns = [self.d1_pos], [self.d2_pos], [self.s_pos]

        # set the field based on these parameters
        self.set_pos()

    def set_pos(self):
        """
        set the field
        """
        # Dog bot 1 gets assigned a value of 1
        self.field[self.d1_pos] = 1
        # Dog bot 2 gets assigned a value of 2
        self.field[self.d2_pos] = 2
        # Sheep gets assigned a value of 3
        self.field[self.s_pos] = 3
        # print their positions
        print("DOG BOT 1 Positions: ", self.d1_posns)
        print("DOG BOT 2 Positions: ", self.d2_posns)
        print("SHEEP Positions: ", self.s_posns)
        # display the field
        print(self.field)

    def neighbors(self, pos):
        """
        returns list of neighbors
        """
        # assign the position coordinates
        i, j = pos[0], pos[1]
        # if the field isn't already occupied by the dog bots
        if self.field[i][j] not in [1, 2]:
            # check for all corners
            if pos in [(0, 0), (6, 6), (0, 6), (6, 0)]:
                # left top corner
                if pos == (0, 0):
                    neighbors = self.get_neighbor([(0, 1), (1, 0)], i, j)
                # right bottom corner
                elif pos == (6, 6):
                    neighbors = self.get_neighbor([(6, 5), (5, 6)], i, j)
                # right top corner
                elif pos == (0, 6):
                    neighbors = self.get_neighbor([(1, 6), (0, 5)], i, j)
                # left bottom corner
                elif pos == (6, 0):
                    neighbors = self.get_neighbor([(5, 0), (6, 1)], i, j)
            # check the middle portion of the field
            elif 0 < i < 6 and 0 < j < 6:
                neighbors = self.get_neighbor([(i+1, j), (i-1, j), (i, j-1), (i, j+1)], i, j)
            # check the top edge
            elif i == 0 and 0 < j < 6:
                neighbors = self.get_neighbor([(i+1, j), (i, j-1), (i, j+1)], i, j)
            # check for the left edge
            elif j == 0 and 0 < i < 6:
                neighbors = self.get_neighbor([(i-1, j), (i+1, j), (i, j+1)], i, j)
            # check for the bottom edge
            elif i == 6 and 0 < j < 6:
                neighbors = self.get_neighbor([(i-1, j), (i, j-1), (i, j+1)], i, j)
            # check for the right edges
            elif j == 6 and 0 < i < 6:
                neighbors = self.get_neighbor([(i+1, j), (i-1, j), (i, j-1)], i, j)

        return neighbors

    def sheep(self):
        """
        function to move the sheep
        """
        # get the neighbors based on the sheep's position
        neighbors = self.neighbors(self.s_pos)
        print(neighbors)
        # if there are no neighbors (the sheep is pinned)
        if not neighbors:
            print("Sheep is at the same position")
            # stay at the same position
            mov = self.s_pos
        # otherwise
        else:
            # randomly choose among the neighbors
            mov = random.choice(neighbors)
        # if the position chosen is already occupied by the dog bots, choose again
        while mov == self.d1_pos or mov == self.d2_pos:
            mov = random.choice(neighbors)
        # assign the sheep's current positiion to this position
        self.s_pos = mov
        print("Sheep moved to ", self.s_pos)
        # add the new position to the list of current positions
        self.s_posns.append(self.s_pos)
        # assign all previous positions except the current one to 0, to show that the sheep is no longer there
        for pos in self.s_posns[:-1]:
            self.field[pos] = 0
        # display the field
        self.set_pos()

    def get_neighbor(self, steps, i, j):
        """
        returns the list of neighbors based on the index and the steps:
        """
        # initialize an empty list
        neighbor = []
        # for all possible steps
        for s in steps:
            # if the dog bots haven't already occupied the position
            if self.field[s[0]][s[1]] not in [1, 2]:
                # add those positions to the list and return
                neighbor.append((s[0], s[1]))

        return neighbor

    def commands(self, command, pos):
        """
        possible commands and possible actions based on those commands
        """
        # if the command is up, and if the position is not already at the top of the field
        if command == 'up' and pos[0] != 0:
            # get the corresponding action (adding this to the current position enables moving up)
            dif = (-1, 0)
        # if the command is down, and the position isn't already at the bottom of the field
        elif command == 'down' and pos[0] != 6:
            # get the corresponding action (adding this to the current position enables moving down)
            dif = (1, 0)
        # if the command is left, and the index isn't already at the left edge of the field
        elif command == 'left' and pos[1] != 0:
            # get the corresponding action (moving left)
            dif = (0, -1)
        # if the command is right and the index isn't already at the rightmost edge
        elif command == 'right' and pos[1] != 6:
            # get the corresponding action (move right)
            dif = (0, 1)
        # if the command is hold, stay in the same place
        elif command == 'hold':
            dif = (0, 0)
        # for all other given commands, return Invalid
        else:
            return 'Invalid'

        return dif

    def update_location(self, pos, obstacles):
        """
        function to update the location of the bots taking into account the obstacles
        """
        comm = input("Enter the command for the bot: ")
        # get the corresponding action based on the commands
        mov = self.commands(comm, pos)
        print(mov)
        # if the move is invalid, ask again for a valid position
        while mov == 'Invalid' or self.is_invalid_move((pos[0] + mov[0], pos[1] + mov[1])):
            print("Invalid move")
            comm = input("Enter the command for the bot: ")
            mov = self.commands(comm, pos)
        # if there are obstacles blocking that position, print and ask for another action
        while self.field[(pos[0] + mov[0], pos[1] + mov[1])] in obstacles:
            print("Obstacle: Invalid move")
            comm = input("Enter a valid command for the bot: ")
            mov = self.commands(comm, pos)
        # get the new position by adding with the action
        pos = (pos[0] + mov[0], pos[1] + mov[1])

        # return the new position
        return pos

    def dog1(self):
        """
        function to move the dog bots
        """
        # update the position of the first dog bot
        self.d1_pos = self.update_location(self.d1_pos, [2, 3])

        # print the new position
        print("Current position: ", self.d1_pos)

        # add to the list of poditions
        self.d1_posns.append(self.d1_pos)
        # for all other positions, assign to 0, to show that the bot is no longer in those fields
        for pos in self.d1_posns[:-1]:
            self.field[pos] = 0

        # display the field
        self.set_pos()

        return self.d1_pos

    def dog2(self):
        """
        function to move the second dog bot
        """
        # update the position of the dog bot
        self.d2_pos = self.update_location(self.d2_pos, [1, 3])

        # print current position of the dog bot
        print("Current position: ", self.d2_pos)

        # add this position to the list of positions of the dog bot
        self.d2_posns.append(self.d2_pos)
        print(self.d2_posns)
        # assign all other positions in the field to 0, to show that the bot is no longer in that position
        for pos in self.d2_posns[:-1]:
            self.field[pos] = 0

        # display the field
        self.set_pos()

    def is_invalid_move(self, pos):
        """
        returns if the move performed was invalid
        """
        # checks the bounds of the position, whether the position moves out of the field
        return pos[0] == -1 or pos[1] == 7 or pos[0] == 7 or pos[1] == -1

    def game_over(self):
        """
        returns if the sheep is pinned by the bots
        """
        return (self.d1_pos == (5, 6) and self.d2_pos == (6, 5)) or (self.d1_pos == (6, 5) and self.d2_pos == (5, 6)) \
               and self.s_pos == (6, 6)


def board_layout1():
    # create the layout of the field
    field = Field()

    rounds = 0
    # until the game is over
    while not field.game_over():
        print("======")
        print("ROUND ", rounds+1)
        print("======\n")
        print("DOG BOT 1")
        # move dog bot 1
        field.dog1()
        print("DOG BOT 2")
        # move dog bot 2
        field.dog2()
        print("SHEEP")
        # move the sheep
        field.sheep()
        print("\n")
        # add 1 to number of rounds
        rounds += 1

    # print total number of rounds required
    print("Total number of rounds needed to pin the sheep: ", rounds)


if __name__ == '__main__':
    board_layout1()
