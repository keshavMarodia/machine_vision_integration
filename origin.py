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
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import json
# from capture2 import Merging
from marks import Marks,table_Marks
from holes import Holes
# from control_page import excel

app = Flask(__name__)
CORS(app)

# @app.route('/start', methods=['GET'])
def start():
    bluetooth.write(b's')
    # nex()
    return jsonify({'message': 'Start command sent.'})

@app.route('/fetchphoto1', methods=['GET'])
def fetchphoto1():
    return cv2.imread('')

@app.route('/basler_camera', methods=['GET'])
def basler_camera():
    global Img1_path, Img2_path

    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    camera.Width.SetValue(4608)
    camera.Height = 3288

    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(50)


    if camera.IsPylonDeviceAttached() and camera.IsUsb():
        
        # Grabing Continusely (video) with minimal delayg
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        while camera.IsGrabbing():
            
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                #cv2.namedWindow('Live Camera', cv2.WINDOW_NORMAL)
                if List_position[-1] == 'origin':
                    Img1_path = r"Captured_images\Capture\Image1.jpg"
                    cv2.imwrite(Img1_path, img)
                    # myimage=ImageTk.PhotoImage(Image.open(Img1_path).resize((548,384)))
                    # final_image=Label(Frame1, image=myimage)
                    # final_image.myimage=myimage
                    # final_image.grid(row=5,column=0, pady=350)
                    break
                else:
                    Img2_path = r"Captured_images\Capture\Image2.jpg"
                    cv2.imwrite(Img2_path, img)
                    Merging()

                    break                      
             
            grabResult.Release()
            
        # Releasing the resource    
        camera.StopGrabbing()

    else:
        
        print("Camera is not connected... ")
    return jsonify({'message': 'basler camera clicked an image'})

def Merging():
    
    rot4 = cv2.imread(Img1_path)
    #img1_rot = cv2.rotate(rot4, cv2.cv2.ROTATE_90_CLOCKWISE)
    #cv2.imwrite("Delete/1.jpg", img1_rot)
    rot = cv2.imread(Img2_path)
    #img2_rot = cv2.rotate(rot, cv2.cv2.ROTATE_90_CLOCKWISE)
    #image1_rotation = cv2.rotate(src, cv2.cv2.ROTATE_90_CLOCKWISE)

    np_img = np.array(rot)

    #h1,w1 = np_img.shape[:2]
    #print (h1,w1)

    np_img_del = np.delete(np_img,np.s_[0:435],axis=0)
    #h2,w2 = np_img_del.shape[:2]

    cv2.imwrite(r"college-project\src\components\images\2.jpg", np_img_del)
   
    #im = cv2.imread('Delete/1.jpg')
    result = rot4[:,72:]

    y1 = cv2.imread(r'college-project\src\components\images\2.jpg')
    result1 = y1[:, :-72]

    im_h1_rot = np.vstack((result1,result))

    #print (h2,w2)
    
    #concatenate image 1 image 2
    #im_h1 = cv2.hconcat([img1_rot,np_img_del])
    #im_h1_rot = cv2.rotate(im_h1, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(r"college-project\src\components\images\concat.jpg", im_h1_rot)
    # myimage=ImageTk.PhotoImage(Image.open("Delete/concat.jpg").resize((548,768)))
    # final_image=Label(Frame1, image=myimage)
    # final_image.myimage=myimage
    # final_image.grid(row=0,column=0)

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

@app.route('/marking' , methods=['GET'])
def marks():
    tableMarks = Marks()
    return json.dumps(tableMarks)

@app.route('/holes' , methods=['GET'])
def holes():
    holes = Holes()
    return json.dumps(holes)

@app.route('/reference_table' , methods=['GET'])
def reference_table():
    global Final1
    data= pd.read_csv(r"C:\Users\ASUS\Desktop\Section_1.csv")
    Name_Count = data.query('Name=="Point"')
    Sort = Name_Count.sort_values(by='Position X')
    Sort.insert(0, 'ID', range(1, 1 + len(Sort)))
    Final1 = Sort.drop(['Count', 'Length',], axis=1)
    json_object = Final1.to_json(orient='records')
    return json.dumps(json_object)
    
   
    

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
    

    