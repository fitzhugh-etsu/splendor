import random


def evaluate(inputs, outputs):
    return (
        (random.random(), ) ,   # How good is the board position?
        [random.random()] * 6,  # Resource affinity
        [random.random()] * 5,  # Noble affinity
        [random.random()] * len(outputs))

def won(history
