"""
Screenshot Base
Takes Screenshot and Fullscreens

"""

import pygame
from PIL import Image as Im
from PIL import ImageGrab, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys
import os
import time
from transforms import RGBTransform
import random

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

def screenshot():
	im= ImageGrab.grab(bbox=None)
	#http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
	scr = im.convert("RGB")
	# https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
	# https://stackoverflow.com/questions/25202092/pil-and-pygame-image
	data = scr.tobytes()
	size = scr.size
	mode = scr.mode
	return data, size, mode

# Background class acts as the "sprite" image behind all other game elements 
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame/28005796
class Background(pygame.sprite.Sprite):
	def __init__(self,data,size,mode,location):
		pygame.sprite.Sprite.__init__(self)
		self.data,self.size,self.mode = data,size,mode
		self.image = pygame.image.fromstring(data,size,mode)
		# https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
		self.image = pygame.transform.scale(self.image, (infoObject.current_w,infoObject.current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

	def scrnMod(self):
		scrn = RGBTransform().mix_with((255,255,255),factor=.12).applied_to(Im.frombytes(self.mode,self.size,self.data))
		scrn = RGBTransform().mix_with((0,0,255),factor=.12).applied_to(scrn)
		data = scrn.tobytes()
		size = scrn.size
		mode = scrn.mode
		self.new = pygame.image.fromstring(data,size,mode)
		self.new = pygame.transform.scale(self.new, (int(round(infoObject.current_w*1.005)),int(round(infoObject.current_h*1.005))))
		return self.new

class Player:
	def __init__(self):
		self.length = 10
		self.coords = [[(10-i)*20,0] for i in range(self.length)]
		self.speed = 20

	def move(self,direction):
		while len(self.coords)!=self.length:
			self.coords.append([0,0])
		for i in range(self.length-1,0,-1):
			self.coords[i][0]=self.coords[i-1][0]
			self.coords[i][1]=self.coords[i-1][1]
		if direction<=1:
			self.coords[0][0] += self.speed*(-1)**direction
		else:
			self.coords[0][1] += self.speed*(-1)**direction

class Apple:
	def __init__(self):
		self.coords = [random.randrange(20,infoObject.current_w,20)-20,random.randrange(20,infoObject.current_h,20)-20]

	def reroll(self):
		self.coords = [random.randrange(20,infoObject.current_w,20)-20,random.randrange(20,infoObject.current_h,20)-20]

#retrieves screenshot data
pygame.init()
print("Taking screenshot in...")
# for i in range(5):
# 	print(5-i)
# 	time.sleep(1)
data,size,mode = screenshot()

# initializes pygame in fullscreen and sets screen background.
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen.fill([255,255,255])
infoObject = pygame.display.Info()
BackGround = Background(data,size,mode,[0,0])
appleSprite = pygame.image.load(os.path.join(image_path, 'cursor.png')).convert_alpha()
appleSprite = pygame.transform.scale(appleSprite, (13,19))
screen.blit(BackGround.image, BackGround.rect)
red = 255,0,0
player = Player()
apple = Apple()
while apple.coords in player.coords:
	apple.reroll()
playerSprite = BackGround.scrnMod()
current = 0

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_l:
				if current!=1:
					current = 0
			elif event.key == pygame.K_a:
				if current!=0:
					current = 1
			elif event.key == pygame.K_m:
				if current!=3:
					current = 2
			elif event.key == pygame.K_w:
				if current!=2:
					current = 3
			elif event.key == pygame.K_ESCAPE:
				sys.exit()
	player.move(current)
	if player.coords[0][0]>=infoObject.current_w:
		player.coords[0][0]=0
	elif player.coords[0][0]<0:
		player.coords[0][0]=infoObject.current_w-20
	if player.coords[0][1]>=infoObject.current_h:
		player.coords[0][1]=0
	elif player.coords[0][1]<0:
		player.coords[0][1]=infoObject.current_h-20
	if player.coords[0] in player.coords[1:-1]:
		break
	screen.blit(BackGround.image, BackGround.rect)
	screen.blit(appleSprite,(apple.coords[0],apple.coords[1]))
	print(len(player.coords))
	for i in range(player.length):
		screen.blit(playerSprite,(player.coords[i][0],player.coords[i][1]),(player.coords[i][0],player.coords[i][1],20,20))
	if player.coords[0] == apple.coords:
		player.length+=2
		apple.reroll()
		while apple.coords in player.coords:
			apple.reroll()
	print(apple.coords)
	pygame.display.flip()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
	screen.blit(BackGround.image, BackGround.rect)
	for i in range(player.length):
		screen.blit(playerSprite,(player.coords[i][0],player.coords[i][1]),(player.coords[i][0],player.coords[i][1],20,20))
	print(apple.coords)
	pygame.display.flip()
