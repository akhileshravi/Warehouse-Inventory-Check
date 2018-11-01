# import the necessary packages
from imutils import paths
import argparse
import cv2
from os import listdir
 
def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

path = "C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_'18\\Bar Codes"
threshold = 200

# loop over the input images
for imageName in listdir(path):
    if imageName[-3:] in ['jpg', 'png', 'bmp']:
        t = time.time()
        # load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian
        # method
        imagePath = path + '\\' + imageName
        
        image1 = cv2.imread(imagePath)
        
        if type(image1) == type(None):
            continue
        image = cv2.resize(image1, (400,400))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        text = "Not Blurry"

        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < threshold:
            text = "Blurry"

        # show the image
        cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Image", image)
        key = cv2.waitKey(0)

cv2.destroyAllWindows()
