import numpy as np
import cv2
from copy import deepcopy

img = cv2.imread('sag.jpg')
orig=deepcopy(img)
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
b=1
for cnt in contours:
    
    area = cv2.contourArea(cnt)
    
    if 1500 < area < 90000:

        (x,y,w,h) = cv2.boundingRect(cnt)
        #print 'sides-',x,y,w,h
     #   cv2.rectangle(gray,(x,y),(x+w,y+h),255,-1)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),0)
        #SAGGREGATING DIFFERENT IMAGES OF WHITE REGION FROM PIC 
        k=img[y:y+h,x:x+w]
        #ADD THE NEXT CODE HERE AS WHITE REGION IN PIC IS OBTAINED
        cv2.imshow(str(b),k)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        cv2.drawContours(img,[cnt],0,(0,200,200),2)
        b=b+1
        #print 'contour-',contours
        
cv2.imshow('original',orig)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
