import random


class EffortAgent:
    def __init__(self, memory_length, epsilon, u_l, u_h, r1, r2, beta, cost, threshold):
        self.memory_length = memory_length
        self.epsilon = epsilon
        self.u_l = u_l
        self.u_h = u_h
        self.r1 = r1
        self.r2 = r2
        self.beta = beta
        self.cost = cost
        self.threshold = threshold
        self.choices = []
        self.states = []

        for i in xrange(memory_length):
            if random.random() < 0.5:
                self.choices.append(1)
                if random.random() < 0.5:
                    self.states.append(1)
                else:
                    self.states.append(0)
            else:
                self.choices.append(0)
                self.states.append(0)

    def set_neighbours(self, nbrs):
        self.neighbours = nbrs

    def make_choice(self):
        if random.random() < self.epsilon:
            if random.random() < 0.5:
                self.choices.append(0)
                return 0
            else:
                self.choices.append(1)
                return 1
        else:
            if self.expected_utility_on_effort() > self.expected_utility_without_effort():
                self.choices.append(1)
                return 1
            else:
                self.choices.append(0)
                return 0

    def set_state(self, state):
        self.states.append(state)

    def estimated_probability_of_success(self):
        average = self.history()
        if average < self.threshold:
            return self.r1 * average
        else:
            return self.beta - self.r2 * average

    def expected_utility_on_effort(self):
        p = self.estimated_probability_of_success()
        return (self.u_h - self.cost) * p + (self.u_l - self.cost) * (1.0 - p)

    def expected_utility_without_effort(self):
        return self.u_l

    def current_state(self):
        return self.states[-1]

    def current_choice(self):
        return self.choices[-1]

    def average_state(self):
        if len(self.states) == 0:
            return 0
        else:
            return sum(self.states) / float(len(self.states))

    def average_effort(self):
        if len(self.choices) == 0:
            return 0
        else:
            return sum(self.choices) / float(len(self.choices))

    def history(self):
        success = sum(self.states[-self.memory_length:])
        attempts = sum(self.choices[-self.memory_length:])

        if attempts == 0:
            return 0.0
        else:
            return success / float(attempts)


class EffortWorld:

    def __init__(self, n, threshold, beta, r1, r2, u_l, u_h, memory, epsilon, cost):
        """
        Create a world with n agents
        """

        self.threshold = threshold
        self.r1 = r1
        self.r2 = r2
        self.beta = beta
        self.agents = []
        for i in xrange(n):
            self.agents.append(EffortAgent(memory_length=memory, epsilon=epsilon, u_l=u_l, u_h=u_h, r1=r1, r2=r2, beta=beta, cost=cost, threshold=threshold))

        for idx, a in enumerate(self.agents):
            a.set_neighbours(self.agents)

    def step(self):
        choices = []
        for a in self.agents:
            choices.append(a.make_choice())

        ave_choice = sum(choices) / float(len(choices))

        if ave_choice < self.threshold:
            p = self.r1 * ave_choice
        else:
            p = self.beta - self.r2 * ave_choice

        for a in self.agents:
            if a.current_choice() == 0:
                a.set_state(0)
            else:
                if random.random() < p:
                    a.set_state(1)
                else:
                    a.set_state(0)

    def total_effort(self):
        return sum(map(lambda a: a.current_choice(), self.agents))

    def total_high_status(self):
        return sum(map(lambda a: a.current_state(), self.agents))


def run_simulation(n, periods=1000,threshold=0.5, beta=1.25, r1=1.5, r2=1.0, u_l=2.0, u_h=5.0, memory=10, epsilon=0.1, cost=1.0):
    world = EffortWorld(n, threshold=threshold, beta=beta, r1=r1, r2=r2, u_l=u_l, u_h=u_h, memory=memory, epsilon=epsilon, cost=cost)

    efforts, high_statuses = [], []

    for period in xrange(periods):
        world.step()
        efforts.append(world.total_effort())
        high_statuses.append(world.total_high_status())

    average_effort = map(lambda a: a.average_effort(), world.agents)
    average_state  = map(lambda a: a.average_state(),  world.agents)

    return {
        "efforts": efforts,
        "high_statuses" : high_statuses,
        "ave_effort" : average_effort,
        "ave_state" : average_state
    }