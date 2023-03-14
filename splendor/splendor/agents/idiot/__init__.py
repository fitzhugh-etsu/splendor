import random
from splendor.io import AgentIntent, OUTPUTS_LEN
from typing import NamedTuple


class IdiotAgent(NamedTuple):
    random: random.Random

    @staticmethod
    def evaluate(agent, inputs):

        return AgentIntent(
            position_quality=agent.random.random(),  # How good is the board position?
            resource_affinity=[agent.random.random()] * 6,  # Resource affinity
            noble_affinity=[agent.random.random()] * 5,  # Noble affinity
            action_probabilities=[agent.random.random()] * OUTPUTS_LEN))

    @staticmethod
    def train(agent, actions, weight):
        return agent

def create(seed=None):
    return IdiotAgent(
        random=random.Random(seed))
