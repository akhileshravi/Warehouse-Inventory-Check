import cv2
import numpy as np
from copy import deepcopy
img=cv2.imread('mini.jpg')
im=deepcopy(img)
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#(IITM)SET THE THRESHOLD VALUE FOR YELLOW COLOR
lower_yellow=np.array([0,100,100])
upper_yellow=np.array([90,255,255])
mask=cv2.inRange(hsv,lower_yellow,upper_yellow)
res=cv2.bitwise_and(img,img,mask=mask)
image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
for cnt in contours:
    
    area = cv2.contourArea(cnt)
    
    if 3500<area<10000:
        print'True'
        
img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('img',img)
cv2.imshow('original',im)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
