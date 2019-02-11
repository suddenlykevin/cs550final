'''
Do screenshot 
'''

from PIL import Image, ImageGrab
im= ImageGrab.grab(bbox=None)
#http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
scr = im.convert("RGB")
#https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
scr.show()
scr.save("userdesktop.jpg", "JPEG")