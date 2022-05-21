import cv2
import mediapipe as mp
import time
import pyautogui as pgui
import sys
##################################
# HAND TRACKING FUNCTIONS:

class handFinder():
    def __init__(self,mode=False, maxHands=1,modelC=1,detectionCon = 0.7, trackCon = 0.7):
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

##########################################################

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    # print("reached here!")__________________________________________________________
    lmlist = handFinder().findPosition(img, draw=False)
    
    # print(lmlist) #printing landmarks ______________________________________________

    if len(lmlist) != 0: # If hand is present in the frame

        if lmlist[20][1] > lmlist[4][1]:  # If Right-Hand is turned back, or left hand is used

            # To Stop the function
            if lmlist[12][2] > lmlist[10][2]:
                sys.exit("Neateye Goes!")

            # For Seeking the Video
            if lmlist[0][1] > lmlist[12][1]:  # Right swipe
                pgui.press("right")
                time.sleep(0.2)
            if lmlist[0][1] < lmlist[12][1]:  # Left swipe
                pgui.press("left")
                time.sleep(0.2)
            continue


        # Pause Function :
        if lmlist[12][2] > lmlist[10][2]:
            pgui.press('space')
            time.sleep(2)
            continue

        # For Volume control using arrow keys
        if lmlist[0][1] > lmlist[12][1]:  # Vol Up
            pgui.press("up")
            time.sleep(0.2)
        if lmlist[0][1] < lmlist[12][1]:  # Vol Down
            pgui.press("down")
            time.sleep(0.2)
        
