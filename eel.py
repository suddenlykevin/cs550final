"""
Screenshot Base
Takes Screenshot and Fullscreens

"""

import pygame
from PIL import Image, ImageGrab, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys

# Screenshot function takes screenshot and converts it to data that pygame can read
def screenshot():
	im= ImageGrab.grab(bbox=None)
	#http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
	scr = im.convert("RGB")
	# https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
	# https://stackoverflow.com/questions/25202092/pil-and-pygame-image
	data = scr.tobytes()
	size = scr.size
	mode = scr.mode
	return data,size,mode

# Background class acts as the "sprite" image behind all other game elements 
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame/28005796
class Background(pygame.sprite.Sprite):
	def __init__(self,data,size,mode,location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.fromstring(data,size,mode)
		# https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
		infoObject = pygame.display.Info()
		self.image = pygame.transform.scale(self.image, (infoObject.current_w,infoObject.current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

# retrieves screenshot data
data,size,mode = screenshot()

# initializes pygame in fullscreen and sets screen background.
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill([255,255,255])
BackGround = Background(data,size,mode,[0,0])
screen.blit(BackGround.image, BackGround.rect)
red = 255,0,0

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				screen.fill(red)
	pygame.display.flip()
