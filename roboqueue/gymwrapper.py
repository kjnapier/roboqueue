# gymwrapper.py
from roboqueue import TargetList, StationaryTarget, Telescope, Conditions
from spacerocks.time import Time

import gym
from gym import spaces

import numpy as np

from copy import deepcopy

SECONDS_PER_DAY = 86_400.0

class TelescopeSchedulingEnv(gym.Env):
    def __init__(self, targets: TargetList, telescope: Telescope, conditions: Conditions, start_epoch: float, max_duration: float, reward_config: dict):
        super(TelescopeSchedulingEnv, self).__init__()

        '''
        Parameters
        ----------
        telescope : Telescope
            The telescope to be used for the scheduling
        start_epoch : float
            The start time of the scheduling (jd)
        conditions : Conditions
            The conditions for the telescope scheduling
        max_duration : float
            The maximum duration of the scheduling in seconds
        targets : TargetList
            The list of targets to be observed
        reward_config : dict
            The configuration for the reward function
        '''

        self.telescope = telescope
        self.conditions = conditions
        self.max_duration = max_duration
        self.reward_config = reward_config
        self.total_duration = 0.0
        self.observed_targets = []
        self.epoch = start_epoch

        # Current observation
        self.init_targets = deepcopy(targets)
        self.targets = targets
        self.sky_state = np.array(self.targets.at(self.epoch, self.telescope, self.conditions)).T

        # Action space for now is just a target object (since ordering a list)
        self.action_space = spaces.Discrete(len(self.targets) + 1)

        # Observation space for each target includes ra, dec, alt, az, exptime
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(len(self.targets), 6), dtype=np.float32)

        self.initial_state = deepcopy(self)

        self.do_nothing_actions = [len(self.targets)]

        # print(f"[INFO] Observation space dim: {self.observation_space}, Action space dim: {self.action_space}")


    def step(self, action):

        DO_NOTHING_PENTALTY = 1.0
        EXTRA_PENTALTY = 60.0

       # print(f"[INFO] Action: {action}")
        if action in self.do_nothing_actions:
            # just wait for 1 second
            self.total_duration += DO_NOTHING_PENTALTY / SECONDS_PER_DAY
            self.epoch += DO_NOTHING_PENTALTY / SECONDS_PER_DAY
            self.sky_state = np.array(self.targets.at(self.epoch, self.telescope, self.conditions)).T
            
            reward = -self.reward_config['exptime'] * DO_NOTHING_PENTALTY
            done = (self.total_duration >= self.max_duration) or (len(self.targets.targets) == 0)
            return self.sky_state, reward, done, {}
        

        # index targets based on action to get single exptime
        ra, dec, alt, az, exptime, is_done = self.targets[action].at(self.epoch, self.telescope, self.conditions)

        skip = is_done or (exptime > 1e5)
        if skip:
            print(f"[INFO] Skipping target {action}")
            self.total_duration += EXTRA_PENTALTY / SECONDS_PER_DAY
            self.epoch += EXTRA_PENTALTY / SECONDS_PER_DAY
            self.sky_state = np.array(self.targets.at(self.epoch, self.telescope, self.conditions)).T
            reward = -self.reward_config['exptime'] * EXTRA_PENTALTY
            done = (self.total_duration >= self.max_duration) or (len(self.targets) == 0)
            return self.sky_state, reward, done, {}



        # self.do_nothing_actions.append(action)
        self.targets[action].done = True
        self.observed_targets.append(self.targets[action])
        self.total_duration += exptime / SECONDS_PER_DAY
        self.epoch += exptime / SECONDS_PER_DAY

        self.sky_state = np.array(self.targets.at(self.epoch, self.telescope, self.conditions)).T

        reward = -self.reward_config['exptime'] * exptime + self.reward_config['n_observed_targets'] * len(self.observed_targets)
        done = (self.total_duration >= self.max_duration) or (len(self.observed_targets) == len(self.targets))

        if len(self.observed_targets) == len(self.targets):
            print(len(self.observed_targets), len(self.targets))
            print(f"[INFO] All targets observed. Done in {self.total_duration} days.")

        return self.sky_state, reward, done, {}

    def reset(self):
        self.__init__(self.init_targets, self.telescope, self.conditions, self.epoch, self.max_duration, self.reward_config)
        return self.sky_state

    def render(self, mode='human'):
        # Nothing to render for now
        pass