import copy
import random

import numpy as np
from keras.layers import BatchNormalization, Dense, Dropout, Input
from keras.models import Model

import splendor.io as io
from splendor.models.actions import AgentIntent, ValidPlayerActions

# IMAGE DUMP
# keras.utils.plot_model(model, "my_first_model.png")

def create(input_length, output_layer=128):
    # https://jonathan-hui.medium.com/alphago-zero-a-game-changer-14ef6e45eba5
    # https://keras.io/getting_started/intro_to_keras_for_engineers/
    inputs = Input(shape=(input_length,))

    model = Dense(input_length, activation='relu')(inputs)
    model = BatchNormalization()(model)
    model = Dropout(0.2)(model)
    model = Dense(input_length / 2, activation='relu')(model)
    model = BatchNormalization()(model)
    model = Dropout(0.2)(model)
    model = Dense(input_length / 2, activation='relu')(model)
    model = BatchNormalization()(model)
    model = Dropout(0.2)(model)

    model = Dense(output_layer, activation='softmax')(model)

    model = Model(inputs=inputs, outputs=model)

    model.compile(
        optimizer='adam',  # keras.optimizers.RMSprop(),  # Optimizer
        # Minimize loss:
        loss='mean_squared_error',  # custom_loss_function,
    )

    return model

class AlphaAgent():
    random: random.Random
    trainings: int
    network: None

    def __init__(self, seed=None, trainings=0, rand=None):
        self.random = rand or random.Random(seed)
        self.trainings = trainings

        self.network = create(input_length=io.INPUTS_LEN,
                              output_layer=(1 +
                                            6 +
                                            5 +
                                            len(ValidPlayerActions)))

    def evaluate(self, inputs):
        vec = np.array(list(map(float, inputs)))
        vec = vec.reshape(-1, len(inputs), 1)
        results = self.network.predict(vec, verbose=0)[0]

        return AgentIntent.from_tuple(results)

    def train_new(self, history):
        # history[N][1] = 1 / -1 for scoring
        # history[N][0][0] = PerformedAction
        # history[N][0][1] = Intent

        # Inputs
        inputs = np.stack([np.array(io.inputs(h[0][0].game)) for h in history])
        # Targets
        targets = np.stack([np.array(h[0][1].to_tuple()) for h in history])
        # Weights
        weights = np.stack([np.array([h[1]]) for h in history])

        new_obj = copy.deepcopy(self)
        new_obj.trainings += 1

        results = new_obj.network.fit(
            x=inputs,
            y=[targets, weights],
            use_multiprocessing=True,
            verbose=2)
        print(results)
        return new_obj
