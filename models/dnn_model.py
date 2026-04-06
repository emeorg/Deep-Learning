from libs import *
from tensorflow import keras
from tensorflow.keras import layers

def build_model(input_dim):
    model = keras.Sequential([
        keras.Input(shape=(input_dim,)),

        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),

        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),

        layers.Dense(32, activation='relu'),

        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model