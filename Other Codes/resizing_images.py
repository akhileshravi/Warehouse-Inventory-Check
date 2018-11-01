import os
from shutil import copyfile
import cv2
from math import ceil

path = r"C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Bar Code Dataset\DATASET"
paths = ['']*4

def resize(imagepath, writepath):
    for i in os.listdir(imagepath):
        image = cv2.imread(imagepath)
        height, width = image.shape[:2]
        t = max(height, width)
        t = ceil(t/300.0)
        h, w = int(height/t), int(width/t)
        resized = cv2.resize(image, (w,h), interpolation = cv2.INTER_AREA)
        cv2.imwrite(writepath + '\\' + i, image)
    




