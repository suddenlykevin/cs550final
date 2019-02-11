import pygame
from PIL import Image, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance
import sys

pygame.init()
size = width, height = 320,240
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
red = 255,0,0

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				screen.fill(red)
	pygame.display.flip()
