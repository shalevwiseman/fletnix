import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# TODO: remove this import
# from scipy.stats import beta


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
        self.phase_counter = 0
        self.users_distribution = users_distribution
        self.users_alpha = np.full((num_users, num_arms), 0.1)
        self.users_beta = np.full((num_users, num_arms), 0.1)
        self.users_max_score = np.zeros((num_users, num_arms))
        self.users_counter = np.zeros((num_users, num_arms))
        self.users_satisfaction = np.zeros((num_users, num_arms))
        self.users_mean = np.zeros((num_users, num_arms))
        self.arm_use_per_phase = np.zeros(num_arms)
        self.num_round_per_phase = 0
        self.current_user = None
        self.current_arm = None
        self.current_round = 0
        self.keep_arms = True
        self.keeping_length = self.num_rounds
        self.round_to_thrash = arms_thresh
        self.user_not_to_choose = {}
        self.deactivated_arms = set()
        for i in range(num_users):
            self.user_not_to_choose[i] = set()
        # TODO: think about initial conditions for keeping or not an arm



        pass

    def choose_arm(self, user_context):
        """
        :input: the sampled user (integer in the range [0,num_users-1])
        :output: the chosen arm, content to show to the user (integer in the range [0,num_arms-1])
        """
        # update the current user
        self.current_user = user_context

        # update the current round
        # checks for every phase round.
        if self.current_round > 0 and self.current_round % self.phase_len == 0:
            self.phase_counter += 1
            self.num_round_per_phase = 0

            # for every arm check if it is deactivated
            for i in range(self.num_arms):
                if self.arm_use_per_phase[i] < self.arms_thresh[i]:
                    self.deactivated_arms.add(i)
            self.arm_use_per_phase = np.zeros(self.num_arms)
            self.round_to_thrash = self.arms_thresh
        if (len(self.deactivated_arms) == self.num_arms - 1):
            self.keep_arms = False

        self.current_round += 1
        # update the current phase
        self.num_round_per_phase += 1


        if (self.keep_arms == True) and (self.current_round < self.keeping_length):
            total_rounds_to_thrash = 0
            # check if we need to force thrash
            for i in range(self.num_arms):
                if self.round_to_thrash[i] > 0:
                    total_rounds_to_thrash += self.round_to_thrash[i]
            if (self.num_round_per_phase > total_rounds_to_thrash):
                self.max_sample()
                self.arm_use_per_phase[self.current_arm] += 1
                self.round_to_thrash[self.current_arm] -= 1
                return self.current_arm
            else:
                # TODO: think about somthing better
                for i in range(self.num_arms):
                    if (i not in self.deactivated_arms) and (self.arm_use_per_phase[i] < self.arms_thresh[i]):
                        self.current_arm = i
                        self.users_counter[self.current_user][self.current_arm] += 1
                        self.arm_use_per_phase[self.current_arm] += 1
                        self.round_to_thrash[self.current_arm] -= 1
                        return self.current_arm

        # TODO: think about the expectation of keep arm or not, if we want to keep, self.keeping_length =
        #  self.num_rounds
        self.max_sample()
        self.arm_use_per_phase[self.current_arm] += 1
        self.round_to_thrash[self.current_arm] -= 1
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

    def max_sample(self):
        current_sample = np.zeros(self.num_arms)
        # for each arm, sample a score from the beta distribution of the current user and the current arm
        for i in range(self.num_arms):
            if i not in self.user_not_to_choose[self.current_user] and i not in self.deactivated_arms:
                current_sample[i] = np.random.beta(self.users_alpha[self.current_user][i],
                                                   self.users_beta[self.current_user][i])
        if (current_sample.size != 0):
            self.current_arm = np.argmax(current_sample)




        for i in range(self.num_users):
            for j in range(self.num_arms):
                if (self.users_counter[i][j] > 1) and (self.users_max_score[i][j] == 0):
                    self.user_not_to_choose[i].add(j)








