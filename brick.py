
""" 
Code based on Breakout V 0.1 June 2009 by John Cheetham. Can be found at http://www.johncheetham.com/projects/breakout. 

Sources for screenshot capture: 
https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
https://stackoverflow.com/questions/25202092/pil-and-pygame-image 
http://www.varesano.net/blog/fabio/capturing%20screen%20image%20python%20and%20pil%20windows
"""

import sys, pygame, random,time, os
from PIL import Image, ImageGrab

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

class Breakout():
   
	def main(self, screen, cursor, BackGround,mac): #Set some inital constants 
		xspeed_init = 15
		yspeed_init = 15
		max_lives = 5
		bat_speed = 30
		score = 0 

		infosize = pygame.display.Info() #info to make the display the correct size 
		size = width, height = int(infosize.current_w), int(infosize.current_h)

		bat = pygame.image.load(os.path.join(image_path, 'editbat.png')).convert_alpha() #loading and scalling the bat 
		bat = pygame.transform.scale(bat, (int(infosize.current_w*0.1),int(infosize.current_h*0.05)))
		batrect = bat.get_rect()

		ball = cursor #the "ball" is the cursor determined in the home function and is different for different operating systems
		ball.set_colorkey((255, 255, 255))
		
		ballrect = ball.get_rect()

		wall = Wall()
		wall.build_wall(width)

		# Initialise ready for game loop
		batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
		ballrect = ballrect.move(width / 2, height / 2)       
		xspeed = xspeed_init
		yspeed = yspeed_init
		lives = max_lives
		clock = pygame.time.Clock()
		pygame.key.set_repeat(1,30)       
		pygame.mouse.set_visible(0)       # turn off mouse pointer

		while 1:

			# 60 frames per second
			clock.tick(60)

			# process key presses
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					if event.key == pygame.K_LEFT:                        
						batrect = batrect.move(-bat_speed, 0)     
						if (batrect.left < 0):                           
							batrect.left = 0      
					if event.key == pygame.K_RIGHT:                    
						batrect = batrect.move(bat_speed, 0)
						if (batrect.right > width):                            
							batrect.right = width

			# check if bat has hit ball    
			if ballrect.bottom >= batrect.top and \
			   ballrect.bottom <= batrect.bottom and \
			   ballrect.right >= batrect.left and \
			   ballrect.left <= batrect.right:
				yspeed = -yspeed                          
				offset = ballrect.center[0] - batrect.center[0]                          
				# offset > 0 means ball has hit RHS of bat                   
				# vary angle of ball depending on where ball hits bat                      
				if offset > 0:
					if offset > 30:  
						xspeed = 7
					elif offset > 23:                 
						xspeed = 6
					elif offset > 17:
						xspeed = 5 
				else:  
					if offset < -30:                             
						xspeed = -7
					elif offset < -23:
						xspeed = -6
					elif xspeed < -17:
						xspeed = -5     
					  
			# move bat/ball
			ballrect = ballrect.move(xspeed, yspeed)
			if ballrect.left < 0 or ballrect.right > width:
				xspeed = -xspeed                
					
			if ballrect.top < 0:
				yspeed = -yspeed                
							

			# check if ball has gone past bat - lose a life
			if ballrect.top > height:
				lives -= 1
				# start a new ball
				xspeed = xspeed_init
				rand = random.random()                
				if rand > 0.5:
					xspeed = -xspeed 
				yspeed = yspeed_init  
						 
				ballrect.center = width * random.random(), height / 3   

				#prcesses losing 
				if lives == 0:                    
					msg = pygame.font.Font(None,50).render("Game Over! Score: " + str(score), True, (0,255,255))
					screen.blit(BackGround.image, BackGround.rect)
					msgrect = msg.get_rect()
					msgrect = msgrect.move((msgrect.center[0]), 0)
					screen.blit(msg, msgrect)
					pygame.display.flip()
					# process key presses
					#     - ESC to quit
					#     - any other key to restart game
					#Restarts game
					while 1:
						restart = False
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								sys.exit()
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_ESCAPE:
									return
								if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
									restart = True      
						if restart:                   
							screen.blit(BackGround.image, BackGround.rect)
							wall.build_wall(width)
							lives = max_lives
							score = 0
							break
			
			#allows for bouncing off sides of the screen
			if xspeed < 0 and ballrect.left < 0:
				xspeed = -xspeed                                
			

			if xspeed > 0 and ballrect.right > width:
				xspeed = -xspeed                               
			
		   
			# check if ball has hit wall
			# if yes yhen delete brick and change ball direction
			index = ballrect.collidelist(wall.brickrect)       
			if index != -1: 
				if ballrect.center[0] > wall.brickrect[index].right or \
				   ballrect.center[0] < wall.brickrect[index].left:
					xspeed = -xspeed
				else:
					yspeed = -yspeed                
						 
				wall.brickrect[index:index + 1] = []
				score += 10
			#continue to blit the background image (screenshot)	and the score text 
			screen.blit(BackGround.image, BackGround.rect)
			scoretext = pygame.font.Font(None,40).render(str(score), True, (0,255,255))
			scoretextrect = scoretext.get_rect()
			scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
			screen.blit(scoretext, scoretextrect)


 			#Blit for wall 
			for i in range(0, len(wall.brickrect)):
				screen.blit(wall.brick, wall.brickrect[i])    

			# if wall completely gone then rebuild it
			if wall.brickrect == []:              
				wall.build_wall(width)                
				xspeed = xspeed_init
				yspeed = yspeed_init                
				ballrect.center = width / 2, height / 3
		 	
		 	#blit for bat and ball 
			screen.blit(ball, ballrect)
			screen.blit(bat, batrect)
			pygame.display.flip()

class Wall():

		#creating each brick and determining brick length 
	def __init__(self):
		self.brick = pygame.image.load(os.path.join(image_path, 'editbrick.png')).convert_alpha()
		brickrect = self.brick.get_rect()
		self.bricklength = brickrect.right - brickrect.left       
		self.brickheight = brickrect.bottom - brickrect.top             

	def build_wall(self, width):        
		xpos = 0 					
		ypos = 60
		adj = 0
		self.brickrect = []
		for i in range (0, int(2*width/self.bricklength)):   #creating the wall scaled to screen size         
			if xpos > width:
				if adj == 0:
					adj = self.bricklength / 2
				else:
					adj = 0
				xpos = -adj
				ypos += self.brickheight
				
			self.brickrect.append(self.brick.get_rect())    
			self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
			xpos = xpos + self.bricklength