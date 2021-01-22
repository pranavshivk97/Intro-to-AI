class MDP:
    """
    class that creates the Markov Decision Process model
    """
    def __init__(self, beta=0.9):
        """
        initializes the state space, transition model and rewards associated with the model
        :param beta: discount factor
        """
        self.states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.trans_use, self.trans_replace = [[] for _ in range(len(self.states))], [[] for _ in
                                                                                     range(len(self.states))]
        self.rewards_use, self.rewards_replace = [0 for _ in range(len(self.states))], [0 for _ in
                                                                                        range(len(self.states))]
        self.beta = beta

    def setup_mdp(self):
        """
        builds the MDP model
        """
        # probabilities of the machine being used in each state
        probs_use = [0.1 * i for i in range(1, 9, 1)]
        probs_use.insert(0, 1)
        # print(probs_use)

        # probabilities of the machine being replaces in each state
        probs_replace = [1 for i in range(1, 10)]
        # the machine is always used in the state New (0) (p=1), so the probability of it being replaced in
        # that state is 0
        probs_replace.insert(0, 0)
        # print(probs_replace)

        # reward on using the machine in a New state is 101
        self.rewards_use[0] = 101
        # machine can't be replaced in a New state so reward for this state is taken as 0
        self.rewards_replace[0] = 0

        for i in range(1, 9):
            # setting the rewards for each state
            self.rewards_use[i] = 100 - 10 * i
            # a cost of 255 is incurred on replacing the machine in any state, which means the reward is -255.
            self.rewards_replace[i] = -255
            # transition model for using the machine in each state
            self.trans_use[i] = [(i + 1, probs_use[i]), (i, 1 - probs_use[i])]
            # transition model for replacing the machine in each state
            self.trans_replace[i] = [(0, 1)]
        # setting the reward for using the machine in the Dead state to -infinity (not possible)
        self.rewards_use[9] = float('-inf')
        # setting reward for replacing the machine in a Dead state
        self.rewards_replace[9] = -255
        # using a machine in New state moves the machine to state Used1 with a probability of 1
        self.trans_use[0] = [(1, 1)]
        # using a machine in the Dead state
        self.trans_replace[9] = [(0, 1)]
        # print(self.rewards_use)
        # print(self.rewards_replace)
        # print(self.trans_use)
        # print(self.trans_replace)

    def setup_mdp2(self, cost):
        """
        for problem 2c, set the MDP in such a way that the transition model for
        replacing the machine factors in the cost
        :param cost: cost for which the bot can sell the deal for
        """
        # probabilities for moving the machine to the next state after using it
        probs_use = [0.1 * i for i in range(1, 9, 1)]
        # since the machine can only be used in the New state, p=1
        probs_use.insert(0, 1)
        # print(probs_use)

        # probabilities for replacing the machine in each state is always 1 - it always reverts to the New state
        probs_replace = [1 for _ in range(1, 10)]
        # a machine in the New state can only be used and not replaced, so probability for replacing the machine in a
        # New state is 0
        probs_replace.insert(0, 0)
        # print(probs_replace)

        # reward for using the machine in a New state is 101
        self.rewards_use[0] = 101
        # reward for replacing the machine in a New state is 0
        self.rewards_replace[0] = 0

        for i in range(1, 9):
            # setting rewards using the machine in each state, except Dead
            self.rewards_use[i] = 100 - 10 * i
            # setting replacement (using a machine in states Used1 or Used2) costs
            self.rewards_replace[i] = cost
            # setting the transition model for using the machine
            self.trans_use[i] = [(i + 1, probs_use[i]), (i, 1 - probs_use[i])]
            # setting the transition model for replacing the machine
            self.trans_replace[i] = [(1, 0.5), (2, 0.5)]
        # reward for using the machine in Dead state is the negative of the cost
        self.rewards_use[9] = cost
        # reward for replacing the machine in the Dead state is the negative value of the cost
        self.rewards_replace[9] = cost
        # transition law for using the machine in new state - go to state 1 (Used1) with p=1
        self.trans_use[0] = [(1, 1)]
        # transition law for replacing the model in the dead state - move to states Used1 or Used2 with p=0.5 each
        self.trans_replace[9] = [(1, 0.5), (2, 0.5)]
        print(self.rewards_use)
        print(self.rewards_replace)
        print(self.trans_use)
        print(self.trans_replace)

    def actions(self, state):
        """
        defines the possible actions to take in each state
        :param state: current state the machine is in
        Action 0 - USE, Action 1 - REPLACE
        """
        # if the machine is in a NEW state
        if state == 0:
            # action = use
            return [0]
        # if the machine is in Dead state
        elif state == 9:
            # action = replace
            return [1]
        else:
            # otherwise either use or replace it (for all the other states (Used1 - Used8)
            return [0, 1]

    def transition(self):
        """
        :return: transition model with the (state, prob) for each possible action (USE, REPLACE)
        """
        return [self.trans_use, self.trans_replace]

    def reward(self):
        """
        :return: reward associated with each action (USE, REPLACE)
        """
        return [self.rewards_use, self.rewards_replace]


def value_iteration(mdp, beta, e=0.001):
    """
    implementation of the value iteration algorithm to find the optimal utility
    :param mdp: MDP object
    :param beta: discount factor
    :param e: error associated with the utility (epsilon)
    :return: optimal utility U*
    """
    # initialize the utility for all states to be 0 initially
    utility = {state: 0 for state in mdp.states}
    # repeat
    while True:
        # create a copy of the utility
        util = utility.copy()
        # intialize the max change in the utility to 0
        delta = 0
        # for all states in the model
        for s in mdp.states:
            # define the updated utility function based on the Bellman equation
            utility[s] = max([(mdp.reward()[a][s] + beta * sum([p * util[s1] for (s1, p) in mdp.transition()[a][s]]))
                              for a in mdp.actions(s)])
            # update the change observed in the utility in that iteration
            delta = max(delta, abs(util[s] - utility[s]))
        # check if the algorithm converges
        if delta < e * (1 - mdp.beta) / mdp.beta:
            # if so, return the utility function
            return utility


def optimal_policy(mdp, beta, utility):
    """
    determines the optimal policy using the utility obtained in value iteration
    :param mdp: MDP object
    :param beta: discount factor
    :param utility: optimal utility function
    :return: best policy (action) that gives the optimal utility
    """
    # initialize a dictionary for the optimal policies for each state with state=key
    pi = {}
    # for all states
    for s in mdp.states:
        # decide the optimal policy by considering the action that produces the expected optimal utility
        # maps from state to action
        pi[s] = max(mdp.actions(s), key=lambda a: util(mdp, s, a, beta, utility))
    return pi


def util(mdp, s, a, beta, utility):
    """
    function to return the expected utility
    :param mdp: MDP object
    :param s: current state
    :param a: current action
    :param beta: discount factor
    :param utility: optimal utility
    """
    return [(mdp.reward()[a][s] + beta * sum([p * utility[s1] for (s1, p) in mdp.transition()[a][s]]))]


def main():
    # implement q2a
    # create the MDP object
    mdp = MDP()
    # set up the MDP based on the specifications
    mdp.setup_mdp()
    # set beta value
    # beta = [0.9]
    # for q2d
    beta = [0.1, 0.3, 0.5, 0.7, 0.8, 0.85, 0.87, 0.9, 0.99]
    # beta = [0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
    # for all values of beta
    for b in beta:
        print(b)
        # get the optimal utility
        utility = value_iteration(mdp, b)
        print("U*: ", utility)
        # get the optimal action that produces this utility
        print("pi*: ", optimal_policy(mdp, b, utility))

    # for q2c
    # for all costs from 0 to 254 (at 255 you don't want to take the deal)
    # for cost in range(255):
    #     # c is made negative to factor it into the reward for replacement
    #     c = -cost
    #     print("Cost: ", cost)
    #     # set up the MDP model with the cost of buying the used machine
    #     mdp.setup_mdp2(c)
    #     # run value iteration for all cost values
    #     ul = value_iteration(mdp, 0.9)
    #     print("U*: ", ul)
    #     # find the optimal action for all the cost values
    #     pi = optimal_policy(mdp, 0.9, ul)
    #     print("pi*: ", pi)


if __name__ == '__main__':
    main()
