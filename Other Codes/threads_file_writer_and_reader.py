from thread import start_new_thread
from time import sleep
import os

def clear():
    path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18"
    try:
        os.mkdir(path + '\Hello')
    except:
        pass
    os.chdir(path + '\Hello')
    cwd = os.getcwd()
    for i in os.listdir(cwd):
        try:
            os.remove(i)
        except:
            pass

def writefiles(n, name, txt):
    """Writes n files"""
    path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18"
    try:
        os.mkdir(path + '\Hello')
    except:
        pass
    os.chdir(path + '\Hello')
    cwd = os.getcwd()
##    for i in os.listdir(cwd):
##        try:
##            os.remove(i)
##        except:
##            pass
    for i in xrange(1, n+1):
        a = open(name+str(i)+'.txt','w')
        a.write(txt+str(i))
        a.close()
        sleep(0.5)
        
def readfiles():
    path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\\Hello"
    files0 = []
    while True:
        files1 = os.listdir(path)
        if files1 != files0:
            for i in files1:
                if i not in files0:
                    print i,
                    try:
                        a = open(i)
                        print a.read()
                        a.close()
                    except:
                        pass
        files0 = files1

clear()
start_new_thread(readfiles,())
start_new_thread(writefiles,(10,'Hi','Fil'))
##
