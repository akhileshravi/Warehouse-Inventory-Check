import cv2
import numpy as np
from pyzbar.pyzbar import decode

img = cv2.imread('C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_\'18\\Bar Codes\\b0009.jpg')
#img = cv2.resize(img,(400,500))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,gray = cv2.threshold(gray,180,255,0)
gray2 = gray.copy()
kernel = np.ones((5,5),np.uint8)
gray2 = cv2.morphologyEx(gray2, cv2.MORPH_OPEN, kernel)
gray2 = cv2.morphologyEx(gray2, cv2.MORPH_CLOSE, kernel)

c = 1
bars= []
contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if 2000<cv2.contourArea(cnt)<90000:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(gray2,(x,y),(x+w,y+h),255,-1)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),0)
        cv2.drawContours(img,[cnt],0,(0,255,0),2)
        roi = img[x:x+w, y:y+h]
        height, width = roi.shape[:2]
	# 8 bpp by considering just the blue channel
        cv2.imwrite(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Bar Codes\Imwrite\\B0"+str(c)+".jpg",roi)
        #bars.extend( decode((roi[:, :, 0].astype('uint8').tobytes(), width, height)) )
        #cv2.drawContours(mask,[cnt],0,255,-1)
        c += 1




cv2.imshow('IMG',gray2)
cv2.imshow('orig',img)
#cv2.imshow('IMG2',opening)
cv2.waitKey(0)  
cv2.destroyAllWindows()
