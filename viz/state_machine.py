#!/usr/bin/env python3
# Copyright (C) 2022 Auxilio Robotics

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# @file state_machine.py
# @brief Python program for the state machine

# @author Auxilio Robotics

# Imports
import numpy as np

"""! State machine for robot facial expressions"""
class StateMachine():
    """! Constructor
       @param dim Dimension of the image
    """
    def __init__(self, states, dim):
        self.valence_happy = 0
        self.arousal_happy = 200
        self.r_happy = dim//4
        self.theta_happy = -0.6

        self.valence_sad = 189
        self.arousal_sad = -84
        self.r_sad = 0
        self.theta_sad = 0

        self.valence_neutral = 0
        self.arousal_neutral = dim//2
        self.r_neutral = 0
        self.theta_neutral = 0

        self.valence = self.valence_neutral
        self.arousal = self.arousal_neutral
        self.r = self.r_neutral
        self.theta = self.theta_neutral
        self.state = 'neutral'

        self.counter = 0
        self.counter_max = 0
        self.transitinPoints = np.empty((1,4))

        self.states = states
        self.state_index = 0
        self.dim = dim

    """! brief Get the current state
       @return Current state
    """
    def getState(self):
        return self.state

    """! Get the current parameters
         @return Current parameters
    """
    # \return Current parameters
    def getParams(self):
        if (self.counter == self.counter_max):
            self.state_index += 1
            if self.state_index == len(self.states):
                self.state_index = 0
            self.setState(self.states[self.state_index])

        if self.counter < self.counter_max:
            self.valence = self.transitionPoints[0][self.counter]
            self.arousal = self.transitionPoints[1][self.counter]
            self.r = self.transitionPoints[2][self.counter]
            self.theta = self.transitionPoints[3][self.counter]
            self.counter += 1
        return [self.r, self.theta, self.arousal, self.valence]

    """! Set the current state
         @param new_state New state
    """
    def setState(self, new_state):
        if self.state == 'neutral':
            if new_state == 'happy':
                self.transitionPoints = [np.linspace(self.valence_neutral, self.valence_happy, 50), 
                                         np.linspace(self.arousal_neutral, self.arousal_happy, 50), 
                                         np.linspace(self.r_neutral, self.r_happy, 50), 
                                         np.linspace(self.theta_neutral, self.theta_happy, 50)]
                self.counter = 0
                self.counter_max = len(self.transitionPoints[0])
                self.state = 'happy'
            if new_state == 'sad':
                self.transitionPoints = [np.linspace(0, self.valence_sad, 50), 
                                         np.linspace(-self.dim//2, self.arousal_sad, 50), 
                                         np.linspace(0, self.r_sad, 50), 
                                         np.linspace(0, self.theta_sad, 50)]
                self.counter = 0
                self.counter_max = len(self.transitionPoints[0])
                self.state = 'sad'
            if new_state == 'neutral':
                self.transitionPoints = np.empty((1,4))
                self.counter = 0
                self.counter_max = 0
                self.state = 'neutral'
        elif self.state == 'happy':
                if new_state == 'neutral':
                    self.transitionPoints = [np.linspace(self.valence_happy, self.valence_neutral, 50),
                                             np.linspace(self.arousal_happy, self.arousal_neutral, 50), 
                                             np.linspace(self.r_happy, self.r_neutral, 50), 
                                             np.linspace(self.theta_happy, self.theta_neutral, 50)]
                    self.counter = 0
                    self.counter_max = len(self.transitionPoints[0])
                    self.state = 'neutral'
                if new_state == 'sad':
                    self.transitionPoints = [np.hstack((np.linspace(self.valence_happy, 0, 25).reshape(1,25), np.linspace(0, self.valence_sad, 25).reshape(1,25))).reshape(50,), 
                                             np.hstack((np.linspace(self.arousal_happy, self.dim//2, 25).reshape(1,25), np.linspace(-self.dim//2, self.arousal_sad, 25).reshape(1,25))).reshape(50,), 
                                             np.linspace(self.r_happy, self.r_sad, 50), 
                                             np.linspace(self.theta_happy, self.theta_sad, 50)]
                    self.counter = 0
                    self.counter_max = len(self.transitionPoints[0])
                    self.state = 'sad'
                if new_state == 'happy':
                    self.transitionPoints = np.empty((1,4))
                    self.counter = 0
                    self.counter_max = 0
                    self.state = 'happy'
        elif self.state == 'sad':
                if new_state == 'neutral':
                    self.transitionPoints = [np.linspace(self.valence_sad, 0, 50), 
                                             np.linspace(self.arousal_sad, -self.dim//2, 50), 
                                             np.linspace(self.r_sad, self.r_neutral, 50), 
                                             np.linspace(self.theta_sad, self.theta_neutral, 50)]
                    self.counter = 0
                    self.counter_max = len(self.transitionPoints[0])
                    self.state = 'neutral'
                if new_state == 'happy':
                    self.transitionPoints = [np.hstack((np.linspace(self.valence_sad, 0, 25).reshape(1,25), np.linspace(self.valence_neutral, self.valence_happy, 25).reshape(1,25))).reshape(50,), 
                                             np.hstack((np.linspace(self.arousal_sad, -self.dim//2, 25).reshape(1,25), np.linspace(self.arousal_neutral, self.arousal_happy, 25).reshape(1,25))).reshape(50,), 
                                             np.linspace(self.r_sad, self.r_happy, 50), 
                                             np.linspace(self.theta_sad, self.theta_happy, 50)]
                    self.counter = 0
                    self.counter_max = len(self.transitionPoints[0])
                    self.state = 'happy'
                if new_state == 'sad':
                    self.transitionPoints = np.empty((1,4))
                    self.counter = 0
                    self.counter_max = 0
                    self.state = 'sad'
