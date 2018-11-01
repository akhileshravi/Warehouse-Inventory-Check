import cv2
import numpy as np
from pyzbar.pyzbar import decode
from copy import deepcopy
from matplotlib import pyplot as plt



c = 25
bars= []

img = cv2.imread('C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_\'18\\Bar \
Codes\\b0021.jpg')

orimg = deepcopy(img)
gray0 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret1 ,gray = cv2.threshold(gray0,180,255,0)

kernel = np.ones((5,5),np.uint8)

##gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
##gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

a = []


for cnt in contours:
    
    area = cv2.contourArea(cnt)
    
    if 1500 < area < 90000:

        (x,y,w,h) = cv2.boundingRect(cnt)
     #   cv2.rectangle(gray,(x,y),(x+w,y+h),255,-1)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),0)
        cv2.drawContours(img,[cnt],0,(0,200,200),2)
        
        white_roi = deepcopy(orimg[y:y+h, x:x+w])
        gray_1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


        gray_xx = 255 - gray_1
        stencil = np.zeros(gray_xx.shape).astype(gray_xx.dtype)
        color = [255, 255, 255]
        cv2.fillPoly(stencil, cnt, color)
        result = cv2.bitwise_and(gray_xx, stencil)
        result = 255 - result


        
        gray_roi_1 = cv2.dilate((255 - result),kernel,iterations = 2)
        gray_roi_1 = 255 - gray_roi_1
        
        ret2, gray_roi_2 = cv2.threshold(gray_roi_1,180,255,0)
        
        gray_roi_2 = 255 - gray_roi_2
        gray_roi_2 = cv2.morphologyEx(gray_roi_2, cv2.MORPH_OPEN, kernel)
        gray_roi_2 = cv2.morphologyEx(gray_roi_2, cv2.MORPH_CLOSE, kernel)
        gray_roi_2 = cv2.dilate(gray_roi_2,kernel,iterations = 2)

        height, width = white_roi.shape[:2]
##        bars.extend( decode((white_roi[:, :, 0].astype('uint8').tobytes(), width, height)) )
##        print decode((white_roi[:, :, 0].astype('uint8').tobytes(), width, height))

        cv2.imshow('White ROI',white_roi)
        cv2.imshow('gray_roi_2',gray_roi_2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        black_contours, black_heir = cv2.findContours(gray_roi_2,
                                        cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        for blk_cnt in black_contours:
    
            if area/10 < cv2.contourArea(blk_cnt) < area:
                
                (bx,by,bw,bh) = cv2.boundingRect(blk_cnt)
##                cv2.rectangle(gray_roi_2,(x,y),(x+w,y+h),255,-1)
                cv2.rectangle(img,(bx,by),(bx+bw,by+bh),(200,200,0),0)
                cv2.drawContours(img,[cnt],0,(0,255,0),2)
                roi = orimg[by:by+bh, bx:bx+bw]
                if a == []:
                    a = deepcopy(roi)
                cv2.imshow('ROI',roi)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                height, width = roi.shape[:2]
                # 8 bpp by considering just the blue channel
                cv2.imwrite(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Bar Codes\Imwrite\\B0"+str(c)+".jpg",roi)
                bars.extend( decode((roi[:, :, 0].astype('uint8').tobytes(), width, height)) )
                print decode((roi[:, :, 0].astype('uint8').tobytes(), width, height))
                #cv2.drawContours(mask,[cnt],0,255,-1)
                c += 1
'''
print  "c =",c,"\n\n"
im, im1 = deepcopy(gray2), deepcopy(gray2)

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(im1,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(im,(x,y),3,255,-1)
print len(corners)
plt.imshow(im),plt.show()


x,y = corners[0].ravel()
quad = [(x,y)]*4
#quad = [topleft, topright, bottomleft, bottomright]
cor = []
for i in corners:
    x, y = i.ravel()
    if x+y < quad[0][0] + quad[0][1]:
        quad[0] = (x,y)
    if y-x < quad[1][1] -quad[1][0]:
        quad[1] = (x,y)
    cor += [(x,y)]

cor.remove(quad[0])
cor.remove(quad[1])

m = (float(quad[1][1]-quad[0][1])/(quad[1][0]-quad[0][0]))
#m = (y2-y1)/(x2-x1)
c = quad[0][1] - m*quad[0][0]
#c = y1 - m*x1

for i in cor:
    x,y = i
    if y - 3 < (m*x + c) < y + 3:
        cor.remove(i)

    
quad[2] = quad[3] = cor[0]
for i in cor:
    x, y = i
    if x < quad[2][0]:
        quad[2] = (x,y)
    elif x > quad[3][0]:
        quad[3] = (x,y)
    
'''
##cv2.imshow('IMG',gray2)
##cv2.imwrite(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Bar Codes\Imwrite\\B01730.jpg",gray2)
cv2.imshow('orig',img)

#cv2.imshow('IMG2',opening)
cv2.waitKey(0)  
cv2.destroyAllWindows()
print bars
