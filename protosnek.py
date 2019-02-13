"""
Screenshot Base
Takes Screenshot and Fullscreens

"""

import pygame
from PIL import Image, ImageGrab, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys
import os

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

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
		self.image = pygame.transform.scale(self.image, (infoObject.current_w,infoObject.current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class Player:
	length = 10
	x = [0 for i in range(length)]
	y = [0 for i in range(length)]
	speed = 10

	def move(self,direction):
		for i in range(self.length-1,0,-1):
			self.x[i]=self.x[i-1]
			self.y[i]=self.y[i-1]
		if direction<=1:
			self.x[0] += self.speed*(-1)**direction
		else:
			self.y[0] += self.speed*(-1)**direction

# retrieves screenshot data
data,size,mode = screenshot()

# initializes pygame in fullscreen and sets screen background.
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill([255,255,255])
infoObject = pygame.display.Info()
BackGround = Background(data,size,mode,[0,0])
playerSprite = pygame.image.load(os.path.join(image_path, 'cursor.png')).convert_alpha()
playerSprite = pygame.transform.scale(playerSprite, (13,19))
screen.blit(BackGround.image, BackGround.rect)
red = 255,0,0
player = Player()
current = 0

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				if current!=1:
					current = 0
			elif event.key == pygame.K_LEFT:
				if current!=0:
					current = 1
			elif event.key == pygame.K_DOWN:
				if current!=3:
					current = 2
			elif event.key == pygame.K_UP:
				if current!=2:
					current = 3
			elif event.key == pygame.K_ESC:
				sys.exit()
	player.move(current)
	if player.x[0]>=infoObject.current_w:
		player.x[0]=0
	elif player.x[0]<0:
		player.x[0]=infoObject.current_w-10
	if player.y[0]>=infoObject.current_h:
		player.y[0]=0
	elif player.y[0]<0:
		player.y[0]=infoObject.current_h-10
	screen.blit(BackGround.image, BackGround.rect)
	for i in range(player.length):
		screen.blit(playerSprite,(player.x[i],player.y[i]))
	pygame.display.flip()
