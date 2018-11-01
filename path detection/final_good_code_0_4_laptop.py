#NOTE this code can creat problem if line angle is in range so make a time after which
#the code will watch that
#so if we r getting an order we will have to use that one for some time then th

##from picamera.array import PiRGBArray
##from picamera import PiCamera
import cv2
import numpy as np
import math
import time
from copy import deepcopy

t=0
w1, h1 = 640, 480
##camera = PiCamera()
##camera.awb_mode = "tungsten"
##camera.resolution = (w1, h1)
##camera.zoom = (0.7, 0.7, 1, 1)
##camera.framerate = 32
##rawCapture = PiRGBArray(camera, size=(640, 480))

cap = cv2.VideoCapture(0)
w1 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  #Obtain video dimension x
h1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
w=int(w1)
h=int(h1)
roiWid = w1
roiHig = h1
roiX = 0
roiY = int(h1/2)-220


#####Functions#####

def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    if vx1 == vx2:
        return 90
    else:
        m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
        theta1 = math.atan(m)                  #calculate the slope angle
        return theta1*(180/np.pi)


def dis(m1,c1,m2,c2):
    ''' Distance from centre of the intersection of two lines'''
    
    global w,h
    
    X=float(c2-c1)/float(m1-m2)
    Y=(float(m1*c2)-float(m2*c1))/float(m1-m2)
    X=int(X)
    Y=int(Y)
    
    l=((X-(w/2))**2+(Y-(h/2))**2)**(0.5)
    
    return(l)


def shape(frame):
    
    ''' Checking for a square in each frame '''
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert BGR to HSV
    ret,thresh = cv2.threshold(gray,127,255,1)
    im,contours,h = cv2.findContours(thresh,1,2)
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            if cv.PointPolygonTest(cnt, (240, 320), measureDist = False) > 0:
                return True
    return False


def find_lines(frame):
    
    ''' Finds the yellow lines in the frame '''
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([20,100,100],dtype=np.uint8)
    upper_blue = np.array([60,255,255],dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    kernel = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(edges,kernel,iterations = 2)
    
    minLineLength = 10
    maxLineGap = 15

    lines = np.ndarray([0,0,0])
    lines1 = cv2.HoughLinesP(dilation,1,np.pi/180,100,minLineLength,maxLineGap)
    lines2 = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    
    if type(lines1) == np.ndarray:
        if type(lines2) == np.ndarray:
            temp_lines = [i for i in lines1] + [j for j in lines2]
            lines = np.array(temp_lines)
            
        else:
            lines = deepcopy(lines1)
            
    elif type(lines2) == np.ndarray:
        lines = deepcopy(lines2)
        
    else:
        #lines = np.ndarray(shape = [0,0,0])
        lines = None
    
    return lines


def length_line(x1, y1, x2, y2):
    return ( (x2 - x1)**2 + (y2 - y1)**2 )**0.5

def longest_line(lines):
    
    longest = lines[0]
    for x1, y1, x2, y2 in lines[0]:
        longest = (x1, y1, x2, y2)
    long_length = length_line(x1, y1, x2, y2)
    orig_slope = abs(slope(x1, y1, x2, y2))
    
    for i in lines:
        for x1, y1, x2, y2 in i:
            if orig_slope: 
                if abs(slope(x1, y1, x2, y2)) > 45 and orig_slope <= 45:
                    longest = (x1, y1, x2, y2)
                    long_length = length_line(x1, y1, x2, y2)
                    orig_slope = False
                    
            if length_line(x1, y1, x2, y2) > long_length and 45 < abs(slope(x1,x2,y1,y2)) <= 90:
                longest = (x1, y1, x2, y2)
                long_length = length_line(x1, y1, x2, y2)
    
    for x1, y1, x2, y2 in lines[0]:
        longest = (x1, y1, x2, y2)
    if abs(slope(x1, y1, x2, y2)) > 45:
        return (x1, y1, x2, y2)
    else:
        for i in lines:
            for x1, y1, x2, y2 in i:
                if length_line(x1, y1, x2, y2) > long_length:
                    longest = (x1, y1, x2, y2)
                    long_length = length_line(x1, y1, x2, y2)
        return (x1, y1, x2, y2)

##### Flag Initiations #####

flag_stay = False
left_flag = right_flag = False
front_flag = True
position = 0
first_line_found = False
line_end_flag = False
perpendicular_found = False
outside_plus_flag = True

##### Limit Definitions #####
radius_limit = 50
roll_limit = 20

### Main While Loop ###


while True:

##for imgfrm in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # Take each frame
    _, frame = cap.read()
##    frame = imgfrm.array 

    #Find all the yellow lines
    lines = find_lines(frame)

    frameClone=frame.copy()
    

    if not first_line_found:
        #Finding the yellow line in the beginning
        
        if type(lines)==np.ndarray:
            
            left_flag = right_flag = False
            front_flag = True
            position = 0

            for x1,y1,x2,y2 in lines[0]:
                longest = (x1, y1, x2, y2)
            long_length = length_line(x1, y1, x2, y2)
            
            for i in lines:
                for x1, y1, x2, y2 in i:
                    if length_line(x1, y1, x2, y2) > long_length:
                        longest = (x1, y1, x2, y2)
                        long_length = length_line(x1, y1, x2, y2)
                    
                    
                    
            for x1,y1,x2,y2 in [longest]:
                cv2.line(frameClone,(x1,y1),(x2,y2),(0,255,0),20)
                #print('0000naaaaaaa')
                if (round(x2-x1)!=0):
                    arctan = slope(x1,x2,y1,y2)
                else:
                    arctan = 90
                print(arctan)
                
                #discuss and show the way by which angle of line is analysed to SAGAR 
                if 85<=abs(arctan)<=95:
                    
                    # NOTE-WE CAN BREAK FROM HERE BCZ WE GOT THE LINES.
                    #the commands for the pitch will be given here(angle dependent)
                    # print("it's straight")
                    #after the roll is given and track is straight calculate the distance of yellow line from centre and give tolerance
                   
                    if abs((w*0.5)-x1)>roll_limit:
                        if w*0.5 < x1:
                            print('Right hand roll')
                        else:
                            print('Left hand roll')
                        #hence roll is given accordingly
                        #now the detected path is right go on path and hence use the pitch command
                        
                    else:
                        print('Pitch to the next +')
                        #yaw is 0.
                        first_line_found = True
                        
                else:
                    
                    if arctan <= 0:
                        print('Clockwise yaw')
                    else:
                        print('Anti-clockwise yaw')
                    #use the code to give rolling bcz the line has to get almost straight
                        
        else:
            
            if front_flag:
                print('Pitch to find')
                front_flag, left_flag, position = False, True, 0
                
            elif left_flag:
                print('Left hand roll to find')
                position -= 1
                
                if position == 0:
                    front_flag, left_flag = True, False
                elif position == -5:
                    left_flag, right_flag = False, True
                    
            elif right_flag:
                print('Right hand roll to find')
                position += 1
                
                if position == 5:
                    right_flag, left_flag = False, True
    

    elif first_line_found and ( t<10 or (t == 10 and (not outside_plus_flag))):
        
        if type(lines)==np.ndarray:
            perpendicular_attained = False

            longest = longest_line(lines)
            
            
            for x1,y1,x2,y2 in [longest]:
                cv2.line(frameClone,(x1,y1),(x2,y2),(0,255,0),20)
                arctan = slope(x1,x2,y1,y2)
                #choose a nice range to select only 1 principle line
                if 55<=abs(arctan)<=90:
                    
                    if 55<=abs(arctan)<85:
                        #check the positive and negative values of arctan for direction of rotation
                        if arctan <= 0:
                            print('Clockwise yaw')
                        else:
                            print('Anti-clockwise yaw')
                        
                    #we r not using the else for this if bcz we have to focus 
                    elif 85<=abs(arctan)<=90:
                        
                        if abs(w*0.5-x1)>roll_limit:
                            if w*0.5 < x1:
                                print('Right hand roll')
                            else:
                                print('Left hand roll')
                                
                        else:
                            #now u have straight line and right under the drone so detect perpendicular lines if not get pitch
                            #if yes sleep
                            
                            for k in range(len(lines)):
                                i = lines[k]
                                if perpendicular_attained:
                                    break
                                for x1,y1,x2,y2 in i:
                                    
                                    if (round(x2-x1)!=0):
                                        arctan = slope(x1,x2,y1,y2)
                                    else:
                                        arctan=90
                                    
                                    try:
                                        m1=float(y2-y1)/float(x2-x1)
                                    except ZeroDivisionError:
                                        m1 = 600000
                                    c1=float(y1)-m1*float(x1)
                                    
                                    for j in lines[k+1:]:
                                        if perpendicular_attained:
                                            break
                                        for x3,y3,x4,y4 in j:
                                            
                                            arctan1 = slope(x3,x4,y3,y4)
                                            try:
                                                m2=float(y4-y3)/float(x4-x3)
                                            except ZeroDivisionError:
                                                m2 = 600000
                                            c2=float(y4)-m2*float(x4)
                                            
                                            #CHOOSE a range for perpendicular line
                                            if 85<abs(arctan1-arctan)<90:
                                                cv2.line(frameClone,(x3,y3),(x4,y4),(0,255,0),20)
                                                #print('bhaii perpendicular lines')
                                                l=dis(m1,c1,m2,c2)
                                                #need to give pitch
                                                #check here the l size according the conditions
                                                if l<radius_limit:
                                                    #make it stop and count t
                                                    
                                                    perpendicular_attained = True
                                                    
                                                    if not outside_plus_flag:
                                                        print('Pitch OUT of the +')
                                                        
                                                        
                                                    elif t==5:
                                                        #t should be 5 not 4
                                                        print('Turn in such a way that camera is balanced')
                                                        print('Pitch OUT of the +')
                                                        #sleep here too bcz needs to give pitch also time duration may be fine
                                                        #t=t+1 is needed otherwise the drone will rotate
                                                        t=t+2
                                                        outside_plus_flag = False
                                                        
                                                    elif t<5 or 6<t<11:
                                                        print('Stay')
                                                        print('Pitch OUT of the +')
                                                        outside_plus_flag = False
                                                        t=t+1
                                                        #watch if any else condition needs to keep
                                                        #take photos
                                                else:
                                                    outside_plus_flag = True
                                                        
##                                                else:
##                                                    print('Pitch to the next + (inside)')
##                                                    time.sleep(0.001)
                                                        
                            if not perpendicular_attained:
                                print('Pitch to the next +')
                                               
                                                
        else:
            
            if front_flag:
                print('Pitch')
                front_flag, left_flag, position = False, True, 0
                
            elif left_flag:
                print('Left hand roll')
                position -= 1
                if position == 0:
                    front_flag, left_flag = True, False
                elif position == -5:
                    left_flag, right_flag = False, True
                    
            elif right_flag:
                print('Right hand roll')
                position += 1
                if position == 5:
                    right_flag, left_flag = False, True
            #now below use elif if for generating the code for line loss

    
    else:
        
        if type(lines)==np.ndarray and (not line_end_flag):
            for x1,y1,x2,y2 in lines[0]:
                arctan = slope(x1,x2,y1,y2)
                
                #choose a nice range to select only 1 principle line
                if 0<=abs(arctan)<=90:
                    if 55<=abs(arctan)<=85:
                        #check the positive and negative values of arctan for direction of rotation
                        if arctan <= 0:
                            print('Clockwise yaw (square)')
                        else:
                            print('Anti-clockwise yaw (square)')
                            
                    #we r not using the else for this if bcz we have to focus 
                    if 85<abs(arctan)<=90:
                        
                         if abs((w*0.5)-x1)>roll_limit:
                            if w*0.5 < x1:
                                print('Right hand roll (square)')
                            else:
                                print('Left hand roll (square)')
                                
                         else:
                             print('Pitch (square)')
            
            
        else:
            if not line_end_flag:
                line_end_flag = True
                print("Zoom out")
            #it will go above and then pitch will be given
            #detect a square and stop the flying
            
            elif shape(frame)!=1:
                print('Pitch to the square')
            else:
                print('Land')
    cv2.imshow('frameClone',frameClone)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#cap.release()
cv2.destroyAllWindows()
