import numpy as np
import cv2
eye_cascade=cv2.CascadeClassifier('myhaar.xml')
img=cv2.imread('b0449.bmp')
img=cv2.resize(img,(400,400))
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
eyes = eye_cascade.detectMultiScale(gray)
for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
