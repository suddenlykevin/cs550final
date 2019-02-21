"""
Snake

Functionality derived from tutorial:
https://pythonspot.com/snake-with-pygame/

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

class Player:
	def __init__(self):
		self.length = 10
		self.coords = [[(10-i)*20,0] for i in range(self.length)]
		self.speed = 20
		self.score = 0

	def move(self,direction):
		while len(self.coords)!=self.length:
			self.coords.append([0,0])
		self.score = (self.length-10)*10
		for i in range(self.length-1,0,-1):
			self.coords[i][0]=self.coords[i-1][0]
			self.coords[i][1]=self.coords[i-1][1]
		if direction<=1:
			self.coords[0][0] += self.speed*(-1)**direction
		else:
			self.coords[0][1] += self.speed*(-1)**direction

class Apple:
	def __init__(self):
		self.coords = [random.randrange(20,pygame.display.Info().current_w,20)-20,random.randrange(20,pygame.display.Info().current_h,20)-20]

	def reroll(self):
		self.coords = [random.randrange(20,pygame.display.Info().current_w,20)-20,random.randrange(20,pygame.display.Info().current_h,20)-20]

class Snake:
	def __init__(self, screen, cursor, BackGround):
		pygame.mouse.set_visible(0)
		self.screen = screen
		self.BackGround = BackGround
		self.appleSprite = cursor
		self.player = Player()
		self.apple = Apple()
		while self.apple.coords in self.player.coords:
			self.apple.reroll()
		self.playerSprite = BackGround.scrnMod(0)
		self.current = 0
	def play(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_l:
						if self.current!=1:
							self.current = 0
					elif event.key == pygame.K_a:
						if self.current!=0:
							self.current = 1
					elif event.key == pygame.K_m:
						if self.current!=3:
							self.current = 2
					elif event.key == pygame.K_w:
						if self.current!=2:
							self.current = 3
					elif event.key == pygame.K_ESCAPE:
						pygame.display.iconify()
						self.pause(0)
			self.player.move(self.current)
			if self.player.coords[0][0]>=pygame.display.Info().current_w:
				self.player.coords[0][0]=0
			elif self.player.coords[0][0]<0:
				self.player.coords[0][0]=pygame.display.Info().current_w-20
			if self.player.coords[0][1]>=pygame.display.Info().current_h:
				self.player.coords[0][1]=0
			elif self.player.coords[0][1]<0:
				self.player.coords[0][1]=pygame.display.Info().current_h-20
			if self.player.coords[0] in self.player.coords[1:-1]:
				self.pause(1)
				return
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			self.screen.blit(self.appleSprite,(self.apple.coords[0],self.apple.coords[1]))
			# https://stackoverflow.com/questions/32781858/pygame-blit-part-of-an-imagebackground-image
			for i in range(self.player.length):
				self.screen.blit(self.playerSprite,(self.player.coords[i][0],self.player.coords[i][1]),(self.player.coords[i][0],self.player.coords[i][1],20,20))
			if self.player.coords[0] == self.apple.coords:
				self.player.length+=2
				self.apple.reroll()
				while self.apple.coords in self.player.coords:
					self.apple.reroll()
			scoretext = pygame.font.Font(None,40).render(str(self.player.score), True, (0,255,255))
			scoretextrect = scoretext.get_rect()
			scoretextrect = scoretextrect.move(pygame.display.Info().current_w - scoretextrect.right, 0)
			self.screen.blit(scoretext, scoretextrect)
			pygame.display.flip()
	def pause(self, status):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return
					if event.key in [pygame.K_w,pygame.K_m,pygame.K_a,pygame.K_l] and status == 0:
						self.play()
			self.screen.blit(self.BackGround.image, self.BackGround.rect)
			for i in range(self.player.length):
				self.screen.blit(self.playerSprite,(self.player.coords[i][0],self.player.coords[i][1]),(self.player.coords[i][0],self.player.coords[i][1],20,20))
			if status == 1:
				msg = pygame.font.Font(None,70).render("Game Over! Score: " + str(self.player.score), True, (0,255,255))
				self.screen.blit(self.BackGround.image, self.BackGround.rect)
				msgrect = msg.get_rect()
				msgrect = msgrect.move(pygame.display.Info().current_w / 2 - (msgrect.center[0]), pygame.display.Info().current_h / 3)
				self.screen.blit(msg, msgrect)
			pygame.display.flip()
