Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:17:05) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
======= RESTART: C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Decoder.py =======
>>> import cv2
>>> import Decoder
>>> img = cv2.imread("C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_'18\\QR Codes\\qr0014.png")
>>> Decoder.dec(img)
[Decoded(data=b'http://qrd.by', type='QRCODE')]
>>> Decoder.dec(img)
[Decoded(data=b'http://qrd.by', type='QRCODE')]
>>> Decoder.dec(None, "C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_'18\\QR Codes\\qr0014.png")
[Decoded(data=b'http://qrd.by', type='QRCODE')]
>>> Decoder.dec(path = "C:\\Akhilesh\\BTech\\Inter_IIT_Tech_Meet_'18\\QR Codes\\qr0014.png")
[Decoded(data=b'http://qrd.by', type='QRCODE')]
>>> height, width = img.shape[:2]
>>> smaller_width = int(width*0.67)
>>> img2 = [0:smaller_width, 0:height]
SyntaxError: invalid syntax
>>> img2 = img[0:smaller_width, 0:height]
>>> Decoder.dec(img2)
[Decoded(data=b'http://qrd.by', type='QRCODE')]
>>> import "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Decoder.py"
SyntaxError: invalid syntax
>>> import C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Decoder.py
SyntaxError: invalid syntax
>>> 
