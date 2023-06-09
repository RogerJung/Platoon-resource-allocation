import numpy as np
import random

def same_seeds(seed):
    random.seed(seed)
    np.random.seed(seed)

same_seeds(2023)

class ENVIRONMENT(object):
    """docstring for ENVIRONMENT"""
    def __init__(
        self,
        n_actions,
        rb_leader,
        rb_member,
        rb_hidden,
        state_size=32,
        window_size=1,
    ):
        super(ENVIRONMENT, self).__init__()
        self.state_size = state_size
        self.window_size = window_size
        self.rb_leader = rb_leader
        self.rb_member = rb_member
        self.rb_hidden = rb_hidden
        self.n_actions = n_actions
        self.n_nodes = 2

    def reset(self):
        state = []
        for i in range(int(self.state_size / 2)):
            action_index = np.where(self.rb_leader[i] == 0)
            # action_size_period = len(action_index[0])
            # action_sel = np.random.choice(action_size_period)
            ##The leader vehicle choose an idle RB to send
            # action = action_index[0][action_sel]
            action = np.random.choice(action_index[0])
            # print(f"idle RB: {action_index[0]}")
            # print(f"select RB:{action}")
            #The leader vehicle will receive an ack/nack from the last member
            obs = int(self.rb_hidden[i][action] > 0)
            state.append(action)
            state.append(obs)
        state = np.array(state)
        return state

    def step(self, action, time):
        reward = 0
        observation_ = int(self.rb_hidden[time][action] +
                           self.rb_leader[time + 1][action] > 0)

        reward = int(observation_ == 0)
        # print(reward)

        return observation_, reward

    def test_update(self, rb_leader, rb_member):
        self.rb_leader = rb_leader
        self.rb_member = rb_member
        self.rb_hidden = rb_member
