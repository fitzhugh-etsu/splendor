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

        return AgentIntent(
            position_quality=results[0],
            resource_affinity=tuple(results[1:7]),      # 6
            noble_affinity=tuple(results[7:12]),        # 5
            action_probabilities=tuple(results[12:]))   # rest of them

    def train(self, history):
        print(history[0])
        def to_vec(inputs):
            vec = np.array(list(map(float, inputs)))
            vec = vec.reshape(-1, len(inputs), 1)
            return vec


        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)

        """
        input_boards = CONFIG.nnet_args.encoder.encode_multiple(input_boards)
        """
        input_boards = self.encoder.encode_multiple(input_boards)

        self.nnet.model.fit(x=input_boards, y=[target_pis, target_vs], batch_size=CONFIG.nnet_args.batch_size, epochs=CONFIG.nnet_args.epochs, verbose=VERBOSE_MODEL_FIT)

        self.network.a
        print("Train this agent on ", len(history), " now!")
        return IdiotAgent(
            trainings=self.trainings + 1,
            rand=self.random)
