import time
import numpy as np
import tensorflow as tf
from helper import plot, wait
from agent import Agent
from minesweeper import MinesweeperGame
from datetime import datetime

STATE_VISIBLE = True

if __name__ == '__main__':
    start_time = datetime.now().strftime("%d_%m_%Y___%H_%M_%S")
    image_name = f"{start_time}_training.png"
    tf.compat.v1.disable_eager_execution()


    x_side, y_side = 7, 7
    game = MinesweeperGame(x_side, y_side, 10)
    lr = 0.0003
    n_games = 6000
    agent = Agent(gamma=0, epsilon=1.0, lr=lr,
                input_dims=(y_side, x_side, 1),
                n_actions=y_side * x_side,
                mem_size=100_000, batch_size=256,
                epsilon_end=0.01, state_visible = STATE_VISIBLE)

    scores = []
    avg_scores = []
    successes = []
    avg_successes = []
    already_clicked_perc = []
    avg_already_clicked_perc = []

    for ind in np.arange(n_games + 1):
        done = False
        score = 0
        game.reset()
        observation = agent.get_state(game)
        step_count, times_clicked_already_clicked = 0, 0
        mine_on_first_trial = False

        while not done:
            action = agent.choose_action(observation)
            i, j = action // x_side, action % x_side

            observation_, reward, done, info = agent.step(game, i, j)

            if not STATE_VISIBLE:
                if step_count == 0 and done == True:
                    mine_on_first_trial = True
                if mine_on_first_trial:
                    break
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()

            step_count += 1

            # if reward is 0.5, it means that the agent clicked on
            # a cell that has already been clicked
            if reward == -.5:
                times_clicked_already_clicked += 1

        wait() # to avoid overheating my selfless laptop
        if mine_on_first_trial: continue

        scores.append(score)
        if game.victory:
            successes.append(1)
        else:
            successes.append(0)

        avg_score = np.mean(scores[-100:])
        avg_scores.append(avg_score)
        avg_successes.append(np.mean(successes[-100:]))
        already_clicked_perc.append(times_clicked_already_clicked / step_count)
        avg_already_clicked_perc.append(np.mean(already_clicked_perc[-100:]))

        if ind % 50 == 0 and ind > 0:
            plot(scores, avg_scores, avg_successes, avg_already_clicked_perc, image_name)
        print('episode: ', ind, 'score %.2f' % score,
                'average_score %.2f' % avg_score,
                'epsilon %.3f' % agent.epsilon)
        if np.all(np.array(avg_scores[-3:]) > 4):
            agent.eps_min = agent.eps_min * .2
    agent.save_model()
