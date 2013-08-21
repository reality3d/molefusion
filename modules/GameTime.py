import pygame
from pygame.locals import *

from Constants import Constants

import os

class GameTime(pygame.sprite.Sprite):
	"Control the time of the game"

	def __init__(self, pos, time):
		"Sets up the timer"

		pygame.sprite.Sprite.__init__(self)
		
		self.screen_size=Constants.SCREEN.get_size()	        
		self.font = pygame.font.Font(os.path.join("fonts","freesansbold.ttf"), 20)
		self.color = (255,255,0)
		
		self.GameTimeEvent=pygame.event.Event(Constants.GAMETIME, {})
		pygame.time.set_timer(Constants.GAMETIME, 1000)
		
		self.time = time
		self.image = self.font.render(str(self.time), 1, (211, 225, 228))
		self.rect  = self.image.get_rect()
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.active = True
		self.dirty = 0
		
	def __del__(self):
		pygame.time.set_timer(Constants.GAMETIME, 0)
		
	def add_timer(self):
		pygame.time.set_timer(Constants.GAMETIME, 1000)
		
	def delete_timer(self):
		pygame.time.set_timer(Constants.GAMETIME, 0)
	
	def change(self,value):
		self.time += value
		self.dirty = 1
				
	def alive(self):
		return self.active
	
	def set_alive(self,value):
		self.active= value
	
	def get_time(self):
		return self.time
	
	def set_time(self,value):
		self.time=value
		self.dirty = 1
		
	def update(self):
		if not self.dirty:
			return
		
		self.image = self.font.render(str(self.time), 1, (211, 225, 228))
		self.dirty=0
		
						
