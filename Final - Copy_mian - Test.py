#----------------------------------------------------------------------Libraries----------------------------------------------------------------------
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

# from marks import *
from origin import *

#--------------------------------------------------------------------Starting-------------------------------------------------------------------------
Reference_line1 = 2855
Reference_line2 = 317
def initial():
    global Reference_line1, Reference_line2


    try:
        os.mkdir("Delete")
    except:
        shutil.rmtree("Delete")
        os.mkdir("Delete")
    try:
        os.mkdir("Coordinates")
    except:
        shutil.rmtree("Coordinates/")
        os.mkdir("Coordinates/")
    try:
        os.mkdir("Captured_images")
    except:
        print("")

    try:
        os.mkdir("Captured_images/Capture")
    except:
        shutil.rmtree("Captured_images/Capture")
        os.mkdir("Captured_images/Capture")
        
# def Arduino():
#     global port, List_position, bluetooth
#     port="COM10" #This will be different for various devices and on windows it will probably be a COM port.
#     bluetooth=serial.Serial(port, 9600) #Start communications with the bluetooth unit
#     #print("Connected")
#     bluetooth.flushInput() #This gives the bluetooth a little kick
#     List_position = ['origin']
# -------------------------------------------------------------------commands--------------------------------------------------------------------------
# def start():
#     bluetooth.write(b's')#These need to be bytes not unicode, plus a number NO = Red, NC = Orange
#     nex()                                                                                                                                           
# def nex():    
#     bluetooth.write(b'h')#These need to be bytes not unicode, plus a number NO = Red, NC = Orange
# def first_frame():
#      bluetooth.write(b'b')#These need to be bytes not unicode, plus a number
#      List_position.append("Second_frame")
# def on_origin():
#     bluetooth.write(b"s")
#     nex() 
#     List_position.append("origin")   #origin button function 
# def on_closing():
#      k.withdraw()
#      bluetooth.write(b"s")#These need to be bytes not unicode, plus a number
#      nex()
#      quit()
#-------------------------------------------------------------------GUI-------------------------------------------------------------------------------  
def GUI():
    global L1, var,r
    global r, buttonFont
    r = tk.Tk()
    r.state('zoomed')
    r.title('Stepper Motor')

    r.iconbitmap("images/icon.ico")

    icon=Image.open("images/icon.jpg")

    new1=ImageTk.PhotoImage(icon)
    logo=Label(r,image=new1).pack()
    buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
    var = StringVar()
    #sel()


    var.set("Select Type")

    #Create a dropdown Menu
    drop= OptionMenu(r, var,"Marking", "Drilling", "Torqueing", "Wire_Locking").pack()

    username_label =Label(r,text="Username:",font="Times 18 bold")
    username_label.pack(padx=80)
    username = Entry(r,font="Times 16 bold")
    username.pack()
  
    password_label =Label(r, text="Password:", font="Times 18 bold").pack()
    password = Entry(r, show="*",font="Times 16 bold")
    password.pack()

    Login_page = Button(r, text='Login',height= 1, width=10, font=buttonFont, command=class_selected).pack(pady= 20)


    r.mainloop()
#----------------------------------------------------------------GUI main page------------------------------------------------------------------------
def main_page():
    r.destroy()
    
    global  Frame1, Frame2, second_frame, ktext
    start()

    k = tk.Tk()
    k.state('zoomed')

    main_frame = Frame(k)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar1 = ttk.Scrollbar(main_frame, orient= HORIZONTAL, command=my_canvas.xview)
    my_scrollbar1.pack(side=BOTTOM, fill=X)

    my_scrollbar = ttk.Scrollbar(main_frame, orient= VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    

    my_canvas.configure(xscrollcommand=my_scrollbar1.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
    

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    Frame1 = LabelFrame(second_frame, text="Captured Image",bg = "grey",  
                bd=10,width=3288/6,height=4608/6)
    Frame1.grid(row=4, column = 1, rowspan=2, sticky = 'W', padx = 10, pady = 10)
    Frame1.grid_propagate(0)
    Frame2 = LabelFrame(second_frame, text="Reference Image",bg = "grey",  
                bd=10,width=3288/6,height=4608/6)
    Frame2.grid(row=4, column = 2, rowspan=2,sticky = 'W', padx = 10, pady = 10)
    Frame2.grid_propagate(0)
    button1 = Button(second_frame, text='origin', height= 1, width=10, font=buttonFont)
    button1.config(command=on_origin)
    #button1.pack(pady= 10)
    button1.grid(row = 6, columnspan= 2, sticky = 'W', padx = 100, pady = 10)
    button3 = Button(second_frame , text='Next_frame',height= 1, width=10, font=buttonFont)
    button3.config(command=first_frame)
    #button3.pack(pady= 10)
    button4 = Button(second_frame , text='Capture',height= 1, width=10, font=buttonFont)
    button4.config(command=basler_camera)
    #button4.pack(pady= 10)
    button5 = Button(second_frame , text='Process',height= 1, width=10, font=buttonFont)
    button5.config(command=condition)
    k.protocol("WM_DELETE_WINDOW", on_closing)
    button3.grid(row = 6, columnspan = 2, sticky = 'E', padx = 150, pady = 10)
    button4.grid(row = 7, columnspan = 2, sticky = 'W', padx = 100, pady = 10)
    button5.grid(row = 7, columnspan = 2, sticky = 'E', padx = 150, pady = 10)
    var1 = StringVar()
    var2 = StringVar()
    var1.set("Select Section")
    var2.set("Select Section")
    #Create a dropdown Menu
    Parent_section= OptionMenu(second_frame, var1,"A1", "A2","A3", "A4","A5", "A6").grid(row = 6, column = 2, sticky = 'ew', padx = 50, pady = 10)
    Child_section= OptionMenu(second_frame, var2,"1", "2","3", "4","5", "6","7", "8").grid(row = 7, column = 2, sticky = 'ew', padx = 50, pady = 10)
    if selected == "Marking" or selected == "Drilling":
        
        button5 = Button(second_frame , text='upload',height= 1, width=10, font=buttonFont)
        #button5.config(command=condition)
        button5.grid(row = 8, columnspan=3, sticky = 'E', padx = 100, pady = 10)

        upload_file = Menubutton(second_frame, height= 1, width=10,text = "Choose File",relief=RAISED, font=buttonFont)
        upload_file.menu=Menu(upload_file,tearoff=False)
        upload_file["menu"]=upload_file.menu
        #upload_file.menu.add_command(label="Take a photo", command=camera)
        upload_file.menu.add_command(label="Choose from files", command=files)
        upload_file.grid(row = 8, columnspan=3, pady = 10, padx =(750,0) ,sticky='w')    
    else:
        print("")    

    k.mainloop()
#----------------------------------------------------------------File Chossing------------------------------------------------------------------------
def files():
    global pic, csv_path
    second_frame.filename=askopenfilename(defaultextension="Cad Drawings",title="Choose a file",filetypes=[("png files","*.png"),("jpg files","*.jpg")])
    pic=second_frame.filename
    csv_path = os.path.splitext(pic)[0]
    

    excel()
    my_image = ImageTk.PhotoImage(Image.open(pic).resize((548,768)))
    my_Label = Label(Frame2, image = my_image)
    my_Label.my_image=my_image
    my_Label.grid(row=0,column=0, padx=(0,30), pady=(0,30))
    return pic
#----------------------------------------------------------------Merging------------------------------------------------------------------------------
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

    cv2.imwrite("Delete/2.jpg", np_img_del)
   
    #im = cv2.imread('Delete/1.jpg')
    result = rot4[:,72:]

    y1 = cv2.imread('Delete/2.jpg')
    result1 = y1[:, :-72]

    im_h1_rot = np.vstack((result1,result))

    #print (h2,w2)
    
    #concatenate image 1 image 2
    #im_h1 = cv2.hconcat([img1_rot,np_img_del])
    #im_h1_rot = cv2.rotate(im_h1, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite("Delete/concat.jpg", im_h1_rot)
    myimage=ImageTk.PhotoImage(Image.open("Delete/concat.jpg").resize((548,768)))
    final_image=Label(Frame1, image=myimage)
    final_image.myimage=myimage
    final_image.grid(row=0,column=0)
def Final_Merge():
    IMG1 = cv2.imread("Delete/1.jpg")
    img1_rot = cv2.rotate(IMG1, cv2.ROTATE_90_CLOCKWISE)

    IMG2 = cv2.imread("Delete/2.jpg")
    img2_rot = cv2.rotate(IMG2, cv2.ROTATE_90_CLOCKWISE)

    np_img = np.array(img2_rot)

    h1,w1 = np_img.shape[:2]
    #print (h1,w1)

    np_img_del = np.delete(np_img,np.s_[0:435],axis=1)

    h2,w2 = np_img_del.shape[:2]
    #print (h2,w2)

    #concatenate image 1 image 2
    im_h1 = cv2.hconcat([img1_rot,np_img_del])
    im_h1_rot = cv2.rotate(im_h1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite("Delete/concat_Final.jpg", im_h1_rot)
    myimage=ImageTk.PhotoImage(Image.open("Delete/concat_Final.jpg").resize((548,768)))
    final_image=Label(Frame2, image=myimage)
    final_image.myimage=myimage
    final_image.grid(row=0,column=0)
#-----------------------------------------------------------------Camera------------------------------------------------------------------------------
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
#------------------------------------------------------------------Choose-----------------------------------------------------------------------------  
def choose():

    if selected == "Marking":
        Marks()
        
    elif selected == "Drilling":
        Holes()
    else:
        Torque()
#------------------------------------------------------------------Bars-------------------------------------------------------------------------------  
def bars():
    global Bar1, Bar2,Two_images_bars 
    Two_images_bars = []

    for m in range (1,3):
        imagepath = "Captured_images/Capture/Image" + str(m) + ".jpg"
        for i in range(1):
            print("yes")
            subprocess.run(f"python Yolo_Bars/detect.py --weights {'Yolo_Bars/best.pt'} --source {imagepath} --img {'512'} --iou {'0.1'} --conf {'0.5'}")
            print("No")

        img = cv2.imread(imagepath)
        array_created = np.full((3288, 4608, 3), 255, dtype = np.uint8)

        f = open("Coordinates/coordinates_Bars.txt","r")

        Bars_ref = []

        lines = [line.rstrip() for line in f]

        for i in range(len(lines)):
            string = lines[i]
            lst = string.split(',')
            Dist_x = round((int(lst[2]) - int(lst[0]))/2) 
            Dist_y = round((int(lst[3]) - int(lst[1]))/2)

            center_x = int(lst[0]) + (Dist_x)
            center_y = int(lst[1]) + (Dist_y)
            Bars_ref.append(center_x)
            
        if len(Bars_ref) == 1:
            Label(second_frame, text = "One Bar Identified", bg = 'orange').grid(row = 6 , column = 5, sticky = 'W', padx = 10, pady = 0)
            break
        else:
            try:
                Bar1 = min(Bars_ref) + round(53/2)
                Two_images_bars.append(Bar1)
                Bar2 = max(Bars_ref) - round(53/2)
                Two_images_bars.append(Bar2)
            except:
                Label(second_frame, text = "No Bars Identified", bg = 'orange').grid(row = 6 , column = 5, sticky = 'W', padx = 10, pady = 0)
                break 
#------------------------------------------------------------------Holes------------------------------------------------------------------------------  
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
# ------------------------------------------------------------------Marks------------------------------------------------------------------------------      
def Marks():
    global Centers,  Final_Dimension, Final_Dimension1, Final_Dimension3, straight, Curve,Final_Dimension1_list,Final_Dimension2_list,Final_Dimension3_list, m,Centers_final,flatList
    bars()
    
    Centers_final = []
    coordinates_final = []
    k=1
    s=1
    Final_Dimension1_list = []
    Final_Dimension2_list = []
    Final_Dimension3_list = []
    for m in range(1,3):

        imagepath = "Captured_images/Capture/Image" + str(m) + ".jpg"

        #---------------------------------Holes Model----------------------------------------------

        subprocess.run(f"python Yolo_Marks/detect.py --weights {'Yolo_Marks/best.pt'} --source {imagepath} --img {'512'} --iou {'0.1'} --conf {'0.7'}")
        
        #------------------------------------------------------------------------------------------

        img = cv2.imread(imagepath)
        array_created = np.full((3288, 4608, 3), 255, dtype = np.uint8)

        f = open("Coordinates/coordinates_Marks.txt","r")

        lines = [line.rstrip() for line in f]

        for i in range(len(lines)):
            string = lines[i]
            lst = string.split(',')
            roi = img[int(lst[1]):int(lst[3]), int(lst[0]):int(lst[2])]
            array_created[int(lst[1]):int(lst[3]), int(lst[0]):int(lst[2])] = roi

        th, dst = cv2.threshold(array_created, 75, 255, cv2.THRESH_BINARY)

        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        th1, dst1 = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)

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

        blank = np.zeros(thresh.shape[:2],
                        dtype='uint8')

        cv2.drawContours(blank, contours, -1,
                        (255, 0, 0), 1)

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
                    cv2.putText(image_final, "", (cx - 20, cy - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    
            if area >= 100:
                Centers.append('c'+ str(k))
                coordinates.append([cx, cy])
                k += 1
            else:
                continue
        if [2303,1643] in coordinates:
            k -= 1
        else:
            continue

        if [2303,1643] in coordinates:
            index_value = coordinates.index([2303,1643])
            del Centers[index_value]
            del coordinates[index_value]
        else:
            print("Nothing to delete")

        for i in range(len(Centers)):
            Dict[Centers[i]] = coordinates[i]

        for straight in range(len(Centers)):
            if m == 1:
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
                #print(Final_Dimension,Final_Dimension1)
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
                #print(Final_Dimension,Final_Dimension1) 
        for Curve in range(len(Centers)):              
            if m == 1:
                Distance_pixels2 = int(Reference_line1) - int(coordinates[Curve][1])
                Final_Dimension3 = int(Distance_pixels2)/int(53)
                Final_Dimension3 = round(Final_Dimension3, 1)
                Final_Dimension3_list.append(Final_Dimension3)
                #Final_dimensions2()
        
            else:
                Distance_pixels2 = int(coordinates[Curve][1] - int(Reference_line2))
                Final_Dimension3 = int(105.3) - (int(Distance_pixels2)/int(53))
                Final_Dimension3 = round(Final_Dimension3, 1)
                Final_Dimension3_list.append(Final_Dimension3)
                #Final_dimensions2() 

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
    Final_Dimension2_list,Final_Dimension3_list,flatList=[list(v) for v in zip(*sorted(zip(Final_Dimension2_list,Final_Dimension3_list,flatList)))]
    Final_Merge()
    table_Marks()          
# ------------------------------------------------------------------Torqueing--------------------------------------------------------------------------      
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
#----------------------------------------------------------------Class value--------------------------------------------------------------------------
def class_selected():
    global selected
    selected = var.get()
    
    if selected == "Select Type":
        Label(r, text = "Select Type").pack(pady=10)
    else:
        main_page()
#----------------------------------------------------------------Condition----------------------------------------------------------------------------
def condition():
    Captured_dir = os.listdir("Captured_images/Capture")
    
    
    if len(Captured_dir) == 0:
        Label1 = Label(second_frame, text = "Capture image first", bg = 'orange',font=("Arial", 25))
        Label1.grid(row = 6 , column = 5, sticky = 'W', padx = 10, pady = 0)
        Label1.after(3000, Label1.destroy)


    elif len(Captured_dir) == 1:    
        Label2 = Label(second_frame, text = "Capture both images", bg = 'orange',font=("Arial", 25))
        Label2.grid(row = 6 , column = 5, sticky = 'W', padx = 10, pady = 0)
        Label2.after(3000, Label2.destroy)


    else:
        choose()    
#----------------------------------------------------------------GUI Table----------------------------------------------------------------------------
def table_Marks():
    game_frame = Frame(second_frame)
        
    game_frame.grid(row=5, column = 3, sticky = 'W', padx = 10, pady = 10)

    my_game = ttk.Treeview(game_frame, show = 'headings', height=10)
          
    verscrlbar = ttk.Scrollbar(game_frame, orient ="vertical", command = my_game.yview)
    
    # Calling pack method w.r.to vertical
    # scrollbar
    verscrlbar.pack(side ='right', fill ='x')
    
    # Configuring treeview
    my_game.configure(xscrollcommand = verscrlbar.set)   
    my_game.pack() 

    my_game['columns'] = ('S_No', 'Center_ID', 'Reference1', 'Reference3', 'Approval_state')

    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("S_No",anchor=CENTER,width=40)
    my_game.column("Center_ID",anchor=CENTER,width=40)
    my_game.column("Reference1",anchor=CENTER,width=130)
    #my_game.column("Reference2",anchor=CENTER,width=130)
    my_game.column("Reference3",anchor=CENTER,width=150)
    my_game.column("Approval_state",anchor=CENTER,width=70)

    #Create Headings 
    my_game.heading("#0",text="",anchor=CENTER)
    my_game.heading("S_No",text="ID",anchor=CENTER)
    my_game.heading("Center_ID",text="ID",anchor=CENTER)
    my_game.heading("Reference1",text="Position X",anchor=CENTER)
    #my_game.heading("Reference2",text="Horizontal_Reference2",anchor=CENTER)
    my_game.heading("Reference3",text="Position Y",anchor=CENTER)
    my_game.heading("Approval_state",text="Approval",anchor=CENTER)
    print(flatList)
    
    Final_dim = []
    for i in range(len(Final_Dimension2_list)):
        if Final_Dimension2_list[i] <= 35:
            Final = Final_Dimension2_list[i] #- 0.5
            Final_dim.append(Final)
            
        else:
            Final_dim.append(Final_Dimension2_list[i])

    for i in range(len(flatList)):
        my_game.insert(parent='',index='end',iid=i,text='',
        values=(i+1, flatList[i],Final_dim[i],Final_Dimension3_list[i], 'Yes'))
        print(flatList[i],Final_dim[i],Final_Dimension3_list[i])

    my_game.pack() 
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
#--------------------------------------------------------------------Excel----------------------------------------------------------------------------
def excel():
    global Final, excel_frame, tree, Final1
    
    data= pd.read_csv(str(csv_path)+".csv")
    
    if selected == "Marking":
        Name_Count = data.query('Name=="Point"')
        Sort = Name_Count.sort_values(by='Position X')
    else:
        Name_Count = data.query('Name=="Circle"')
        Sort = Name_Count.sort_values(by='Center X')
    Sort.insert(0, 'ID', range(1, 1 + len(Sort)))
    Final1 = Sort.drop(['Count', 'Length',], axis=1)
    

    excel_frame = Frame(second_frame)
    excel_frame.grid(row=4, column = 3, padx = 10, pady = 10)
    # Create a Treeview widget
    tree = ttk.Treeview(excel_frame)
    
    open_file()
def open_file():
    clear_treeview()

    # Add new data in Treeview widget
    tree["column"] = list(Final1.columns)
    tree["show"] = "headings"

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = Final1.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)

    tree.pack() 
def clear_treeview():
   tree.delete(*tree.get_children())
#----------------------------------------------------------------Start with---------------------------------------------------------------------------
initial()
Arduino()
GUI()







