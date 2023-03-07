import os
import subprocess
import cv2
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


Image_path = 'images/F2.jpg'

try:
    os.mkdir("Delete")
except:
    print("")


#------------------------------- YOLO ----------------------------

subprocess.run(f"python detect.py --weights {'best.pt'} --source {Image_path} --img {'512'} --iou {'0.1'}  --conf {'0.5'}")


#------------------------------- Coordinates cropping ----------------------------

img = cv2.imread(Image_path)
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
cv2.imwrite("Delete/thres.jpg", dst1)
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
k = 1
for i in contours:
    M = cv2.moments(i)
    if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(image_final, [i], -1, (0, 255, 0), 1)
            cv2.circle(image_final, (cx, cy), 1, (0, 0, 255), -1)
            cv2.putText(img, "center", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
    #Dict['c',i+1] = [cx,cy]
    Centers.append('c'+ str(k))
    coordinates.append([cx, cy])
    k += 1
cv2.imwrite("Delete/image.png", image_final)

index_value = coordinates.index([2303,1643])
if [2303,1643] in coordinates:
    del Centers[index_value]
    del coordinates[index_value]
else:
    print("Nothing to delete")

for i in range(len(Centers)):
    Dict[Centers[i]] = coordinates[i]


Reference_line = input("Give Reference line input towards curved portion: ")

for i in range(len(Centers)):
    Distance_pixels = int(Reference_line) - int(coordinates[i][1])
    Final_Dimension = int(Distance_pixels)/int(53)
    print("Distance from reference: \n", Centers[i], ":",  Final_Dimension)

cv2.imwrite("images/Final.jpg", img) 


