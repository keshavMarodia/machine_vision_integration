from unittest import main
import cv2
from PIL import Image
from PIL import Image
from tkinter import *
from re import L
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image   
from pypylon import pylon
from tkinter.filedialog import asksaveasfilename, askopenfilename
import pandas as pd
# from marks import *
from origin import *


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