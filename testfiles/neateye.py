import cv2
import time
import numpy as np
import testfiles.HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui as pgui
##################
# Handling the fps
# frame_rate = 30
# prev = 0

##################
# initialisations
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
vol = 0
######################################


def givlen(a, b):  # give the tracking id of the points you want the length between
    x1, y1 = lmlist[a][1], lmlist[a][2]
    x2, y2 = lmlist[b][1], lmlist[b][2]
    length = math.hypot(x2 - x1, y2 - y1)
    return length
######################################


cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8)
while True:
    # For Pause and Volume gestures :

    # time_elapsed = time.time() - prev
    # if time_elapsed > 1./frame_rate:
    ret, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
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
        # Volume Function:
        vol = np.interp(vollen, [20, 180], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
