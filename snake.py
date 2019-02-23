"""
Snake
by Kevin & Knute

Original code for a transparent game of Snake.

Controls:
W - up
A - left
M - down
L - right
ESC - pause when game is running, exit to main menu when game is paused/over

Functionality derived from tutorial:
https://pythonspot.com/snake-with-pygame/

"""

import sys, pygame, random, time, os
from sys import platform

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

# Player class contains snake properties
class Player:
	# Sets initial properties
	def __init__(self):
		self.length = 10 # Initial length
		self.coords = [[(10-i)*20,0] for i in range(self.length)] # each segment is a 20x20px square
		self.speed = 20 # Moves one segment at a time
		self.score = 0 # Initial score

	# Function called each time snake state changes (location, length etc.)
	def move(self,direction):
		# While loop assigns coordinates to each new segment unaccounted for from length property
		while len(self.coords)!=self.length:
			self.coords.append([0,0])
		self.score = (self.length-10)*10 # Score increases by 10 for each additional segment
		# For each segment in snake in backwards order, the segment takes the x,y coordinate of the segment in front of it, simulating movement
		for i in range(self.length-1,0,-1):
			self.coords[i][0]=self.coords[i-1][0] 
			self.coords[i][1]=self.coords[i-1][1]
		# direction value is determined by play() function.
		if direction<=1:
			self.coords[0][0] += self.speed*(-1)**direction # 1 left, 0 right
		else:
			self.coords[0][1] += self.speed*(-1)**direction # 2 down, 3 up

# Apple function determines and stores location of "cursor" apple
class Apple:
	# Sets first coordinates
	def __init__(self):
		self.coords = [random.randrange(0,pygame.display.Info().current_w,20),random.randrange(0,pygame.display.Info().current_h,20)]
	# Sets new coordinates (if "cursor" coordinates are in snake or snake eats "cursor")
	def reroll(self):
		self.coords = [random.randrange(0,pygame.display.Info().current_w,20),random.randrange(0,pygame.display.Info().current_h,20)]

# Actual game class
class Snake:
	# Sets classes and initial properties, receives screen, OS-specific cursor, and screenshot files from home.py
	def __init__(self, screen, cursor, BackGround):
		# Detects OS for OS-specific functionality
		self.mac = False 
		if platform == "darwin":
			self.mac = True
		pygame.mouse.set_visible(0) # Sets mouse invisible
		# Properties used for blitting objects in play and pause functions
		self.screen = screen 
		self.BackGround = BackGround
		self.appleSprite = cursor
		# Initializes snake and "cursor" apple
		self.player = Player()
		self.apple = Apple()
		# If apple is already within snake coordinates, reset apple coordinates until it isn't
		while self.apple.coords in self.player.coords:
			self.apple.reroll()
		# Makes PlayerSprite "translucent" and adds "crystalline" diffraction look
		self.playerSprite = BackGround.scrnMod
		self.current = 0 # current direction

	# Plays game (snake moving)
	def play(self):
		# Loop refreshes screen after every process (snake movement)
		while 1:
			# If pygame detects event, parse event (usually keystroke) to correct function
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				# Assigns keystrokes to current movement direction
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_l: # right
						if self.current!=1:
							self.current = 0
					elif event.key == pygame.K_a: # left
						if self.current!=0:
							self.current = 1
					elif event.key == pygame.K_m: # down
						if self.current!=3:
							self.current = 2
					elif event.key == pygame.K_w: # up
						if self.current!=2:
							self.current = 3
					elif event.key == pygame.K_ESCAPE: # if player presses "escape," game pauses and minimizes
						if not self.mac: # iconify crashes mac app
							pygame.display.iconify()
						if self.pause(0): # if user presses esc twice, then game returns to main menu
							return
			self.player.move(self.current) # moves player (see move() function)

			# wraps snake around screen if segment coordinates exceed width or height domains
			if self.player.coords[0][0]>=pygame.display.Info().current_w:
				self.player.coords[0][0]=0
			elif self.player.coords[0][0]<0:
				self.player.coords[0][0]=pygame.display.Info().current_w-20
			if self.player.coords[0][1]>=pygame.display.Info().current_h:
				self.player.coords[0][1]=0
			elif self.player.coords[0][1]<0:
				self.player.coords[0][1]=pygame.display.Info().current_h-20

			# if snake moves into a coordinate that is included in the snakes other coordinates, game over, return to menu.
			if self.player.coords[0] in self.player.coords[1:-1]:
				self.pause(1) # 1 indicates game over
				return

			# BLITTING: blits all of the sprites onto screen based on coordinates provided by self.player, self.apple and textures from BackGround
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			self.screen.blit(self.appleSprite,(self.apple.coords[0],self.apple.coords[1]))
			# Blitting a selected area of an image: https://stackoverflow.com/questions/32781858/pygame-blit-part-of-an-imagebackground-image
			# Blits one 20x20 square for each segment of the snake at the corresponding coordinates
			for i in range(self.player.length):
				self.screen.blit(self.playerSprite,(self.player.coords[i][0],self.player.coords[i][1]),(self.player.coords[i][0],self.player.coords[i][1],20,20))
			
			# Detects if snake collides with "cursor" apple and rerolls apple coordinates if so
			if self.player.coords[0] == self.apple.coords:
				self.player.length+=2
				self.apple.reroll()
				while self.apple.coords in self.player.coords:
					self.apple.reroll()
			# sets score text based on player.score
			scoretext = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),30).render(str(self.player.score), True, (0,255,255))
			scoretextrect = scoretext.get_rect()
			scoretextrect = scoretextrect.move(pygame.display.Info().current_w - scoretextrect.right, 0)

			# Blits score onto corner
			self.screen.blit(scoretext, scoretextrect)
			pygame.display.flip() # displays screen

	# pauses game (snake not moving)
	def pause(self, status):
		# Loop refreshes to detect keystrokes
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				# on keystroke, if game is just paused, directional keys will return to self.play(). Escape always returns to self.play() then home.py
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return True
					if event.key in [pygame.K_w,pygame.K_m,pygame.K_a,pygame.K_l] and status == 0:
						return False
			# if game is over, score and text is displayed on screen.
			if status == 1:
				msg = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),30).render("Game Over! Score: " + str(self.player.score), True, (0,255,255))
				msgrect = msg.get_rect()
				msgrect = msgrect.move(0, 0)
				self.screen.blit(msg, msgrect)
			pygame.display.flip() # displays screen