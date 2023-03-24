from fileinput import filename
import os
import subprocess
from turtle import bgcolor
from unittest import main
import cv2
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from re import L
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk,Image   
import time
import tkinter.font as font
import serial
from pypylon import pylon
import shutil
import math
from tkinter.filedialog import asksaveasfilename, askopenfilename
import pandas as pd
from flask import Flask,jsonify
from flask_restful import Resource, Api, reqparse
from capture2 import basler_camera

app = Flask(__name__)

# @app.route('/start', methods=['GET'])
def start():
    bluetooth.write(b's')
    # nex()
    return jsonify({'message': 'Start command sent.'})

@app.route('/basler_camera', methods=['GET'])
def call_capture():
    basler_camera()

# @app.route('/nex', methods=['POST'])
def nex():
    bluetooth.write(b'h')
    return jsonify({'message': 'Nex command sent.'})

@app.route('/first_frame', methods=['GET'])
def first_frame():
    bluetooth.write(b'b')
    # nex()
    List_position.append("Second_frame")
    return jsonify({'message': 'First frame command sent.'})

@app.route('/on_origin', methods=['GET'])
def on_origin():
    bluetooth.write(b's')
    nex()
    List_position.append("origin")
    return jsonify({'message': 'On origin command sent.'})

# @app.route('/on_closing', methods=['POST'])
# def on_closing():
#     # k.withdraw()
#     bluetooth.write(b's')
#     nex()
#     quit()

# @app.route('/arduino', methods=['GET'])
def arduino():
    global port, List_position, bluetooth
    port = "COM10"
    bluetooth = serial.Serial(port, 9600)
    bluetooth.flushInput()
    List_position = ['origin']
    # on_origin()
    # return jsonify({'message': 'Arduino function executed.'})

if __name__ == '__main__':
    arduino()
    app.run()
    # start()
    

    
