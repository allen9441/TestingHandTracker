import cv2
import numpy as np
import handmodule as hm
import time
import autopy
from autopy.mouse import Button


click = 0
wCam, hCam = 640, 480
frameR = 150
smoothening = 5
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(3)
cap.set(3, wCam)
cap.set(4, hCam)
detector = hm.handDetector()
wScr, hScr = autopy.screen.size()

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)
        if wCam - frameR >= 0 and hCam - frameR >= 0:
            if fingers[1] == 1:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

                if fingers[2] == 1:
                    length, img, lineInfo = detector.findDistance(8, 12, img)
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 7, (0, 255, 0), cv2.FILLED)
                        if click == 0:
                            click = 1
                            autopy.mouse.toggle(None, True)
                    if length >= 40 and click == 1:
                        autopy.mouse.toggle(None, False)
                        click = 0

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 2)

    cv2.imshow("haha just camera", img)
    cv2.waitKey(1)