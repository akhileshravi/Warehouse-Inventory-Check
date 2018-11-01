'''import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    minLineLength = 10
    maxLineGap = 1
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    if type(lines)==np.ndarray:
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),10)

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()'''




import cv2
import numpy as np

cap = cv2.VideoCapture('fieldtrial1.mp4')

while(1):

    # Take each frame
    _, frame = cap.read()

    #reducing frame dimensions (region of interest)
    frame=frame[300:600, 0:]
    #Using Gaussian blur
    image=cv2.GaussianBlur(frame, (21,21),0)
    '''
    #using Median
    image=cv2.medianBlur(frame,15)'''
    #define range of white color in BGR
    lower = np.uint8([140, 145, 150])
    upper = np.uint8([255, 255,255])

    #applying erosion to remove stray points
    kernel= np.ones((5,5),np.uint8)
    img_erosion = cv2.erode(image, kernel, iterations=1)
    #Applying dilation to make the wanted points thicker
    dilation=cv2.dilate(img_erosion, kernel, iterations=1)
    
    #Applying mask in the image
    mask = cv2.inRange(dilation, lower,upper)

    #Canny edge detection used
    mask = cv2.Canny(mask,50,150)
    minLineLength = 5
    maxLineGap = 8
    lines = cv2.HoughLinesP(mask,1,np.pi/180,50,minLineLength,maxLineGap)
    if type(lines)==np.ndarray:
        print(lines)
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),40)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image,image, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
