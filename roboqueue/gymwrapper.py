# gymwrapper.py
import gym
from gym import spaces
from roboqueue import TargetList, StationaryTarget
from spacerocks.utils import time_handler
import numpy as np

class TelescopeSchedulingEnv(gym.Env):
    def __init__(self, telescope, conditions, max_duration, sky_state, targets, reward_config):
        super(TelescopeSchedulingEnv, self).__init__()

        self.telescope = telescope
        self.conditions = conditions
        self.max_duration = max_duration
        self.sky_state = sky_state
        self.reward_config = reward_config
        self.total_duration = 0.0
        self.observed_targets = {}
        self.current_time = time_handler('12 February 2024').utc.jd[0] #time_handler.get_current_time()
        self.epoch = 0.0

        # Current observation
        self.init_targets = targets
        self.targets = targets

        # Action space for now is just a target object (since ordering a list)
        self.action_space = spaces.Discrete(len(self.sky_state)+1)

        # Observation space for each target includes ra, dec, alt, az, exptime
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(len(self.sky_state), 5), dtype=np.float32)

        print(f"[INFO] Observation space dim: {self.observation_space}, Action space dim: {self.action_space}")


    def step(self, action):
        # TODO: add logic for "do nothing"
        # index targets based on action to get single exptime
        ra, dec, alt, az, exptime = self.targets.targets[action].at(self.epoch, self.telescope, self.conditions)

        # Update the total duration and current time from selected action
        self.total_duration += self.observation[action][4]

        # Mark the target as observed
        self.observed_targets[action] = True

        # Update the action space to reflect the current number of targets
        self.action_space = spaces.Discrete(len(self.targets.targets)+1)

        # TODO: change action to index when removing target, make sure first option is "do nothing"

        # Reward for now is f(exptime, n_observed_targets)
        reward = -self.reward_config['exptime'] * exptime + self.reward_config['n_observed_targets'] * len(self.observed_targets)

        # Check if the episode has ended
        done = self.total_duration >= self.max_duration or len(self.targets.targets) == 0

        # Update the observation for sky state
        self.epoch = self.current_time + self.total_duration / 86400
        ra, dec, alt, az, exptime = self.targets.at(self.epoch, self.telescope, self.conditions)

        for star in self.observation:
            print('star', star)
            # only update remaining targets
            if star not in self.observed_targets:
                self.observation[star] = np.array([ra[star], dec[star], alt[star], az[star], exptime[star]])

        # Remove the target from list
        self.targets.targets.pop(action)

        # Update the current time
        self.current_time = self.epoch

        return self.observation, self.observed_targets, reward, done

    def reset(self):
        # Reset the state of the environment to an initial state
        self.observed_targets = {}
        self.targets = self.init_targets
        self.observation = self.sky_state

        return self.observation

    def render(self, mode='human'):
        # Nothing to render for now
        pass