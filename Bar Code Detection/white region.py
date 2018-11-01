import cv2
import numpy as np

img = cv2.imread('barcode.jpg')
#img = cv2.resize(img,(400,500))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,gray = cv2.threshold(gray,180,255,0)
gray2 = gray.copy()

im,contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if 2000<cv2.contourArea(cnt)<90000:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(gray2,(x,y),(x+w,y+h),255,-1)
kernel = np.ones((5,5),np.uint8)
gray3 = cv2.morphologyEx(gray2, cv2.MORPH_OPEN, kernel)

cv2.imshow('IMG',gray3)
cv2.waitKey(0)
cv2.destroyAllWindows()
