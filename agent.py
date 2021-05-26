import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from model import build_dqn
from buffer import ReplayBuffer

class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                input_dims, epsilon_dec=2e-4, epsilon_end=0.01,
                mem_size=1000000, fname='dqn_model.h5', state_visible = True):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims)
        self.x_side, self.y_side, _ = input_dims
        self.state_visible = state_visible

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.predict(state)

            action = np.argmax(actions)

        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        states, actions, rewards, states_, dones = \
                self.memory.sample_buffer(self.batch_size)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        if self.gamma > 0:
            q_eval = self.q_eval.predict(states)
            q_next = self.q_eval.predict(states_)

            q_target = np.copy(q_eval)

            q_target[batch_index, actions] = rewards + \
                            self.gamma * np.max(q_next, axis=1)*dones
        else:
            # if gamma is equal to 0, the q value is equal to the reward only
            # so there is no need to use the models -> speed up!
            q_eval = self.q_eval.predict(states)
            q_target = np.copy(q_eval)
            q_target[batch_index, actions] = rewards

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > \
                self.eps_min else self.eps_min

    def save_model(self):
        self.q_eval.save(self.model_file)


    def load_model(self):
        self.q_eval = load_model(self.model_file)

    def get_state(self, game):
        """the state is the whole grid."""
        if self.state_visible:
            state = np.where(game.is_reveiled, -1, game.mine_position)
            return np.expand_dims(state, [-1])
        else:
            state = np.where(game.is_reveiled, game.mine_count, -8) / 8
            return np.expand_dims(state, [-1])

    def step(self, game, i, j):
        reward, done = game.game_step(i, j)
        new_state = self.get_state(game)
        return new_state, reward, done, None
