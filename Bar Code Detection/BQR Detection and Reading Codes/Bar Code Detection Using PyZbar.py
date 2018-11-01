Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:25:58) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import urllib
>>> from urllib.request import urlopen

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    from urllib.request import urlopen
ImportError: No module named request
>>> for i in 's':
	url = 'https://upload.wikimedia.org/wikipedia/commons/8/8f/Qr-2.png'
	data = qreader.read(urllib.urlopen(url))
	print(data)  # prints "Version 2"

	

Traceback (most recent call last):
  File "<pyshell#4>", line 3, in <module>
    data = qreader.read(urllib.urlopen(url))
NameError: name 'qreader' is not defined
>>> import qreader
>>> for i in 's':
	url = 'https://upload.wikimedia.org/wikipedia/commons/8/8f/Qr-2.png'
	data = qreader.read(urllib.urlopen(url))
	print(data)  # prints "Version 2"

	

Traceback (most recent call last):
  File "<pyshell#7>", line 3, in <module>
    data = qreader.read(urllib.urlopen(url))
  File "C:\Python2764\lib\site-packages\qreader\api.py", line 34, in read
    raise TypeError('parameter should be a PIL image object, a file-like object, or a path to an image file')
TypeError: parameter should be a PIL image object, a file-like object, or a path to an image file
>>> import qrcode
>>> help (qrcode)
Help on package qrcode:

NAME
    qrcode

FILE
    c:\python2764\lib\site-packages\qrcode\__init__.py

PACKAGE CONTENTS
    base
    console_scripts
    constants
    exceptions
    image (package)
    main
    mecard
    speedy
    tests (package)
    util

FUNCTIONS
    run_example(data='http://www.lincolnloop.com', *args, **kwargs)
        Build an example QR Code and display it.
        
        There's an even easier way than the code here though: just use the ``make``
        shortcut.

DATA
    ERROR_CORRECT_H = 2
    ERROR_CORRECT_L = 1
    ERROR_CORRECT_M = 0
    ERROR_CORRECT_Q = 3


>>> run_example(data='http://www.lincolnloop.com', *args, **kwargs)

Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    run_example(data='http://www.lincolnloop.com', *args, **kwargs)
NameError: name 'run_example' is not defined
>>> qrcode.run_example(data='http://www.lincolnloop.com', *args, **kwargs)

Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    qrcode.run_example(data='http://www.lincolnloop.com', *args, **kwargs)
NameError: name 'args' is not defined
>>> qrcode.run_example(data='http://www.lincolnloop.com')
>>> qrcode.run_example(data='http://www.lincolnloop.com')
>>> import theano
WARNING (theano.configdefaults): g++ not available, if using conda: `conda install m2w64-toolchain`

Warning (from warnings module):
  File "C:\Python2764\lib\site-packages\theano\configdefaults.py", line 560
    warnings.warn("DeprecationWarning: there is no c++ compiler."
UserWarning: DeprecationWarning: there is no c++ compiler.This is deprecated and with Theano 0.11 a c++ compiler will be mandatory
WARNING (theano.configdefaults): g++ not detected ! Theano will be unable to execute optimized C-implementations (for both CPU and GPU) and will default to Python implementations. Performance will be severely degraded. To remove this warning, set Theano flags cxx to an empty string.
WARNING (theano.tensor.blas): Using NumPy C-API based implementation for BLAS functions.
>>> import tflearn

Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    import tflearn
ImportError: No module named tflearn
>>> import tflearn

Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    import tflearn
ImportError: No module named tflearn
>>> import theano
>>> import zbar

Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    import zbar
ImportError: No module named zbar
>>> def dec(path):
	image = cv2.imread('pyzbar/tests/code128.png')
>>> height, width = image.shape[:2]

>>> # 8 bpp by considering just the blue channel
>>> decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
SyntaxError: invalid syntax
>>> def dec(path):
	image = cv2.imread('pyzbar/tests/code128.png')
	height, width = image.shape[:2]

	# 8 bpp by considering just the blue channel
	decode((image[:, :, 0].astype('uint8').tobytes(), width, height))

	
>>> def dec(path):
	image = cv2.imread('pyzbar/tests/code128.png')
	height, width = image.shape[:2]

	# 8 bpp by considering just the blue channel
	print decode((image[:, :, 0].astype('uint8').tobytes(), width, height))

	
>>> path = "C:\Akhilesh\BTech\Inter_IIT_Tech_Meet_'18\Bar Codes"
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	

Traceback (most recent call last):
  File "<pyshell#28>", line 2, in <module>
    dec(path+"\\b000"+str(i)+".jpg")
  File "<pyshell#24>", line 2, in dec
    image = cv2.imread('pyzbar/tests/code128.png')
NameError: global name 'cv2' is not defined
>>> import cv2
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	

Traceback (most recent call last):
  File "<pyshell#31>", line 2, in <module>
    dec(path+"\\b000"+str(i)+".jpg")
  File "<pyshell#24>", line 3, in dec
    height, width = image.shape[:2]
AttributeError: 'NoneType' object has no attribute 'shape'
>>> def dec(path):
	image = cv2.imread(path)
	height, width = image.shape[:2]

	# 8 bpp by considering just the blue channel
	print decode((image[:, :, 0].astype('uint8').tobytes(), width, height))

	
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	

Traceback (most recent call last):
  File "<pyshell#35>", line 2, in <module>
    dec(path+"\\b000"+str(i)+".jpg")
  File "<pyshell#33>", line 6, in dec
    print decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
NameError: global name 'decode' is not defined
>>> def dec(path):
	image = cv2.imread(path)
	height, width = image.shape[:2]

	# 8 bpp by considering just the blue channel
	print pyzbar.decode((image[:, :, 0].astype('uint8').tobytes(), width, height))

	
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	

Traceback (most recent call last):
  File "<pyshell#39>", line 2, in <module>
    dec(path+"\\b000"+str(i)+".jpg")
  File "<pyshell#37>", line 6, in dec
    print pyzbar.decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
NameError: global name 'pyzbar' is not defined
>>> import pyzbar

Traceback (most recent call last):
  File "<pyshell#40>", line 1, in <module>
    import pyzbar
ImportError: No module named pyzbar
>>> import pyzbar
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	

Traceback (most recent call last):
  File "<pyshell#43>", line 2, in <module>
    dec(path+"\\b000"+str(i)+".jpg")
  File "<pyshell#37>", line 6, in dec
    print pyzbar.decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
AttributeError: 'module' object has no attribute 'decode'
>>> frompyzbar.pyzbar import decode
SyntaxError: invalid syntax
>>> from pyzbar.pyzbar import decode
>>> def dec(path):
	image = cv2.imread(path)
	height, width = image.shape[:2]

	# 8 bpp by considering just the blue channel
	print decode((image[:, :, 0].astype('uint8').tobytes(), width, height))

	
>>> for i in xrange(1,5):
	dec(path+"\\b000"+str(i)+".jpg")

	
[Decoded(data='C1436800003.', type='CODE39'), Decoded(data='M89914308L', type='CODE39'), Decoded(data='407264N', type='CODE39')]
[Decoded(data='C1436800003.', type='CODE39'), Decoded(data='M89914308L', type='CODE39')]
[Decoded(data='407264N', type='CODE39')]
[]
>>> for i in xrange(5,7):
	dec(path+"\\b000"+str(i)+".jpg")

	
[]
[]
>>> dec(path+"\\b000"+str(7)+".jpg")
[Decoded(data='M85006309A', type='CODE39'), Decoded(data='406517N', type='CODE39')]

>>> 
