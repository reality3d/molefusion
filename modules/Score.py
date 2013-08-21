import pygame
from pygame.locals import *

from Constants import Constants

import os
class Score(pygame.sprite.Sprite):
	"Control the score of the game"

	def __init__(self, pos, value):
		"Sets up the score"

		pygame.sprite.Sprite.__init__(self)
		
		self.screen_size=Constants.SCREEN.get_size()	        
		self.font = pygame.font.Font(os.path.join("fonts","freesansbold.ttf"), 20)
		self.color = (255,255,0)
		
		self.score = value
		self.image = self.font.render(str(self.score), 1, (211, 225, 228))
		self.rect  = self.image.get_rect()
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.active = True
		self.dirty = 0
	
	def change(self,value):
		self.score += value
		self.dirty = 1
				
	def alive(self):
		return self.active
	
	def set_alive(self,value):
		self.active= value
	
	def get_score(self):
		return self.score

	def set_score(self,value):
		self.score=value
		
	def update(self):
		if not self.dirty:
			return
		
		self.image = self.font.render(str(self.score), 1, (211, 225, 228))
		self.dirty=0
		
						
