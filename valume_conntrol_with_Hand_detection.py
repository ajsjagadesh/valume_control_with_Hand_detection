from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cv2
import os


cap = cv2.VideoCapture(0,700)

detector = HandDetector(detectionCon=0.75, maxHands=2)


while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img) 

    if hands:
        fingers1 = detector.fingersUp(hands[0])
        length, info, img = detector.findDistance(hands[0]['lmList'][4], hands[0]['lmList'][8], img)
        p0 = np.array(hands[0]['lmList'][4])
        p2 = np.array(hands[0]['lmList'][8])
        sum_sq = np.sum(np.square(p0-p2))
        dist=int(np.sqrt(sum_sq))
        #print(dist)
        if dist>=50 & dist<=300:
            v = np.interp(dist, [50, 250], [100, 65535])
            st = 'nircmd.exe setsysvolume '+str(v)
            os.system(st)
            val = np.interp(dist, [50, 250], [0, 100])
            print(f'Volume : {int(val+0.5)}')
            #print(f'dist : {dist}')

        
    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()