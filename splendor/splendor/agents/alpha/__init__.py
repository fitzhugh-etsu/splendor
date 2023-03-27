import copy
import numpy as np
import keras.optimizers
import random
from splendor.models.actions import AgentIntent, ValidPlayerActions
import splendor.io as io
from splendor.models.player import Player
from keras.models import Model
from keras.layers import Activation, BatchNormalization, Dense, Flatten, Input, Reshape, ReLU, Add, Dropout
from keras.layers.convolutional import Conv1D
from keras.constraints import unit_norm

# IMAGE DUMP
# keras.utils.plot_model(model, "my_first_model.png")
from tensorflow.keras.constraints import Constraint

def create(input_length, output_layer=128):
    # inputs = Input(shape=(1,))
    # model = Dense(1)(inputs)
    # model = Model(inputs=inputs, outputs=model)
    # print(model(np.array([1])))

    # https://jonathan-hui.medium.com/alphago-zero-a-game-changer-14ef6e45eba5
    # https://keras.io/getting_started/intro_to_keras_for_engineers/
    inputs = Input(shape=(input_length,))
                   #dtype='int32')

    model = Dense(input_length,
                  # input_shape=(input_length,),
                  activation='relu')(inputs)
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

    # import keras.utils
    # keras.utils.plot_model(model, "/tmp/model.png", show_shapes=True)
    model.compile(
        optimizer='Adam', #keras.optimizers.RMSprop(),  # Optimizer
        # Minimize loss:
        #loss=keras.losses.SparseCategoricalCrossentropy(),
        # Monitor metrics:
        #metrics=[keras.metrics.SparseCategoricalAccuracy()],
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
                              output_layer=(
                                1 +
                                6 +
                                5 +
                                len(ValidPlayerActions)))

    def evaluate(self, inputs):
        vec = np.array(list(map(float, inputs)))
        vec = vec.reshape(-1, len(inputs), 1)
        results = self.network.predict(vec, verbose=0)[0]

        return AgentIntent.from_tuple(results)

    def train_new(self, history):
        import pudb; pudb.set_trace()
        # history[N][1] = 1 / -1 for scoring
        # history[N][0][0] = PerformedAction
        # history[N][0][1] = Intent
        training_set = [
            (
                # Inputs
                np.array(io.inputs(h[0][0].game)),
                # Targets
                np.array(h[0][1].to_tuple()),
                # Weights
                h[1])
            for h
            in history
            ]
        new_obj = copy.deepcopy(self)
        new_obj.trainings += 1
        results = new_obj.network.fit(
            x=training_set,
            use_multiprocessing=True,
            verbose=2)

        return new_obj
