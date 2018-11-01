import cv2
from pyzbar.pyzbar import decode


def dec(image = None, path = None):
    if type(image) == type(None) and type(path) == type(None):
        return None
    elif type(image) == type(None):
        image = cv2.imread(path)
    height, width = image.shape[:2]

    # 8 bpp by considering just the blue channel
    print( decode((image[:, :, 0].astype('uint8').tobytes(), width, height)) )
