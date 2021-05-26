from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential

def build_dqn(lr, n_actions, input_dims, conv_size = 128, dense_size = 128):
    model = Sequential([
        Conv2D(conv_size, (3,3), activation='relu', padding='same', input_shape=input_dims),
        Conv2D(conv_size, (3,3), activation='relu', padding='same'),
        Flatten(),
        Dense(dense_size, activation='relu'),
        Dense(dense_size, activation='relu'),
        Dense(n_actions, activation=None)])
    model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    return model
