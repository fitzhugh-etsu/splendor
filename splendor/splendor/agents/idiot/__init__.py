import random
from splendor.io import AgentIntent

def evaluate(agent, inputs, outputs):
    return AgentIntent(
        position_quality=random.random(),  # How good is the board position?
        resource_affinity=[random.random()] * 6,  # Resource affinity
        noble_affinity=[random.random()] * 5,  # Noble affinity
        action_probabilities=[random.random()] * len(outputs))

def train(agent, actions, weight):
    return agent
