import cv2
import numpy as np
import Hand_Tracking_Module as htm
import time
import pyautogui as ap

#1. Find hand Landmarks
#2. Get the tip of the index and middle fingers
#3. Check which fingers are up
#4. Only Index Finger : Moving Mode
#5. Convert Coordinates (640,480) to screen size
#6. Smoothen Values# to prevent flickering
#7. Move Mouse
#8. Both Index and middle fingers are up : Clicking Mode
#9. Find distance between fingers
#10. Click mouse if distance short .
ap.FAILSAFE=False
wScr,hScr=ap.size()
frameR = 100 # Frame Reduction
print(wScr,hScr)
wCam, hCam = 640, 480
pTime=0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 2
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector=htm.handDetector(maxHands=1)
while True:
  success, img = cap.read()
  img=detector.findHands(img)
  lmList,bbox=detector.findPosition(img) 
  cv2.rectangle(img, (frameR+30, frameR), (wCam-frameR-30, hCam-frameR-75),
(255, 0, 255), 2) 
  if len(lmList) != 0:
   x1, y1 = lmList[8][1:]  #thumb
   x2, y2 = lmList[12][1:]  #index
   #print(x1,y1,x2,y2)
   fingers=detector.fingersUp()
   #print(fingers)
   if fingers[1]==1 and fingers[2]==0:  #moving mode

    x3=np.interp(x1,(frameR+30,wCam-frameR-30),(0,wScr))    #converted coordinates
    y3=np.interp(y1,(frameR,hCam-frameR-75),(0,hScr))
    clocX = plocX + (x3-plocX) / smoothening
    clocY = plocY + (y3-plocY) / smoothening
    ap.moveTo(wScr-clocX, clocY, duration=0)  # move mouse to XY coordinates over num_second seconds
    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    plocX, plocY = clocX, clocY
   if fingers[1]==1 and fingers[2]==1:  #clicking mode
     length,img,lineInfo=detector.findDistance(8,12,img)
    #  print(length)
     if length < 40:
      cv2.circle(img, (lineInfo[4], lineInfo[5]),
      15, (0, 255, 0), cv2.FILLED)
      ap.click()
      
  cTime=time.time()
  fps=1/(cTime-pTime)
  pTime=cTime
  cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2,
              (255, 0, 0), 3)
  cv2.imshow('Frame',img)
  if cv2.waitKey(1) & 0xFF == ord('d'):
      break