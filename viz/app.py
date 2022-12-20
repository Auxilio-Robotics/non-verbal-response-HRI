"""! Flask app to serve the visualization of the non-verbal response HRI experiment."""

import os
import json
import logging
import random
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

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

        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        time.sleep(0.05)

# Initialize the Flask application
app = Flask(__name__)
app.config
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
