import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('barcode3.jpg')
image=img
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,img=cv2.threshold(gray,180,255,0)
kernel = np.ones((5,5),np.uint8)
img = cv2.dilate(img,kernel,iterations =1)

corners = cv2.goodFeaturesToTrack(img,250,0.01,10)
corners = np.int0(corners)

'''cv2.imshow('img',img)
cv2.imshow('2',dilation)
cv2.imshow('original',image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
#print corners
cor = []

'''for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)'''
x,y = corners[0].ravel()
print'yo',x,y
quad = [(x,y)]*4
for i in corners:
    x, y = i.ravel()
    if x+y < quad[0][0] + quad[0][1]:
        quad[0] = (x,y)
        cor += [(x,y)]
    if y-x < quad[1][1] -quad[1][0]:
        quad[1] = (x,y)
        cor += [(x,y)]
    if x-y < quad[2][0] -quad[2][1]:
        quad[2] = (x,y)
        cor += [(x,y)]
    if -x-y < -quad[3][0] -quad[3][1]:
        quad[3] = (x,y)
        cor += [(x,y)]
        
s=[quad[0],quad[1],quad[2],quad[3]]
'''cor.remove(quad[0])
cor.remove(quad[1])
corners=corners-cor'''
'''#print corners
for i in s:
    x,y = i
    cv2.circle(img,(x,y),13,255,-1)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#plt.imshow(img),plt.show()
'''
img=255-img
x1,y1=quad[0][0]-12,quad[0][1]-12
x2,y2=quad[1][0]+12,quad[1][1]-12
x3,y3=quad[2][0]-12,quad[2][1]+12
x4,y4=quad[1][0]+12,quad[3][1]+12
pts = np.array([[x1,y1],[x2,y2],[x4,y4],[x3,y3]], np.int32)
pts = pts.reshape((-1,1,2))
#check the thickness of ploygon
img = cv2.polylines(img,[pts],True,(0,255,255),20)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
