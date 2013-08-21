import pygame
from pygame.locals import *

from Constants import Constants

class FadeTransition:
	"Transition to black and From Black"
	
	def __init__(self,max_time,color,type="to"):
		"Sets up the Fade"
				
		self.type=type
		self.max_time=max_time
		self.time_speed=pygame.time.Clock()
		self.time=0
		self.screen = Constants.SCREEN
		self.screen_original = self.screen.copy()
		self.black=pygame.Surface(self.screen.get_size(),SRCALPHA)
		self.black.convert_alpha()
		self.black.fill(color)
		self.run()

		
	def run(self):
		"run loop"
		
		while self.time<self.max_time:
			self.time_speed.tick(Constants.FPS)
			self.time+=self.time_speed.get_time()
			if self.type=="to":
				self.black.set_alpha((float(self.time)/self.max_time)*255)
			elif self.type=="from":
				self.black.set_alpha(255-(float(self.time)/self.max_time)*255)
			self.screen.blit(self.screen_original,(0,0))
			self.screen.blit(self.black,(0,0))
			pygame.display.update()

		pygame.event.clear()


