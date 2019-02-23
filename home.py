"""`
2/22/2019

CLASSWORK
Final Project for CS550 by Kevin Xie and Knute Broady 

Problem: I'M BORED IN CLASS!

The goal of this project was to hide games in a user's screen so that they 
could be played without other people knowing. Once the program is run through 
terminal, the user has 3 seconds to go to their chosen background window before 
the program takes a screenshot that will be used as the backgroud of the game. 
There are to games to choose from, a "sneaky" snake game and a "buried" brick 
breaker game. This can be chosen through the GUI after launch. The snake game 
is controlled using 'W' for up, 'M' for down, 'L' for left and 'A' for right. 
These controls were chosen to make it less obvious that the user is playing 
a game. For brick breaker the controls are just the arrow keys, left arrow 
for left, right arrow for right. For groupwork (2-player Pong), players use
I, M and W, X to control their respective paddles. The mouse object, that is 
used in all games, changes depending on the user's OS. While playing, 
the user can minimize and pause the game by pressing esc and resume by 
reopening the window and pressing any movement key. The user can exit back to 
the main menu using esc when each game is over. On the main menu, the user can 
quit by pressing esc. There are two examples of translucency in this game,
one using the alpha property of png files, and another using RGB manipulations
of the background to emulate transparency and offset to emulate "diffraction" of light.

Universal Sources: (applies to all files)
https://www.pygame.org/docs/
Python Package Project: Pygame by Mia
https://pillow.readthedocs.io/en/3.3.x/reference/Image.html

Specific Sources:
Snake game tutorial: https://pythonspot.com/snake-with-pygame/
Brickbreaker game template: http://www.johncheetham.com/projects/breakout
Screenshot related: https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
					https://stackoverflow.com/questions/25202092/pil-and-pygame-image 
					http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
Blitting specific area of an image: https://stackoverflow.com/questions/32781858/pygame-blit-part-of-an-imagebackground-image
Title screen & Buttons: https://pythonprogramming.net/pygame-button-function-events/
Display properties: https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
OS Detection: https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on

On my honor, I have neither given nor received unauthorized aid.
Kevin Xie & Knute Broady

"""

import pygame
from PIL import Image as Im
from PIL import ImageGrab
import sys
import os
import time
from transforms import RGBTransform
from sys import platform

# links to other game files
from snake import Snake 
from brick import Breakout
from groupwork import Groupwork

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path
mac = False # if mac is True, functionality differs slightly (minimize/iconify doesn't work)

pygame.init()
pygame.font.init()

# Function for generating a button: https://pythonprogramming.net/pygame-button-function-events/
# takes screen to blit onto, text, location, sprite to map onto button, and function to call on press
def button(screen,msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed()
    # if mouse position is within the bounds of a button, it changes to active texture (brighter background)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.blit(ac,(x,y), (x,y,w,h))
        # If mouse clicks on a button, it executes action
        if click[0] == 1 and action != None:
            action()         
    else:
        screen.blit(ic, (x,y), (x,y,w,h))
    # blits text at correct position on top of button
    smallText = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),20) # opening a cusotm ttf file: https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font
    textSurf = smallText.render(msg,True,[255,255,255])
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

# Screenshot function takes screenshot and converts it to data that pygame can read
# PIL screenshot source: http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
def screenshot():
	im= ImageGrab.grab(bbox=None)
	# PIL screenshots in different modes (RGBA for mac and RGB for windows), so they must be standardized to RGB for next operations
	scr = im.convert("RGB")
	# Converting PIL to pygame: https://stackoverflow.com/questions/25202092/pil-and-pygame-image
	# Returns raw data from screenshot
	data = scr.tobytes()
	size = scr.size
	mode = scr.mode
	return data,size,mode

# Background class acts as the "sprite" image behind all other game elements 
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame/28005796
class Background(pygame.sprite.Sprite):
	# takes RAW data from screenshot and converts it to pygame sprites of different variations (for transparency effect)
	def __init__(self,data,size,mode,location):
		pygame.sprite.Sprite.__init__(self)
		self.data,self.size,self.mode = data,size,mode
		# converting from string to image: pygame docs
		self.image = pygame.image.fromstring(data,size,mode)
		# transforming file to the resolution of a screen: https://stackoverflow.com/questions/19954469/how-to-get-the-resolution-of-a-monitor-in-pygame
		self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_w,pygame.display.Info().current_h))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

		# Creates "transparent" sprites to be used by Snake game and buttons
		mixFac = [.12,.2] # .12 is dim sprite and .2 is a brighter sprite
		for i in range(2):
			scrn = RGBTransform().mix_with((255,255,255),factor=mixFac[i]).applied_to(Im.frombytes(self.mode,self.size,self.data))
			scrn = RGBTransform().mix_with((0,0,255),factor=mixFac[i]).applied_to(scrn)
			data = scrn.tobytes()
			size = scrn.size
			mode = scrn.mode
			# saves two images: dimmer transparent texture and brighter transparent texture with a "crystalline" diffraction effect
			if i == 0:
				self.scrnMod = pygame.image.fromstring(data,size,mode)
				self.scrnMod = pygame.transform.scale(self.scrnMod, (int(round(pygame.display.Info().current_w*1.005)),int(round(pygame.display.Info().current_h*1.005))))
			else:
				self.scrnMod1 = pygame.image.fromstring(data,size,mode)
				self.scrnMod1 = pygame.transform.scale(self.scrnMod1, (int(round(pygame.display.Info().current_w*1.005)),int(round(pygame.display.Info().current_h*1.005))))

# Main app and menu system class
class Home:
	# assembles properties
	def __init__(self):
		self.data,self.size,self.mode = screenshot()
		# initializes pygame in fullscreen and sets screen background.
		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.screen.fill([255,255,255])
		self.BackGround = Background(self.data,self.size,self.mode,[0,0])
		self.screen.blit(self.BackGround.image, self.BackGround.rect)

		# OS detection: https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
		# Detects OS for compatibility reasons: Mac will change cursor image and disable "Iconify()"
		if platform == "darwin":
			self.cursor = pygame.image.load(os.path.join(image_path, 'cursor1.png')).convert_alpha()
			self.cursor = pygame.transform.scale(self.cursor, (15,22))
			mac = True # to change functionality on different OSs
		elif platform == "win32" or platform == "win64":
			self.cursor = pygame.image.load(os.path.join(image_path, 'cursor.png')).convert_alpha()
			self.cursor = pygame.transform.scale(self.cursor, (int(pygame.display.Info().current_w*0.0065),int(pygame.display.Info().current_w*0.00975)))
	
	# Function opens Snake with relevant properties
	def opensnake(self):
		snake = Snake(self.screen,self.cursor,self.BackGround,mac) # allows Snake to manipulate screen, blit cursor and background
		snake.play() 
		pygame.mouse.set_visible(1) # once Snake returns, mouse is visible again
		time.sleep(1) # buffer so ESC does not register twice

	# Function opens Brickbreaker with relevant properties
	def openbrick(self):
		br = Breakout()
		br.main(self.screen,self.cursor,self.BackGround,mac)
		pygame.mouse.set_visible(1)
		time.sleep(1)

	def opengroup(self):
		group = Groupwork(self.screen,self.cursor,self.BackGround,mac)
		group.play()
		pygame.mouse.set_visible(1)
		time.sleep(1)

	# Initializes menu on screen
	def play(self):
		# for "breathing" title screen
		i=0
		t=1

		while 1:
			# blits background image behind all other elements
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			# shuts down if ESC is entered on menu screen
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()

			# "Breathing" title screen; large "CLasswork" text moves from black to white and vice versa in a loop
			t+=1
			u=t//255
			i+=1*(-1)**u
			largeText = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),118)
			TextSurf = largeText.render("Classwork",True,[i+2,i+2,i+2])
			TextRect = TextSurf.get_rect()
			TextRect.center = ((pygame.display.Info().current_w/2),(pygame.display.Info().current_h/2))

			# Generates buttons using button() function defined above. Connects functions to execute Snake/Brickbreaker
			button(self.screen,"SNEAKY SNAKE", (pygame.display.Info().current_w/5), (pygame.display.Info().current_h*3/4), pygame.display.Info().current_w/5, 50, self.BackGround.scrnMod, self.BackGround.scrnMod1, self.opensnake)
			button(self.screen,"BURIED BRICK", (pygame.display.Info().current_w*3/5), (pygame.display.Info().current_h*3/4), pygame.display.Info().current_w/5, 50, self.BackGround.scrnMod, self.BackGround.scrnMod1, self.openbrick)
			button(self.screen,"GROUPWORK", (pygame.display.Info().current_w*2/5), (pygame.display.Info().current_h*1/5), pygame.display.Info().current_w/5, 50, self.BackGround.scrnMod, self.BackGround.scrnMod1, self.opengroup)

			# Blits title on screen
			self.screen.blit(TextSurf,TextRect)
			pygame.display.flip()

# Let the fun begin! (if you're running the original file only)
if __name__ == '__main__':
	print("Capturing screen in...")
	# Countdown
	for i in range(3):
		print(str(3-i)+"...")
		time.sleep(1)
	# Initializes game!
	start = Home()
	start.play()