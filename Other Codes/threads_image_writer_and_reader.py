from thread import start_new_thread
from time import sleep
import os
from shutil import copy2
import cv2



path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18"
path1 = path + "\HelloImages"
path2 = path + '\Bar Codes'

def clear():
    path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18"
    try:
        os.mkdir(path + '\HelloImages')
    except:
        pass
    os.chdir(path + '\HelloImages')
    cwd = os.getcwd()
    for i in os.listdir(cwd):
        try:
            os.remove(i)
        except:
            pass

def copyimages(n, name, txt):
    """Writes n files"""
    try:
        os.mkdir(path)
    except:
        pass
    
    for i in xrange(1, n+1):

        try:
            copy2(path2 + "\\b000" + str(i) + ".jpg", path1)
            sleep(1.5)
        except IOError:
            pass
    
def readimages():
    path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\\Hello"
    files0 = []
    os.chdir
    while True:
        files1 = os.listdir(path1)
        if files1 != files0:
            for i in files1:
                if i not in files0:
                    print i,
                    try:
                        img = cv2.imread(i)
                        cv2.imshow(i,img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    except:
                        pass
        files0 = files1

clear()
start_new_thread(readimages,())
start_new_thread(copyimages,(10,'Hi','Fil'))
##
