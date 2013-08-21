import pygame
from pygame.locals import *

from GuiWidget import GuiWidget

import os

from Constants import Constants

class GW_Image(GuiWidget):
	"Image type Widget"

	def __init__(self, file , pos):
		"Sets up the image widget"

		GuiWidget.__init__(self)
		        
		self.screen_size=Constants.SCREEN.get_size()
		
		self.image=pygame.image.load(file)
		self.image.convert() #for blitting more faster
		
		self.rect  = self.image.get_rect()
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)

	
	def update(self):
		if not self.dirty:
			return
		"""	
		if(self.get_focus()):
			self.image = self.font.render( self.title, 1, (255, 255, 0) )
		else:
			self.image = self.font.render( self.title, 1, (255, 255, 255) )"""
		
		self.dirty = 0

	def set_pos(self, pos):
		self.rect.center = (self.screen_size[0]*pos[0],self.screen_size[1]*pos[1])
		

	def get_rect(self):
		return self.rect




