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


def table_Holes():
    game_frame = Frame(second_frame)
        
    game_frame.grid(row=5, column = 3, sticky = 'W', padx = 10, pady = 10)

    my_game = ttk.Treeview(game_frame, show = 'headings', height=10)



    verscrlbar = ttk.Scrollbar(game_frame, orient ="vertical", command = my_game.yview)
    verscrlbar.pack(side ='right', fill ='x')
    # Calling pack method w.r.to vertical
    # scrollbar
    

    # Configuring treeview
    my_game.configure(xscrollcommand = verscrlbar.set)   
    my_game.pack()

    my_game['columns'] = ('S_No', 'Center_ID', 'Reference1', 'Reference3', 'Diameter', 'Approval_state')

    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("S_No",anchor=CENTER,width=40)
    my_game.column("Center_ID",anchor=CENTER,width=40)
    my_game.column("Reference1",anchor=CENTER,width=130)
    #my_game.column("Reference2",anchor=CENTER,width=130)
    my_game.column("Reference3",anchor=CENTER,width=150)
    my_game.column("Diameter",anchor=CENTER,width=70)
    my_game.column("Approval_state",anchor=CENTER,width=70)

    #Create Headings 
    my_game.heading("#0",text="",anchor=CENTER)
    my_game.heading("S_No",text="ID",anchor=CENTER)
    my_game.heading("Center_ID",text="ID",anchor=CENTER)
    my_game.heading("Reference1",text="Center_X",anchor=CENTER)
    #my_game.heading("Reference2",text="Horizontal_Reference2",anchor=CENTER)
    my_game.heading("Reference3",text="Center_Y",anchor=CENTER)
    my_game.heading("Diameter",text="Diameter",anchor=CENTER)
    my_game.heading("Approval_state",text="Approval",anchor=CENTER)


    Final_dim = []
    for i in range(len(Final_Dimension2_list)):
        if Final_Dimension2_list[i] <= 35:
            Final = Final_Dimension2_list[i] #- 0.5
            Final_dim.append(Final)
            
        else:
            Final_dim.append(Final_Dimension2_list[i])



    for i in range(len(flatList)):
        my_game.insert(parent='',index='end',iid=i,text='',
        values=(i+1, flatList[i],Final_dim[i],Final_Dimension3_list[i], (Diameter_List[i]), 'Yes'))
        
def Holes():
    global Centers,  Final_Dimension, Final_Dimension1, Final_Dimension3, straight, Curve,Final_Dimension1_list,Final_Dimension2_list,Final_Dimension3_list,m, Centers_final,flatList, Diameter_List
    bars()
    
    Centers_final = []
    coordinates_final = []
    
    k=1
    s=1
    Final_Dimension1_list = []
    Final_Dimension2_list = []
    Final_Dimension3_list = []
    Diameter_List = []
    for m in range(1,3):

        
        imagepath = "Captured_images/Capture/Image" + str(m) + ".jpg"    
        #---------------------------------------------------------------------------Holes Model

        subprocess.run(f"python Yolo_Holes/detect.py --weights {'Yolo_Holes/best.pt'} --source {imagepath} --img {'512'} --iou {'0.1'}  --conf {'0.7'}")
        
        #------------------------------------------------------------------------------------------


        img = cv2.imread(imagepath)
        array_created = np.full((3288, 4608, 3), 255, dtype = np.uint8)

        f = open("Coordinates/coordinates_Holes.txt","r")

        lines = [line.rstrip() for line in f]

        for i in range(len(lines)):
            string = lines[i]
            lst = string.split(',')
            roi = img[int(lst[1]):int(lst[3]), int(lst[0]):int(lst[2])]
            array_created[int(lst[1]):int(lst[3]), int(lst[0]):int(lst[2])] = roi

        th, dst = cv2.threshold(array_created, 75, 255, cv2.THRESH_BINARY)

        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        th1, dst1 = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(dst1,kernel,iterations = 1)

        imagem = cv2.bitwise_not(erosion)
        cv2.imwrite('Delete/INVERT.jpg', imagem)

        image_final = cv2.imread('Delete/INVERT.jpg')

        gray = cv2.cvtColor(image_final, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5),
                            cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur, 200, 255,
                                cv2.THRESH_BINARY_INV)

        contours, hierarchies = cv2.findContours(  thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        Radius = []


        blank = np.zeros(thresh.shape[:2],
                        dtype='uint8')

        cv2.drawContours(blank, contours, -1,
                        (255, 0, 0), 1)
        for i in range(len(contours)):
            cnt = contours[i]
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            Radius.append(radius)
            #cv2.imwrite("img"+str(k)+".jpg", blank)
            
                    
        Dict = {}
        Centers = []
        coordinates = []
        

        for i in contours:
            M = cv2.moments(i)
            if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    area = cv2.contourArea(i)                
                    cv2.drawContours(image_final, [i], -1, (0, 255, 0), 1)
                    cv2.circle(image_final, (cx, cy), 1, (0, 0, 255), -1)
                    #cv2.putText(imagepath, "center", (cx - 20, cy - 20),
                                    #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    
            #Dict['c',i+1] = [cx,cy]
            if area >= 100:
                Centers.append('c'+ str(k))
                coordinates.append([cx, cy])
                k += 1
            else:
                continue


        #cv2.imwrite("Delete/image.png", image_final)
        if [2303,1643] in coordinates:
            k -= 1
        else:
            continue

        index_value = coordinates.index([2303,1643])
        if [2303,1643] in coordinates:
            del Centers[index_value]
            del coordinates[index_value]
            del Radius[index_value]
        else:
            print("Nothing to delete")

        for i in range(len(Centers)):
            Dict[Centers[i]] = coordinates[i]

        for straight in range(len(Centers)):
            if m == 1:
                #print(Bar1)
                #print(Bar2)
                Distance_pixels = int(Two_images_bars[1]) - int(coordinates[straight][0])
                Distance_pixels1 = int(coordinates[straight][0] - int(Two_images_bars[0]))
                Final_Dimension = int(Distance_pixels)/float(55)
                Final_Dimension = round(Final_Dimension, 1)
                Final_Dimension1 = int(Distance_pixels1)/float(55)
                Final_Dimension1 = round(Final_Dimension1, 1)
                Final_Dimension1_list.append(Final_Dimension)
                Final_Dimension2_list.append(Final_Dimension1)
                #print(Bar1,  coordinates[i][0], Bar2)
                #Final_dimensions()
                #print(Final_Dimension+Final_Dimension1)
            else:
                Distance_pixels = int(Two_images_bars[3]) - int(coordinates[straight][0])
                Distance_pixels1 = int(coordinates[straight][0] - int(Two_images_bars[2]))
                Final_Dimension = int(Distance_pixels)/float(55)
                Final_Dimension = round(Final_Dimension, 1)
                Final_Dimension1 = int(Distance_pixels1)/float(55)
                Final_Dimension1 = round(Final_Dimension1, 1)
                Final_Dimension1_list.append(Final_Dimension)
                Final_Dimension2_list.append(Final_Dimension1)
                #print(Bar1,  coordinates[i][0], Bar2)
                #Final_dimensions()
                #print(Final_Dimension+Final_Dimension1)                
        if m == 1:
            for Curve in range(len(Centers)):
                Distance_pixels = int(Reference_line1) - int(coordinates[Curve][1])
                Final_Dimension3 = int(Distance_pixels)/int(53)
                Final_Dimension3 = round(Final_Dimension3, 1)
                Final_Dimension3_list.append(Final_Dimension3)
                #Final_dimensions2()
        else:
            for Curve in range(len(Centers)):
                Distance_pixels = int(int(coordinates[Curve][1] - Reference_line2) )
                Final_Dimension3 = int(105.3) - (int(Distance_pixels)/int(53)) 
                Final_Dimension3 = round(Final_Dimension3, 1)
                Final_Dimension3_list.append(Final_Dimension3)
                        #Final_dimensions2()
        if m == 1:
            for Curve in range(len(Radius)):
                Diameter = round((((Radius[Curve]/57)*2)*10),1)
                Diameter_List.append(Diameter)
        else:
            for Curve in range(len(Radius)):
                Diameter = round((((Radius[Curve]/57)*2)*10),1)
                Diameter_List.append(Diameter)

        Centers_final.append(Centers)
        coordinates_final.append(coordinates)
        
        for i in range (len(coordinates)):
            cv2.putText(img, "C"+ str(s), (coordinates[i]),cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)
            s +=1
        if m == 1:
            cv2.imwrite("Delete/1.jpg", img)
        else:
            cv2.imwrite("Delete/2.jpg", img)
    flatList = [ item for elem in Centers_final for item in elem]
    Final_Dimension2_list,Final_Dimension3_list,flatList, Diameter_List=[list(v) for v in zip(*sorted(zip(Final_Dimension2_list,Final_Dimension3_list,flatList,Diameter_List)))]
    Final_Merge()
    table_Holes()