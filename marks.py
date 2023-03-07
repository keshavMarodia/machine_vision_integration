import subprocess
import cv2
import numpy as np
from tkinter import *
from tkinter import *
from control_page import *


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