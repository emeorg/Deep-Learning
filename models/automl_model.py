from libs import *
import keras_tuner as kt
from tensorflow import keras
from tensorflow.keras import layers


def build_model_tuner(hp, input_dim):
    model = keras.Sequential()

    model.add(keras.Input(shape=(input_dim,)))

    # número de capas
    for i in range(hp.Int("num_layers", 2, 4)):
        model.add(layers.Dense(
            units=hp.Int(f'units_{i}', min_value=32, max_value=256, step=32),
            activation='relu'
        ))

        model.add(layers.Dropout(
            hp.Float(f'dropout_{i}', 0.2, 0.5, step=0.1)
        ))

    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])
        ),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model