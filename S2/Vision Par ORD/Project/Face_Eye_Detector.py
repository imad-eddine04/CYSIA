import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #import model w n applikiwah ll face
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml') #import model w n applikiwah ll eyes
fullbody_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read() #keep capturing ylamin tdrok 3la 'q'

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # n7awllo l image ta3na ll noir et blanc psq model y detecti ghir noir et blanc images
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # nmedo lmodel gray image ta3na w 3la 7ssab doc ta3 openCV scaleFactor = 1.3 w minNeighbors = 5
    # scaleFactor : bah yla medinalah image size ta3ha (1000 x 1000) ydirlha shrink yssagherha 3la 7ssab data li t3alem 3liha
    # minNeighbors : ch7al distance bin test images li y9aren binathom

    for (x,y,w,h) in faces: #ydor 3la (x,y) w hight w width ta3 kol face li f dataset ta3 faces li f haarcascade model

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5) # y7ot rectangle 3la face li ydetectih fl image
        # rectangle li fih face ghadi nkhedmo bih bah ndetecto eyes
        roi_gray = gray[y:y+h,x:x+w] # n7awloha gris w ndiroha fl vriable roi_gray
        roi_color = frame[y:y+h,x:x+w] # n7awloha b les colors w ndiroha fl vriable roi_color

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5) # nafss chi bsh nkhedmo bl model zawj ta3 eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh),(0,255,0),5)

    cv2.imshow('frame',frame) # nb9aw n afficho fl frame ta3 image
    if cv2.waitKey(1) & 0xFF == ord('q'): #7ata n clickiw 3la 'q'
        break
cap.release() # bah ma yb9ach had code chad l camera w ykhaliha lkach app fl pc t3k kima obs ykhdem biha yla 7taj
cv2.destroyAllWindows() #ybella3 ga3 l windows li baynin