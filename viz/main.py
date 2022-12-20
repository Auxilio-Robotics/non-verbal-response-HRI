# kivy app to display an image on an iPad

# Path: non-verbal-response-HRI/viz/kivy.py

import os
import json
import logging
import random
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window

from viz import Visualizer
from state_machine import StateMachine

"""! Generate frames for the visualization"""
def generate_frames():
    states = ['neutral', 'happy', 'sad', 'neutral', 'sad', 'happy', 'neutral']
    state_machine = StateMachine(states, 512)
    current_state = state_machine.getState()

    viz = Visualizer()
    viz.setParams(state_machine.getParams())

    while(1):
        print('state: ', state_machine.getState())

        params = state_machine.getParams()
        viz.setParams(params)
        eyes = viz.drawEyes()

        ret, buffer = cv2.imencode('.jpg', eyes)
        frame = buffer.tobytes()

        texture = Texture.create(size=(500, 500), colorfmt="rgb")
        texture.blit_buffer(frame, bufferfmt="ubyte", colorfmt="rgb")
        
        yield texture

class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.image = Image()
class TestApp(App):
    def build(self):
        self.image.texture = generate_frames()
        return self.image

if __name__ == '__main__':
    TestApp().run()
