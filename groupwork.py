"""
Pong (Groupwork)
by Kevin & Knute

Original code for a transparent game of Pong
Some behavior based on Breakout V 0.1 June 2009 by John Cheetham. Can be found at http://www.johncheetham.com/projects/breakout. 

Controls:
W - Player 1 Up
X - Player 1 Down
I - Player 2 Up
M - Player 2 Down
ESC - pause when game is running, exit to main menu when game is over

Sources (excl. redundant sources in other files -- snake.py, brick.py, home.py):
Detecting simultaneous keystrokes: https://stackoverflow.com/questions/47935303/press-multiple-keys-at-once

"""

import sys, pygame, random, time, os

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

# Paddle class generates the players paddles based on location and processes movement
class Paddle:
	# Initializes based on selected coordinates of paddle and paddle width
	def __init__(self, height, coords):
		self.length = height/5
		self.speed = 20
		self.coords = coords
	# Movement based on play() directional input
	def move(self,direction):
		if direction == 1:
			self.coords[1]+=self.speed
		else:
			self.coords[1]-=self.speed

# Ball class generates a ball and processes movement
class Ball:
	# Stores initial location and speed
	def __init__(self,size):
		self.xspeed = 16
		self.yspeed = 0
		self.coords = [size[0]/2,size[1]/2]
	# Movement based on play() collisions and "bonus" acceleration
	def move(self,vector, bonus):
		# If x speed is negative, then bonus is negative, else bonus is positive (in order to accelerate in direction of movement)
		if vector[0]<0:
			self.coords[0] += vector[0]-bonus
		else:
			self.coords[0] += vector[0]+bonus
		self.coords[1] += vector[1]

# Pong game
class Groupwork:
	# Sets classes and initial properties, receives screen, OS-specific cursor and functinoality, background for refreshing.
	def __init__(self, screen, cursor, BackGround, mac):
		self.mac = mac
		self.screen = screen 
		self.BackGround = BackGround

		# essential for keeping track of ball boundaries
		self.infosize = pygame.display.Info() #info to make the display the correct size 
		self.size = self.width, self.height = int(self.infosize.current_w), int(self.infosize.current_h)
		
		# sets up players (appearance is textured similarly to snake, using transparent screenshot) and ball
		self.playerSprite = BackGround.scrnMod
		self.player1 = Paddle(self.height,[0,self.height*2/5])
		self.player2 = Paddle(self.height,[self.width-20,self.height*2/5])
		self.ball = Ball(self.size)
		self.ballSprite = cursor

		# Initial score and bonus acceleration = 0
		self.score = 0
		self.accel = 0
		pygame.key.set_repeat(1,30) # holding down a key repeats its input
		pygame.mouse.set_visible(0) # actual cursor is invisible

	# Plays game (ball moving)
	def play(self):
		# Refreshes to simulate movement
		while 1:
			# If pygame detects event (quit), then quit.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# React to keystrokes that are being pressed. If this is put into the "event" loop, then only one keystroke will be parsed
			# Paddles can move simultaneously!
			# simultaneous keystrokes: https://stackoverflow.com/questions/47935303/press-multiple-keys-at-once
			keys = pygame.key.get_pressed()
			if keys[pygame.K_i]:
				if self.player2.coords[1]>=0:
					self.player2.move(0)
			if keys[pygame.K_m]:
				if self.player2.coords[1]<=(self.height-self.height/5):
					self.player2.move(1)
			if keys[pygame.K_w]:
				if self.player1.coords[1]>=0:
					self.player1.move(0)
			if keys[pygame.K_x]:
				if self.player1.coords[1]<=(self.height-self.height/5):
					self.player1.move(1)
			if keys[pygame.K_ESCAPE]: # if player presses "escape," game pauses and minimizes
				if not self.mac: # iconify crashes mac app
					pygame.display.iconify()
				self.pause(0)

			# Detects if ball collides with paddle based on ball's borders and paddle's borders
			if (self.ball.coords[1] <= self.player2.coords[1]+self.height/5 and \
				self.ball.coords[1]+self.ballSprite.get_rect().size[1] >= self.player2.coords[1] and \
				self.ball.coords[0]+self.ballSprite.get_rect().size[0] >= self.width-20 and \
				self.ball.coords[0] <= self.width) or \
				(self.ball.coords[1] <= self.player1.coords[1]+self.height/5 and \
				self.ball.coords[1]+self.ballSprite.get_rect().size[1] >= self.player1.coords[1] and \
				self.ball.coords[0]+self.ballSprite.get_rect().size[0] >= 0 and \
				self.ball.coords[0] <= 20): 
				# Reverse ball velocity
				self.ball.xspeed = -self.ball.xspeed
				# Offset from center of paddle determines ball trajectory (offset depends on which paddle you are colliding with)
				if self.ball.coords[0]<60:
					offset = self.ball.coords[1]+(self.ballSprite.get_rect().size[1]/2) - (self.player1.coords[1]+self.height/10)
				else:
					offset = self.ball.coords[1]+(self.ballSprite.get_rect().size[1]/2) - (self.player2.coords[1]+self.height/10)
				# If offset upwards, then ball reflects at upward angle, if offset downwards, ball reflects at downward angle
				if offset > 0:
					if offset > 30:
						self.ball.yspeed = 7
					elif offset > 23:
						self.ball.yspeed = 6
					elif offset > 17:
						self.ball.yspeed = 5
				else:  
					if offset < -30:
						self.ball.yspeed = -7
					elif offset < -23:
						self.ball.yspeed = -6
					elif offset < -17:
						self.ball.yspeed = -5
				# Each collision adds 1 to the rally score
				self.score+=1

			# Collision with wall (based on ball coordinates) reflects ball with same y velocity
			if (self.ball.yspeed>0 and (self.ball.coords[1]+self.ballSprite.get_rect().size[1])>self.height) or (self.ball.yspeed<0 and self.ball.coords[1]<0):
				self.ball.yspeed = -self.ball.yspeed

			# Game over conditions (ball coordinates exceeding width or passing 0)
			if self.ball.coords[0]<=-self.ballSprite.get_rect().size[0]:
				self.pause(1)
				return # Returns to main menu
			if self.ball.coords[0]>=self.width:
				self.pause(2)
				return

			# 1 bonus velocity per 6 rallies up to 6 bonus velocity
			if self.accel<6:
				self.accel = (self.score//6)*1
			self.ball.move([self.ball.xspeed,self.ball.yspeed],self.accel) # moves ball

			# BLITS background, ball, and paddles at correct coordinates with correct textures
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			self.screen.blit(self.ballSprite,(self.ball.coords[0],self.ball.coords[1]))
			# Paddle textures are modified screenshots to emulate transparency and "crystalline" diffraction
			self.screen.blit(self.playerSprite,(self.player1.coords[0],self.player1.coords[1]),(self.player1.coords[0],self.player1.coords[1],20,self.height/5))
			self.screen.blit(self.playerSprite,(self.player2.coords[0],self.player2.coords[1]),(self.player2.coords[0],self.player2.coords[1],20,self.height/5))
			
			# places score in correct font in corner
			scoretext = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),30).render(str(self.score), True, (0,255,255))
			scoretextrect = scoretext.get_rect()
			scoretextrect = scoretextrect.move(self.width-40, 0)

			# Blits score onto corner
			self.screen.blit(scoretext, scoretextrect)
			pygame.display.flip() # displays screen

	# pauses game (ball not moving)
	def pause(self,status):
		# Loop refreshes to detect keystrokes
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				# on keystroke, if game is just paused, escape/directional keys will return to self.play(). Else, escape returns to self.play() then home.py/main menu
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return
					if event.key in [pygame.K_w,pygame.K_x,pygame.K_i,pygame.K_m] and status == 0:
						return
			# if status = 1 or 2, game is over and the opposite player won. Score and text displayed on screen
			if status == 1:
				msg = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),30).render("Player 2 Wins! Rally: " + str(self.score), True, (0,255,255))
				msgrect = msg.get_rect()
				msgrect = msgrect.move(msgrect.center[0], 0)
				self.screen.blit(msg, msgrect)
			elif status == 2:
				msg = pygame.font.Font(os.path.join(resource_path, 'Linebeam.ttf'),30).render("Player 1 Wins! Rally: " + str(self.score), True, (0,255,255))
				msgrect = msg.get_rect()
				msgrect = msgrect.move(msgrect.center[0], 0)
				self.screen.blit(msg, msgrect)
			pygame.display.flip()