import pygame
from pygame.locals import *

from GuiWidget import GuiWidget

import os

from Constants import Constants

class GW_Label(GuiWidget):
	"Label type Widget"

	def __init__(self, title , pos , color):
		"Sets up the label widget"

		GuiWidget.__init__(self)
		        
		self.screen_size=Constants.SCREEN.get_size()
		self.font = pygame.font.Font(os.path.join("fonts","freesansbold.ttf"), 24)
		self.title = title
		self.color = color
		self.image = self.font.render(self.title, 1, color)
		self.rect  = self.image.get_rect()
		
		self.rect  = self.image.get_rect()
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)

	
	def update(self):
		if not self.dirty:
			return

		self.image = self.font.render( self.title, 1, self.color )
		self.rect  = self.image.get_rect()		
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.dirty = 0
	
	def set_title(self, title):
		self.title = title

		self.dirty = 1
	
	def set_pos(self, pos):
		self.rect.center = (self.screen_size[0]*pos[0],self.screen_size[1]*pos[1])
		
		
	def get_rect(self):
		return self.rect




