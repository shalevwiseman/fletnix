import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Planner:
    def __init__(self, num_rounds, phase_len, num_arms, num_users, arms_thresh, users_distribution):
        """
        :input: the instance parameters (see explanation in MABSimulation constructor)
        """
        self.num_rounds = num_rounds
        self.phase_len = phase_len
        self.num_arms = num_arms
        self.num_users = num_users
        self.arms_thresh = arms_thresh
        self.users_distribution = users_distribution
        self.users_alpha = np.full((num_users, num_arms), 0.1)
        self.users_beta = np.full((num_users, num_arms), 0.1)
        self.users_max_score = np.zeros((num_users, num_arms))
        self.users_counter = np.zeros((num_users, num_arms))
        self.current_user = None
        self.current_arm = None
        self.current_round = 0
        self.user_not_to_choose = {}
        for i in range(num_users):
            self.user_not_to_choose[i] = set()

        """
        # creating a dict that hold distribution info about each user and each arm
        self.user_data = {}
        for i in range(num_users):
            username = f'User{i}'
            self.user_data[username] = {'mu': 0, 'sigma': 1000, 'N': 0, 'sum_satisfaction': 0, 'arms': {}}

            for j in range(num_arms):
                arm_name = f"Arm{j}"
                self.user_data[username]["arms"][arm_name] = {'mu': 0, 'sigma': 1000, 'post_mu': 0, 'post_sigma': 1000,
                                                              'sum_satisfaction': 0}
        """
        # TODO: Decide what/if to store. Could be used in the future
        pass

    def choose_arm(self, user_context):
        """
        :input: the sampled user (integer in the range [0,num_users-1])
        :output: the chosen arm, content to show to the user (integer in the range [0,num_arms-1])
        """
        self.current_round += 1
        self.current_user = user_context
        current_sample = np.zeros(self.num_arms)
        # for each arm, sample a score from the beta distribution of the current user and the current arm
        for i in range(self.num_arms):
            if i not in self.user_not_to_choose[self.current_user]:
                current_sample[i] = np.random.beta(self.users_alpha[self.current_user][i],
                                                   self.users_beta[self.current_user][i])
        if (current_sample.size != 0):
            self.current_arm = np.argmax(current_sample)
        self.users_counter[self.current_user][self.current_arm] += 1

        # TODO: think about somthing better, maybe use mean score instead of max score

        # every quarter of the phase want to check for every user if he has 0 max score for an arm
        # if so, we want to add it to the set of arms not to choose for this user
        if self.current_round % (self.phase_len / 4) == 0:
            for i in range(self.num_users):
                for j in range(self.num_arms):
                    if (self.users_counter[i][j] >= 1000) and (self.users_max_score[i][j] == 0):
                        self.user_not_to_choose[i].add(j)



        return self.current_arm

    def notify_outcome(self, reward):
        """
        :input: the sampled reward of the current round.
        """
        # update the max score of the current arm
        if reward > self.users_max_score[self.current_user][self.current_arm]:
            self.users_max_score[self.current_user][self.current_arm] = reward

        # update the alpha and beta of the current arm
        self.users_alpha[self.current_user][self.current_arm] += reward
        self.users_beta[self.current_user][self.current_arm] += \
            self.users_max_score[self.current_user][self.current_arm] - reward

        # TODO: Use this information for your algorithm
        pass

    def get_id(self):
        # TODO: Make sure this function returns your ID, which is the name of this file!
        return "id_123456789_987654321"

    def get_sample(self):
        current_sample = np.zeros(self.num_arms)
        for i in range(self.num_arms):
            current_sample[i] = np.random.beta(self.users_alpha[self.current_user][i],
                                               self.users_beta[self.current_user][i])
        return current_sample
