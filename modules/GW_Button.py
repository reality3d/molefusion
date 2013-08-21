import pygame
from pygame.locals import *

from GuiWidget import GuiWidget

from Constants import Constants

import os

class GW_Button(GuiWidget):
	"Button type Widget"

	def __init__(self, title , pos, color):
		"Sets up the button widget"

		GuiWidget.__init__(self)
		self.screen_size=Constants.SCREEN.get_size()	        
		self.font = pygame.font.Font(os.path.join("fonts","freesansbold.ttf"), 24)
		self.title = title
		self.color = color
		self.color_normal = color
		self.color_hover = (255,255,0)
		self.image = self.font.render(self.title, 1, (255, 255, 255))
		self.rect  = self.image.get_rect()
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.eventhandlers['onmouseclick']=self.onmouseclick
		self.eventhandlers['onmouseclickup']=self.onmouseclickup
		
	def onmouseover(self,event):
		self.mouse_over=1
		self.color=self.color_hover
		self.dirty=1

	def onmouseout(self,event):
		self.mouse_over=0
		self.color=self.color_normal
		self.dirty=1

	def onmouseclick(self,event):
		self.color=(255,0,0)
		self.dirty=1

	def onmouseclickup(self,event):
		self.color=self.color_normal
		self.dirty=1
						
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




