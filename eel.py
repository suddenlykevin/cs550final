import pygame
from PIL import Image, ImageGrab, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys

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

# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame/28005796
class Background(pygame.sprite.Sprite):
	def __init__(self,data,size,mode,location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.fromstring(data,size,mode)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

data,size,mode = screenshot()
BackGround = Background(data,size,mode,[0,0])

pygame.init()
size = width, height = 320,240
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill([255,255,255])
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
