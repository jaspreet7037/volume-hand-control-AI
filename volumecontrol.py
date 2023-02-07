import cv2 # computer vision opencv module
import time # time library
import numpy as np # numpy library
import handtracking as htm # I used handtracking program and created it into module and used in this program.
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # PYTHON CORE AUDIO WINDOWS LIBRARY(PYCAW)

####################################
wCam, hCam = 1280, 720
####################################

cap = cv2.VideoCapture(1) # syntax to use camera as a main computer vision device
cap.set(3, wCam) # setting width of the frame for video
cap.set(4, hCam) # setting height of the frame for video
pTime = 0 # present time variable to calculate FPS.

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
 
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4],  lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 13, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # hand range 30 - 260
        #volume range -63.5 - 0.0

        vol = np.interp(length, [30, 260], [minVol, maxVol])
        volBar = np.interp(length, [30, 260], [400, 150])
        volPer = np.interp(length, [30, 260], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<30:
            cv2.circle(img, (cx, cy), 13, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))

    cv2.imshow("Img", img) # show your video using camera
    cv2.waitKey(1) # using default camera as 1.