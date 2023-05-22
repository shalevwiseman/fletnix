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
        self.users_picked = np.zeros((num_users,num_arms))
        self.users_tot_val = np.zeros((num_users, num_arms))
        self.users_rate = np.zeros((num_users, num_arms))
        self.current_user = None
        self.current_arm = None
        # creating a dict that hold distribution info about each user
        self.user_data = {}
        for i in range(num_users):
            username = f'User{i}'
            self.user_data[username] = {'mu': 0, 'sigma': 1000, 'N': 0, 'sum_satisfaction': 0, 'arms': {}}

            for j in range(num_arms):
                arm_name = f"Arm{j}"
                self.user_data[username]["arms"][arm_name] = {'mu': 0,'sigma': 1000, 'post_mu': 0, 'post_sigma': 1000, 'sum_satisfaction': 0}
        # TODO: Decide what/if to store. Could be used in the future
        pass

    def choose_arm(self, user_context):
        """
        :input: the sampled user (integer in the range [0,num_users-1])
        :output: the chosen arm, content to show to the user (integer in the range [0,num_arms-1])
        """
        user_name = f"User{user_context}"
        self.user_data[user_name]['N'] += 1

        # Sample from each arm
        post_samps = np.zeros(self.num_arms)
        for j in range(self.num_arms):
            arm_name = f"Arm{j}"
            post_samps[j] = self.get_mu_from_dist(user_name, arm_name)
        chosen_arm = np.where(post_samps == post_samps.max())[0][0]
        #chosen_arm = post_samps.index(max(post_samps))
        self.current_arm = chosen_arm
        self.current_user = user_context


        # TODO: This is your place to shine. Go crazy!
        return chosen_arm

    def notify_outcome(self, reward):
        """
        :input: the sampled reward of the current round.
        """
        self.update_dist(self.current_user, self.current_arm)
        self.user_data[f"User{self.current_user}"]["arms"][f"Arm{self.current_arm}"]["sum_satisfaction"] += reward

        # TODO: Use this information for your algorithm
        pass

    def get_id(self):
        # TODO: Make sure this function returns your ID, which is the name of this file!
        return "id_123456789_987654321"


    def get_mu_from_dist(self, user_name, arm):
        sample_mu = np.random.normal(self.user_data[user_name]['arms'][arm]['post_mu'],
                                     self.user_data[user_name]['arms'][arm]['post_sigma'])
        return sample_mu

    def update_dist(self, user_name, arm):
        prior_sigma = self.user_data[f"User{user_name}"]['sigma']
        N = self.user_data[f"User{user_name}"]['N']
        self.user_data[f"User{user_name}"]['arms'][f"Arm{arm}"]['post_sigma'] = np.sqrt((1/ prior_sigma**2 + N)**(-1))
        self.user_data[f"User{user_name}"]['arms'][f"Arm{arm}"]['post_sigma'] = (self.user_data[f"User{user_name}"]['arms'][f"Arm{arm}"]['post_sigma']**2)\
                                                               * (self.user_data[f"User{user_name}"]['arms'][f"Arm{arm}"]['sum_satisfaction'])


