import random

from splendor.models.actions import AgentIntent, ValidPlayerActions


class IdiotAgent():
    random: random.Random
    trainings: int

    def __init__(self, seed=None, trainings=0, rand=None):
        self.random = rand or random.Random(seed)
        self.trainings = trainings

    def evaluate(self, inputs):
        return AgentIntent(
            position_quality=self.random.random(),  # How good is the board position?
            resource_affinity=tuple([self.random.random()] * 6),  # Resource affinity
            noble_affinity=tuple([self.random.random()] * 5),  # Noble affinity
            action_probabilities=tuple([self.random.random()] * len(ValidPlayerActions)))

    def train_new(self, history):
        print("Train this agent on ", len(history), " now!")
        return IdiotAgent(
            trainings=self.trainings + 1,
            rand=self.random)
