import cv2
import time 
import numpy as np 
import HandTrackingModule as htm
import math
import osascript

cap = cv2.VideoCapture(0)
wCam , hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

pTime=0
detector = htm.handDetector(detectionCon=0.8)

frame = 0
volBar = 400
volPer = 0
while True:
    frame +=1 

    success, img = cap.read()
    img  = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    instuc = "set volume output volume "
    if len(lmList)!=0:
        x1, y1 = lmList[4][1],lmList[4][2]#thumb
        x2, y2 = lmList[8][1],lmList[8][2]#index finger
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1,y1), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img, (cx,cy), 15, (255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)# use something like pycaw to control the volume but for mac
        #print(length)
        minVol = 0
        maxVol = 100
        vol = np.interp(length,[25,200],[minVol,maxVol])
        volBar = np.interp(length,[25,200],[400,150])
        volPer = np.interp(length,[25,200],[0,100])
        instuc+= str(vol)
        

        #20 - 200 -----min and max of the range to 
        if length < 25:
            cv2.circle(img, (cx,cy), 15, (0,255,0),cv2.FILLED)
    #display the volume here         
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)


    if (frame%20==0 and len(lmList)!=0):#costly to change volumen
        frame = 0
        osascript.osascript(instuc)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.putText(img, str(int(volPer)), (48,458),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


    cv2.imshow("Img",img)
    cv2.waitKey(1)
