import cv2
import numpy as np
def shape(cap):
    cap = cv2.VideoCapture(0)
    while(1):
        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,1)
        im,contours,h = cv2.findContours(thresh,1,2)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #print(len(approx))
            if len(approx)==4:
                return 1
cap=cv2.VideoCapture(0)
print(shape(cap))
         
