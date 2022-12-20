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

# @file viz.py
# @brief Python program for HRI visualization

# @author Auxilio Robotics

# Imports
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

from state_machine import StateMachine

"""! Visualizer class for the HRI eyes"""
class Visualizer():
    """! Constructor

    """
    def __init__(self, draw=True, dim=512, eyeRad=85, ix=-1, iy=-1):
        self.drawing = True # true if mouse is pressed

        self.ix = ix
        self.iy = iy

        self.eyeRad = eyeRad
        self.dim = dim

        self.params = np.zeros((4,), float)
        self.params[0] = 0
        self.params[1] = 0
        self.params[2] = self.dim//2
        self.params[3] = 0
        self.img = np.zeros((dim,dim,3), np.uint8)

    """! Set the parameters
        @param params Parameters
    """
    def setParams(self, params):
        self.params = params

    """! Get the parameters
        @return Parameters
    """
    def getParams(self):
        return self.params

    """! Get the image
        @return Image
    """
    def getImg(self):
        return self.img

    """! Draw the pupil
        @param eyeImg Eye image
        @return Eye image with pupil
    """
    def drawPupil(self, eyeImg):
        r, theta, arousal, valence = self.params
        dim = self.dim
        eyeRad = self.eyeRad

        eyemask = eyeImg.copy()
        cv2.circle(eyemask, (dim//2, dim//2), dim//2, (0, 0, 0), -1)

        cv2.circle(eyeImg, (dim//2, dim//2), dim//2, (255, 255, 255), -1) # white eye
        cv2.circle(eyeImg, (dim//2, dim//2), dim//2, (0, 0, 0), 3) # white eye
        cv2.circle(eyeImg, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), eyeRad, (0, 0, 0), -1) # pupil

        return eyeImg

    """! Draw the eye lid
        @param left Left eye
        @return Eye image with eye lid
    """
    def drawEyeLid(self, eyeImg, left = False):
        r, theta, arousal, valence = self.params
        dim = self.dim

        if left:
            cv2.circle(eyeImg, (dim//2 - int(valence), int(arousal) * 4), dim, (0, 0, 0), -1)
        else:
            cv2.circle(eyeImg, (dim//2 + int(valence), int(arousal) * 4), dim, (0, 0, 0), -1)

        return eyeImg

    """! Draw the eyes
        @return Image with eyes
    """
    def drawEyes(self):
        self.img = np.zeros((512,512,3), np.uint8) * 255
        # print(self.img)
        img = self.img
        # print(img)
        dim = self.dim
        params = self.params

        limg = self.drawPupil(img.copy())
        rimg = self.drawPupil(img.copy())
        limg = self.drawEyeLid(limg, True)
        rimg = self.drawEyeLid(rimg, False)

        eyemask = img.copy()
        cv2.circle(eyemask, (dim//2, dim//2), dim//2, (0, 0, 0), -1)
        limg[eyemask == 255] = 255
        rimg[eyemask == 255] = 255

        # pad left eye and right eye by 50 pixels
        limg = cv2.copyMakeBorder(limg, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        rimg = cv2.copyMakeBorder(rimg, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        self.img = np.hstack((limg, rimg))

        # pad on the right and left by 50 pixels
        self.img = cv2.copyMakeBorder(self.img, 0, 0, 50, 50, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # resize to full HD resolution
        self.img = cv2.resize(self.img, (2560, 1664))

        return self.img


if __name__ == '__main__':
    inc = 0

    states = ['neutral', 'happy', 'sad', 'neutral', 'sad', 'happy', 'neutral']
    state_idx = 0
    state_machine = StateMachine(512)
    current_state = state_machine.getState()

    viz = Visualizer()
    viz.setParams(state_machine.getParams())

    while(1):
        print('inc: ', inc)
        print('state: ', state_machine.getState())

        if inc == 50:
            state_idx += 1
            if state_idx >= len(states):
                state_idx = 0
            state_machine.setState(states[state_idx])
            inc = 0

        params = state_machine.getParams()
        viz.setParams(params)
        eyes = viz.drawEyes()
        # eye = np.hstack([eye, eye])
        inc += 1
        # cv2.imshow('a', eye)
        plt.imshow(eyes)

        plt.pause(0.001)
        plt.clf()
    