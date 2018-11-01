#NOTE this code can creat problem if line angle is in range so make a time after which
#the code will watch that
#so if we r getting an order we will have to use that one for some time then th
import cv2
import numpy as np
import math
import time
t1=time.time()
t=0
cap = cv2.VideoCapture(0)
w1 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  #Obtain video dimension x
h1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
w=int(w1)
h=int(h1)
roiWid = w1
roiHig = h1
roiX = 0
roiY = int(h1/2)-220
#print(roiWid,roiHig,roiX,roiY)
def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
    theta1 = math.atan(m)                  #calculate the slope angle
    return theta1*(180/np.pi)
def dis(m1,c1,m2,c2):
    global w,h
    X=float(c2-c1)/float(m1-m2)
    Y=(float(m1*c2)-float(m2*c1))/float(m1-m2)
    X=int(X)
    Y=int(Y)
    l=((X-(w/2))**2+(Y-(h/2))**2)**(0.5)
    return(l)
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
flag, flag_stay = True, False
while flag:

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([20,100,100],dtype=np.uint8)
    upper_blue = np.array([60,255,255],dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    #image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #img = cv2.drawContours(edges, contours, -1, (0,255,0), 3)
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    frameClone=frame.copy()
    #decide this time by experiment for initial gain of track
    v=0
    if time.time()<t1+3:
        if type(lines)==np.ndarray:
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(frameClone,(x1,y1),(x2,y2),(0,255,0),20)
                #print('0000naaaaaaa')
                if (round(x2-x1)!=0):
                    arctan = slope(x1,x2,y1,y2)
                    print(arctan)
                    #discuss and show the way by which angle of line is analysed to SAGAR 
                    if 85<=abs(arctan)<=95:
                        # NOTE-WE CAN BREAK FROM HERE BCZ WE GOT THE LINES.
                        #the commands for the pitch will be given here(angle dependent)
                       # print("it's straight")
                        #after the roll is given and track is straight calculate the distance of yellow line from centre and give tolerance
                        if abs((w*0.5)-x1)>3:
                            print('bhaii roll dede')
                            #hence yaw is given accordingly
                            #now the detected path is right go on path and hence use the pitch command
                        else:
                            print('no yaw plzz,pitch plzz')
                            #yaw is 0.
                            v=5
                            flag = False
                    else:
                        print('bhaii yaw dede')
                        #use the code to give rolling bcz the line has to get almost straight
        else:
            print('give pitch')
            #After u think that sufficient pitch is given and yellow line is not
            #detected move the drone left and right
            k1=0
            k2=0
            #CHOOSE a random number for d1 and d2
            if type(lines)!=np.ndarray and k1<5:
                print('move left')
                k1=k1+1
            if type(lines)!=np.ndarray and k2<10:
                print('move right')
                k2=k2+1
            #now below use elif if for generating the code for line loss
    elif time.time()>t1+3:
        if type(lines)==np.ndarray:
            for x1,y1,x2,y2 in lines[0]:
                arctan = slope(x1,x2,y1,y2)
                #choose a nice range to select only 1 principle line
                if 60<=abs(arctan)<=90:
                    if 60<=abs(arctan)<=84:
                        #check the positive and negative values of arctan for direction of rotation
                        print('bhaii gol ghuma')
                    #we r not using the else for this if bcz we have to focus 
                    if 85<=abs(arctan)<=90:
                        # print("it's straight")
                         if abs(w-x1)>3:
                             print('bhaii side ko ghuma dede')
                         else:
                             #now u have straight line and right under the drone so detect perpendicular lines if not get pitch
                             #if yes sleep
                             for i in lines:
                                for x1,y1,x2,y2 in i:
                                    if (round(x2-x1)!=0):
                                        arctan = slope(x1,x2,y1,y2)
                                        m1=float(y2-y1)/float(x2-x1)
                                        c1=float(y1)-m1*float(x1)
                                        for j in lines:
                                            for x3,y3,x4,y4 in j:
                                                if (round(x4-x3)!=0):
                                                    arctan1 = slope(x3,x4,y3,y4)
                                                    m2=float(y4-y3)/float(x4-x3)
                                                    c2=float(y4)-m2*float(x4)
                                                    #CHOOSE a range for perpendicular line
                                                    if 85<abs(arctan1-arctan)<90:
                                                        #print('bhaii perpendicular lines')
                                                        l=dis(m1,c1,m2,c2)
                                                        #need to give pitch
                                                        #check here the l size according the conditions
                                                        if l<15:
                                                            #make it stop and count t
                                                            t=t+1
                                                            if t==5:
                                                                #t should be 5 not 4
                                                                print('turn in such a way that camera is balanced')
                                                                #sleep here too bcz needs to give pitch also time duration may be fine
                                                                #t=t+1 is needed otherwise the drone will rotate
                                                                t=t+1
                                                            if t<5 or 6<t<11:
                                                                print('bhaii soza jara')
                                                                #watch if any else condition needs to keep
                                                                #take photos
                                                            if t==11:
                                                                #print('land')
                                                                #detect a square and stop the flying
                                                                #it will go above and then pitch will be given
                                                                d4=0
                                                                if shape(cap)!=1:
                                                                    print('give pitch')
                                                                    d4=d4+1
                                                                else:
                                                                    print('land kar ja')
                                                                    flag = False
                                                        else:
                                                            print('give pitch')
                                                    else:
                                                        print('give pitch')
        else:
            d1=0
            d2=0
            #CHOOSE a random number for d1 and d2
            if type(lines)!=np.ndarray and d1<5:
                print('move left')
                d1=d1+1
            if type(lines)!=np.ndarray and d1<10:
                print('move right')
                d2=d2+1
                
            
                    
if type(lines)==np.ndarray and time.time()<t1+3:
        for x1,y1,x2,y2 in lines[0]:
            arctan = slope(x1,x2,y1,y2)
            #choose a nice range to select only 1 principle line
            if 60<=abs(arctan)<=90:
                if 60<=abs(arctan)<=84:
                    #check the positive and negative values of arctan for direction of rotation
                    print('bhaii yaw')
                #we r not using the else for this if bcz we have to focus 
                if 85<=abs(arctan)<=90:
                    # print("it's straight")
                     if abs((w*0.5)-x1)>3:
                         print('bhaii roll dede')
                     else:
                         #now u have straight line and right under the drone so detect perpendicular lines if not get pitch
                         #if yes sleep
                         for i in lines:
                            for x1,y1,x2,y2 in i:
                                if (round(x2-x1)!=0):
                                    arctan = slope(x1,x2,y1,y2)
                                    m1=float(y2-y1)/float(x2-x1)
                                    c1=float(y1)-m1*float(x1)
                                    for j in lines:
                                        for x3,y3,x4,y4 in j:
                                            if (round(x4-x3)!=0):
                                                arctan1 = slope(x3,x4,y3,y4)
                                                m2=float(y4-y3)/float(x4-x3)
                                                c2=float(y4)-m2*float(x4)
                                                #CHOOSE a range for perpendicular line
                                                if 85<abs(arctan1-arctan)<90:
                                                    #print('bhaii perpendicular lines')
                                                    l=dis(m1,c1,m2,c2)
                                                    #need to give pitch
                                                    #check here the l size according the conditions
                                                    if l<15 and flag_stay:
                                                        #make it stop and count t
                                                        t=t+1
                                                        if t==5:
                                                            #t should be 5 not 4
                                                            print('turn in such a way that camera is balanced')
                                                            #sleep here too bcz needs to give pitch also time duration may be fine
                                                            #t=t+1 is needed otherwise the drone will rotate
                                                            t=t+1
                                                        if t<5 or 6<t<11:
                                                            print('bhaii soza jara')
                                                            #watch if any else condition needs to keep
                                                            #take photos
                                                            #SO 
                                                        if t==11:
                                                            #print('land')
                                                                #detect a square and stop the flying
                                                                #it will go above and then pitch will be given
                                                                d4=0
                                                                if shape(cap)!=1:
                                                                    print('give pitch')
                                                                    d4=d4+1
                                                                else:
                                                                    print('land kar ja')
                                                    else:
                                                        print('give pitch')
                                                else:
                                                    print('give pitch')
else:
        d1=0
        d2=0
        #CHOOSE a random number for d1 and d2
        if type(lines)!=np.ndarray and d1<5:
            print('move left')
            d1=d1+1
        if type(lines)!=np.ndarray and d1<10:
            print('move right')
            d2=d2+1
                    
                                                   
                        

        
#After break condition use the above copy paste part  
