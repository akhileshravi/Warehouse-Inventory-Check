import numpy as np
import cv2
from pyzbar.pyzbar import decode
import time
from os import listdir
from copy import deepcopy


BARcode = cv2.CascadeClassifier(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Haar xml files\myhaar final barcode.xml")

def slope(vx1, vx2, vy1, vy2):         #Parameters to calculate slope
    if vx1 == vx2:
        return 90
    else:
        m=float(vy2-vy1)/float(vx2-vx1)        #Slope equation
        theta1 = math.atan(m)                  #calculate the slope angle
        return theta1*(180/np.pi)
    
def find_edge_lines(frame):
    ''' Finds the yellow lines in the frame '''
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_white = np.array([0,0,100], dtype=np.uint8)
    upper_white = np.array([180,50,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    minLineLength = 30
    maxLineGap = 80
    
    lines = cv2.HoughLinesP(edges,1,5*np.pi/180,100,minLineLength,maxLineGap)
    
    return lines

def length(x1, y1, x2, y2):
    return ( (x2-x1)**2 + (y2-y1)**2 ) ** 0.5

def find_box_edge(frame):
    height, width = frame.shape[:2]
    part_x1, part_x2, part_y1, part_y2 = ( int(width*0.25), int(width*0.75),
                                           int(height/8.0), int(height*0.6) )
    part_frame = deepcopy(frame[part_y1:part_y2, part_x1:part_x2])
    frameClone = part_frame.copy()
    gray = cv2.cvtColor(part_frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2,2),np.uint8)
    edges = cv2.Canny(gray,75,150)
    dilated_edges = cv2.dilate(edges,kernel,iterations = 5)
    
    erosion = cv2.erode(dilated_edges,kernel,iterations = 2)
    conv2bgr = dilated_edges
    bgr = cv2.cvtColor(conv2bgr, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # change it according to your need !
    lower_white = np.array([0,0,100], dtype=np.uint8)
    upper_white = np.array([180,50,255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(part_frame,part_frame, mask= mask)
    maskbgr = cv2.cvtColor(dilated_edges, cv2.COLOR_GRAY2BGR)
    lines = find_edge_lines(maskbgr)
    print (lines)
    box_edge = None
    #middle_line = 
    if type(lines) != type(None):
##        if len(lines) > 1 and not flag:
##            flag = True
        for i in range(len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                cv2.line(frameClone, (x1, y1), (x2, y2), (0, 255, 0), 3)
                theta = slope(x1, y1, x2, y2)
                if abs(theta) <= 30:
                    if type(box_edge) == type(None):
                        box_edge = (x1, y1, x2, y2)
                        length_of_edge = length(x1, y1, x2, y2)
                    elif length(x1, y1, x2, y2) > length_of_edge:
                        box_edge = (x1, y1, x2, y2)
                        length_of_edge = length(x1, y1, x2, y2)                        
    if type(box_edge) != type(None):
##        cv2.line(frameClone, box_edge[:2], box_edge[2:], (0, 100, 255), 5)
        x1, y1, x2, y2 = box_edge
        box_edge = (part_x1 + x1, part_y1 + y1, part_x1 + x2, part_y1 + y2)
    return box_edge


def detect_hazard(img):
    #An image has to be given as input, not an image path
##    img=cv2.imread(imgpath)
##    orig=deepcopy(img)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #(IITM)SET THE THRESHOLD VALUE FOR YELLOW COLOR
    lower_yellow=np.array([0,100,100])
    upper_yellow=np.array([90,255,255])
    mask=cv2.inRange(hsv,lower_yellow,upper_yellow)
    res=cv2.bitwise_and(img,img,mask=mask)
    image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]
    #img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    yellow_centroids = []
    distances = []
    yellow_count = 0
    
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        
        if 3500<area<10000: #May have to change area limits
            
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            acnt = cnt
            if (width * 1.0/3.0) < cX < (width * 2.0/3.0):
                yellow_count += 1
                centroid = cX, cY
                if yellow_count == 2:
                    return True, True #Down, Up
                '''
                if len(yellow_centroids) in [0,1]:
                    yellow_centroids += [(cX, cY)]
                    distances += [abs(width*0.5 - cX)]
                elif max(distances+[cX]) != cX:
                    index = distances.find(max(distances))
                    del distances[index]
                    del yellow_centroids[index]
                    yellow_centroids += [(cX, cY)]
                    distances += [abs(width*0.5 - cX)]
                    '''
                    
    if yellow_count == 1:
##        kernel = np.ones((5,5),np.uint8)
##        edges = cv2.Canny(img,100,200)
##        dilated_edges = cv2.dilate(img,kernel,iterations = 1)
        x1, y1, x2, y2 = find_box_edge(img)
        y = (y1 + y2)/2
        if centroid[1] > y:
            return True, False
        else:
            return False, True
    elif yellow_count == 0:
        return False, False
            
##    img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
##    cv2.imshow('img',img)
##    cv2.imshow('original',orig)
##    cv2.imshow('mask',mask)
##    cv2.imshow('res',res)
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()


def bqr_read(imgpath):
    img = cv2.imread(imgpath)
    #watch if image size needs to change if yes then change it in proportion.
    #img=cv2.resize(img,(400,400))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bars = BARcode.detectMultiScale(gray)
    z={}
    z1={}
    k=[]
    t=0
    i=0
    while(i<len(bars)):
        x1=bars[i][0]
        x2=bars[i][0]+bars[i][2]
        y1=bars[i][1]
        y2=bars[i][1]+bars[i][3]
        im=img[bars[i][1]:bars[i][1]+bars[i][3],bars[i][0]:bars[i][0]+bars[i][2]]
        e=5
        
        while(e<210 and t<7): #Decide limit of e and addition factor  of e appropriately
            im=img[y1-e:y2+e,x1-e:x2+e]
            Y1=y1-e
            X1=x1-e
            if y1-e<1 or x1-e<1:
                Y1=2
                X1=2
            im=img[Y1:y2+e,X1:x2+e]
            height, width = im.shape[:2]
            a=decode((im[:, :, 0].astype('uint8').tobytes(), width, height))

            ##Added
            index = 0
            while index < len(a):
                if a[index].type == 'QRCODE':
                    del a[index]
                else:
                    index += 1
            
            
            if len(a)!=0 and t<7:
                g=(a[0] in z)
                if g==False:
                    z[a[0]]=[((x1-e)+(x2+e))/2,((y1-e)+(y2+e))/2]
                    X=((x1-e)+(x2+e))/2
                    l=abs(X-(width/2)) 
                    z1[l]=a[0]
                    t=t+1

            e=e+50
        i=i+1
    s=sorted(z1)
    p=[]
    row_wise=[]
    for i in s:
        if len(p)<3:
            p.append(z1[i])
            row_wise.append((z[z1[i]])[1])
        else:
            break
    if len(row_wise)==2:
        if row_wise[0]>row_wise[1]:
            pass
        else:
            p.reverse()
    #change here little bit if we r taking only 1 output
    if len(row_wise)==1: 
        p.append([])
    if len(row_wise)==0:
        p.append([])
        p.append([])
    print('p',p)

    #here starts QRCODE.
    QRcode = cv2.CascadeClassifier(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Haar xml files\myhaar qr code final.xml")
    img = cv2.imread(imgpath)
    #watch if image size needs to change if yes then change it in proportion.
    #img=cv2.resize(img,(400,400))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    qrs = QRcode.detectMultiScale(gray)
    z={}
    z1={}
    k=[]
    t=0
    i=0
    while(i<len(qrs)):
        x1=qrs[i][0]
        x2=qrs[i][0]+qrs[i][2]
        y1=qrs[i][1]
        y2=qrs[i][1]+qrs[i][3]
        im=img[qrs[i][1]:qrs[i][1]+qrs[i][3],qrs[i][0]:qrs[i][0]+qrs[i][2]]
        e=5
        while(e<100 and t<7):
            im=img[y1-e:y2+e,x1-e:x2+e]
            Y1=y1-e
            X1=x1-e
            if y1-e<1 or x1-e<1:
                Y1=2
                X1=2
            im=img[Y1:y2+e,X1:x2+e]
            height, width = im.shape[:2]
            a=decode((im[:, :, 0].astype('uint8').tobytes(), width, height))

            ##Added
            index = 0
            while index < len(a):
                if a[index].type != 'QRCODE':
                    del a[index]
                else:
                    index += 1
            
            if len(a)!=0 and t<7:
                g=(a[0] in z)
                if g==False:
                    z[a[0]]=[((x1-e)+(x2+e))/2,((y1-e)+(y2+e))/2]
                    X=((x1-e)+(x2+e))/2
                    l=abs(X-(width/2)) 
                    z1[l]=a[0]
                    t=t+1
            e=e+35
        i=i+1
    s=sorted(z1)
    q=[]
    row_wise=[]
    for i in s:
        if len(p)<3:
            q.append(z1[i])
            row_wise.append((z[z1[i]])[1])
        else:
            break
    if len(row_wise)==2:
        if row_wise[0]>row_wise[1]:
            pass
        else:
            q.reverse()
    #change here little bit if we r taking only 1 output
    if len(row_wise)==1:
        q.append([])
    if len(row_wise)==0:
        q.append([])
        q.append([])

    print('q',q)

    return p, q

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

def bqr_database(path, data = {}, done = []):
    t = open('new_database.csv', 'r')
    t.seek(0)
    csv = t.readlines()
    num_img = len(listdir(path))
    if len(csv) < num_img:
        csv += ['\n']*(num_img - len(csv)+1)
    for i in listdir(path):
        if i not in done:
            imgpath = path + '\\' + i
            img = cv2.imread(imgpath)
            p, q = bqr_read(imgpath)
            hazards = detect_hazard(img) # hazards = (downHazard, upHazard) 
            s = i.find('_')
            col = int(i[:s])
            data[col] = [p,q]
            done += [i]
            details = csv[col][:-1].split(',')
            details += ['']*(9-len(details))
            line = ''
            if details[0] == '':
                # Serial Number
                details[0] = str(col)
            if details[2] == '' and p[0] != []:
                #Bar Code Down
                #line += str(p[0].data)[2:-1]
                details[2] = str(p[0].data)[2:-1]
            #line += ','
            if details[3] == '' and q[0] != []:
                #QR Code Down
                #line += str(q[0].data)[2:-1]
                details[3] = str(q[0].data)[2:-1]
            #line += ','
            if details[4] == '':
                if hazards[0] == True:
                    details[4] = 'Yes'
                else:
                    details[4] = 'No'

            
            if details[6] == '' and p[1] != []:
                #Bar Code Up
                #line +=str(p[1].data)[2:-1]
                details[6] = str(p[1].data)[2:-1]
            #line += ','
            if details[7] == '' and q[1] != []:
                #QR Code Up
                #line += str(q[1].data)[2:-1]
                details[7] = str(q[1].data)[2:-1]
            #line += '\n'

            if details[8] == '':
                if hazards[1] == True:
                    details[8] = 'Yes'
                else:
                    details[8] = 'No'
                
            csv[col] = ','.join(details) + '\n'
    t.close()
    t = open('new_database.csv', 'w')
    t.seek(0)
    t.writelines(csv)
    t.close()
    return csv, done

print( bqr_database(r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\CSV Tests")[0])
