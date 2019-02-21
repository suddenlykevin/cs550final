"""`
Home Screen

Universal Sources:
https://www.pygame.org/docs/
Python Package Project: Pygame by Mia
https://pillow.readthedocs.io/en/3.3.x/reference/Image.html

"""

import pygame
from PIL import Image as Im
from PIL import ImageGrab, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys
import os
import time
from transforms import RGBTransform
from sys import platform
from snake import Snake
from brick import Breakout

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

pygame.init()
pygame.font.init()

def button(screen,msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),20)
    textSurf = smallText.render(msg,True,[255,255,255])
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

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
		self.data,self.size,self.mode = data,size,mode
		self.image = pygame.image.fromstring(data,size,mode)
		# https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
		self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_w,pygame.display.Info().current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

	def scrnMod(self, value):
		# https://stackoverflow.com/questions/32578346/how-to-change-color-of-image-using-python
		if value == 1:
			mixFac = .2
		else:
			mixFac = .12
		scrn = RGBTransform().mix_with((255,255,255),factor=mixFac).applied_to(Im.frombytes(self.mode,self.size,self.data))
		scrn = RGBTransform().mix_with((0,0,255),factor=mixFac).applied_to(scrn)
		data = scrn.tobytes()
		size = scrn.size
		mode = scrn.mode
		self.new = pygame.image.fromstring(data,size,mode)
		self.new = pygame.transform.scale(self.new, (int(round(pygame.display.Info().current_w*1.005)),int(round(pygame.display.Info().current_h*1.005))))
		return self.new
# retrieves screenshot data

class Home:
	def __init__(self):
		self.data,self.size,self.mode = screenshot()
		# initializes pygame in fullscreen and sets screen background.
		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.screen.fill([255,255,255])
		self.BackGround = Background(self.data,self.size,self.mode,[0,0])
		self.screen.blit(self.BackGround.image, self.BackGround.rect)
		if platform == "darwin":
			self.cursor = pygame.image.load(os.path.join(image_path, 'cursor1.png')).convert_alpha()
			self.cursor = pygame.transform.scale(self.cursor, (15,22))
		elif platform == "win32" or platform == "win64":
			self.cursor = pygame.image.load(os.path.join(image_path, 'cursor.png')).convert_alpha()
			self.cursor = pygame.transform.scale(self.cursor, (int(pygame.display.Info().current_w*0.0065),int(pygame.display.Info().current_w*0.00975)))
		# https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
	def opensnake(self):
		snake = Snake(self.screen,self.cursor,self.BackGround)
		snake.play()
		pygame.mouse.set_visible(1)
		time.sleep(1)
	def openbrick(self):
		br = Breakout()
		br.main(self.screen,self.cursor,self.BackGround)
		pygame.mouse.set_visible(1)
		time.sleep(1)
	def play(self):
		while 1:
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
			largeText = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),118)
			TextSurf = largeText.render("Homework",True,[255,255,255])
			TextRect = TextSurf.get_rect()
			TextRect.center = ((pygame.display.Info().current_w/2),(pygame.display.Info().current_h/2))
			button(self.screen,"SNEAKY SNAKE", (pygame.display.Info().current_w/5), (pygame.display.Info().current_h*4/5), 300, 50, [200,0,0], [255,0,0], self.opensnake)
			button(self.screen,"BURIED BRICK", (pygame.display.Info().current_w*3/5), (pygame.display.Info().current_h*4/5), 300, 50, [0,200,0], [0,255,0], self.openbrick)
			self.screen.blit(TextSurf,TextRect)
			pygame.display.flip()

print("Capturing screen in...")
for i in range(3):
	print(str(3-i)+"...")
	time.sleep(1)
start = Home()
start.play()