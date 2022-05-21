import cv2
import mediapipe as mp
import time
import pyautogui as pgui
import numpy as np
import math
##################################
# HAND TRACKING FUNCTIONS:


class handFinder():
    def __init__(self,mode=False, maxHands=2,modelC=1,detectionCon = 0.5, trackCon = 0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelC,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPosition(self,img, handNo=0, draw = True):

        lmlist= []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (10,255,10), cv2.FILLED)

        return lmlist

#################################################

def givlen(a, b):  # give the tracking id of the points you want the length between
    x1, y1 = lmlist[a][1], lmlist[a][2]
    x2, y2 = lmlist[b][1], lmlist[b][2]
    length = math.hypot(x2 - x1, y2 - y1)
    return length
######################################

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    # print("reached here!")__________________________________________________________
    lmlist = handFinder().findPosition(img, draw=False)
    
    print(lmlist) #printing landmarks ______________________________________________

    if len(lmlist) != 0:
        # For Seeking the Video
        if lmlist[20][1] > lmlist[4][1]:  # If Right-Hand is turned back, or left hand is used
            if lmlist[0][1] > lmlist[12][1]:  # Right swipe
                pgui.press("right")
                time.sleep(0.5)
            if lmlist[0][1] < lmlist[12][1]:  # Left swipe
                pgui.press("left")
                time.sleep(0.5)
            continue
        vollen = givlen(a=4, b=8)
        spacelen = givlen(a=4, b=12)
        # Pause Function :
        if lmlist[12][2] > lmlist[10][2]:
            pgui.press('space')
            time.sleep(2)
            continue
