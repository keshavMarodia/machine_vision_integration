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
                    myimage=ImageTk.PhotoImage(Image.open(Img1_path).resize((548,384)))
                    final_image=Label(Frame1, image=myimage)
                    final_image.myimage=myimage
                    final_image.grid(row=5,column=0, pady=350)
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