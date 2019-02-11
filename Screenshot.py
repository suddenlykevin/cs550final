'''
Do screenshot 
'''

from PIL import ImageGrab
im= ImageGrab.grab()
#http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
image = im.convert("RGB")
#https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
image.save("userdesktop.jpg", "JPEG")

