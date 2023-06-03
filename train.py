import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from data_loader import load_data
from model.DQN import DQN
from model.environment import ENVIRONMENT

np.random.seed(2023)

leader_csv = "./platoon-resource-allocation/leader_density200.csv"
member_csv = "./platoon-resource-allocation/member_density200.csv"

rb_leader, rb_member = load_data(leader_csv, member_csv)
rb_hidden = rb_member
loss_val = []


env = ENVIRONMENT(
                n_actions = 200,
                rb_leader = rb_leader,
                rb_member = rb_member,
                rb_hidden = rb_hidden,
                state_size=32, 
                window_size=7,
                )

dqn_agent = DQN(env.state_size,
                env.n_actions,  
                loss_val = loss_val,
                memory_size=1000,
                replace_target_iter=200,
                batch_size=1,
                learning_rate=0.01,
                gamma=0.9,
                epsilon=0.1,
                epsilon_min=0,
                epsilon_decay=0.5,
                )

counter = 0
total_reward = 0
collision_num = 0
prob_collision = []
state = env.reset()
state_size = len(state)


print('------------------------------------------')
print('---------- Start processing ... ----------')
print('------------------------------------------')


for time in range(int(state_size/2), (len(rb_member))):
    action_index = np.where(rb_leader[time] == 0)
    action_index = np.reshape(action_index, len(action_index[0]))
    # print(action_index)
    
    # DQN algo.
    action = dqn_agent.choose_action(state, action_index)

    # Random selection algo.
    # action = np.random.choice(action_index)
    
    observation_, reward = env.step(action, time)
    if observation_ > 0:
        collision_num +=1
        prob_collision.append(collision_num/(time+1))
    total_reward += reward

    next_state = np.concatenate([state[2:], [action, observation_]])
    # print(next_state)

    dqn_agent.store_transition(state, action, reward, next_state)
    if counter < 200:
        dqn_agent.learn()       # internally iterates default (prediction) model
        counter += 1
    elif counter < 250:
        counter += 1
    else:
        counter = 0
    state = next_state
    print("Step:{0}%, action:{1}, reward:{2}".format(round((time + 1) * 100 / len(rb_member)), action, reward), end="\r")

p_col_rl = collision_num/((len(rb_member)) - int(state_size/2))
print("\ntotal reward is {0}".format(total_reward))
print("\ncollision probability = ", p_col_rl)