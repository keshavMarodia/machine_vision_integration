from control_page import *
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
from control_page import Final_Merge

def Torque():

    s=1
    for m in range(1,3):

        imagepath = "Captured_images/Capture/Image" + str(m) + ".jpg"

        #---------------------------------Holes Model----------------------------------------------

        subprocess.run(f"python Yolo_torque/detect.py --weights {'Yolo_torque/best_recent.pt'} --source {imagepath} --img {'1644'} ")
        
        #------------------------------------------------------------------------------------------

        img = cv2.imread(imagepath)

        f = open(r"Coordinates/coordinates_torque.txt","r")
        array_created = np.full((3288, 4608, 3), 255, dtype = np.uint8)

        lines = [line.rstrip() for line in f]
        print(lines)

        for i in range(len(lines)):
            string = lines[i]
            lst = string.split(',')
            roi = img[int(lst[1])-100:int(lst[3])+100, int(lst[0])-100:int(lst[2])+100]
            array_created[int(lst[1])-100:int(lst[3])+100, int(lst[0])-100:int(lst[2])+100] = roi
            hsv = cv2.cvtColor(array_created, cv2.COLOR_BGR2HSV)


            # Defining lower and upper bound HSV values
            lower = np.array([0, 151, 0])
            upper = np.array([22, 255, 255])

            # Defining mask for detecting color
            mask = cv2.inRange(hsv, lower, upper)
            no_red = cv2.countNonZero(mask)
            if no_red >= 200:
                print('The number of brown pixels is: ' + str(no_red), 'Approval state: Yes')
            else:
                print('The number of brown pixels is: ' + str(no_red), 'Approval state: No')
        for i in range (len(lines)):
            cv2.putText(array_created, "T{s}:", (lines[0]+20, lines[1]-20),cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)
            s +=1
        if m == 1:
            cv2.imwrite("Delete/1.jpg", array_created)
        else:
            cv2.imwrite("Delete/2.jpg", array_created)
    Final_Merge()