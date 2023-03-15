import random
from splendor.models.actions import AgentIntent, ValidPlayerActions


class IdiotAgent():
    random: random.Random
    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def evaluate(self, inputs):
        return AgentIntent(
            position_quality=self.random.random(),  # How good is the board position?
            resource_affinity=[self.random.random()] * 6,  # Resource affinity
            noble_affinity=[self.random.random()] * 5,  # Noble affinity
            action_probabilities=[self.random.random()] * len(ValidPlayerActions))

    def train(self, actions, weight):
        pass
