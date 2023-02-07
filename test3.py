# importing the modules
import cv2
import numpy as np

# set Width and Height of output Screen
frameWidth = 1280
frameHeight = 720

# capturing Video from Webcam
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# set brightness, id is 10 and
# value can be changed accordingly
cap.set(10, 150)

# object color values
myColors = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]

# color values which will be used to paint
# values needs to be in BGR
myColorValues = [[51, 153, 255],
                 [255, 0, 255],
                 [0, 255, 0],
                 [255, 0, 0]]

# [x , y , colorId ]
myPoints = []


# function to pick color of object
def findColor(img, myColors, myColorValues):
    # converting the image to HSV format
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    # running for loop to work with all colors
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)

        # making the circles
        cv2.circle(imgResult, (x, y), 15,
                   myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints


# contouyrs function used to improve accuracy of paint
def getContours(img):
    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0

    # working with contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


# draws your action on virtual canvas
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]),
                   10, myColorValues[point[2]], cv2.FILLED)


# running infinite while loop so that
# program keep running untill we close it
while True:
    success, img = cap.read()
    imgResult = img.copy()

    # finding the colors for the points
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        # drawing the points
        drawOnCanvas(myPoints, myColorValues)

    # displaying output on Screen
    cv2.imshow("Result", imgResult)

    # condition to break programs execution
    # press q to stop the execution of program
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break










##########################################################################
"""import cv2
import numpy as np
import time
import os
import handtracking as htm

brushThickness = 15
eraserThickness = 100

folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.5)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which finger are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. If Selection Mode - two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            # Checking for the click
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode = Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    img = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header  # header which is containing ths image is called over here.
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)"""