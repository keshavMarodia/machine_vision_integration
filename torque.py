import subprocess
import cv2
import numpy as np

Reference_line1 = 2855
Reference_line2 = 317


def Final_Merge():
    IMG1 = cv2.imread(r"college-project\src\components\images\1.jpg")
    img1_rot = cv2.rotate(IMG1, cv2.ROTATE_90_CLOCKWISE)

    IMG2 = cv2.imread(r"college-project\src\components\images\2.jpg")
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
    cv2.imwrite(r"college-project\src\components\images\concat_Final.jpg", im_h1_rot)
    
    
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
            cv2.imwrite(r'college-project\src\components\images\1.jpg', array_created)
        else:
            cv2.imwrite(r'college-project\src\components\images\2.jpg', array_created)
    Final_Merge()