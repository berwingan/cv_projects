import cv2
import time 
import numpy as np 
import HandTrackingModule as htm
import math

cap = cv2.VideoCapture(0)
wCam , hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

pTime=0
detector = htm.handDetector(detectionCon=0.8)


while True:
    success, img = cap.read()
    img  = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        x1, y1 = lmList[4][1],lmList[4][2]#thumb
        x2, y2 = lmList[8][1],lmList[8][2]#index finger
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1,y1), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img, (cx,cy), 15, (255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)# use something like pycaw to control the volume but for mac
        print(length)
        #20 - 200 -----min and max of the buttons 
        if length<25:
            cv2.circle(img, (cx,cy), 15, (0,255,0),cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


    cv2.imshow("Img",img)
    cv2.waitKey(1)
