import pygame
from pygame.locals import *

from GuiWidget import GuiWidget

import string
import os

from Constants import Constants

class GW_TextInput(GuiWidget):
	"Text input box type Widget"

	def __init__(self, pos , fontsize, width, defaultName="DEFAULT"):
		"Sets up the text input box type widget"

		GuiWidget.__init__(self)
		
		self.set_click_state=0
		
		self.font = pygame.font.Font(os.path.join("fonts","freesansbold.ttf"), fontsize)
		self.linesize = self.font.get_linesize()

		self.screen_size=Constants.SCREEN.get_size() # self.background.get_size()		        
		self.x = pos[0]
		self.y = pos[1]

		self.rect = pygame.Rect( (0,0,width*self.screen_size[0], self.linesize +4) )
		self.boxImg = pygame.Surface( self.rect.size ).convert_alpha()
		self.boxImg.fill((128,128,128))
		self.color = (255,255,255)
		pygame.draw.rect( self.boxImg, self.color, self.rect, 2 )

		self.emptyImg = self.boxImg.convert_alpha()
		self.image = self.boxImg

		self.text = defaultName
		self.textPos = (5, 0)
		self.textColor = (255,255,255)
		self.textColor_clicked = (255,255,0)
		self.textImg = self.font.render( self.text, 1, self.textColor )
		self.image.blit( self.emptyImg, (0,0) )
		self.image.blit( self.textImg, self.textPos )		
				        

		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.flick_time=500
		
		self.eventhandlers['onkeydown']=self.onkeydown

	def onfocus(self,event):
		self.set_focus(1)
		self.set_click_state=1
		self.dirty = 1
		self.flick = True
		self.flicker=pygame.time.get_ticks() # Controls the flicking bar				
	
	def onblur(self,event):
		self.set_focus(0)
		self.set_click_state=0
		self.flick = False
		self.dirty = 1
	
	def onkeydown(self,event):
		
		if event.key == K_BACKSPACE:
			self.text = self.text[:-1]
		elif event.key == K_SPACE:
			self.text += " "
		elif event.key == K_RSHIFT or event.key == K_LSHIFT or event.key == K_CAPSLOCK or event.key == K_TAB or event.key == K_RCTRL or event.key == K_LCTRL:
			pass		
		else:
			self.text += string.upper(pygame.key.name(event.key))
		self.dirty = 1
				
	def update(self):

		temptext = self.text			
		if self.get_focus():
			if((pygame.time.get_ticks() - self.flicker) > self.flick_time): # Controls the flicking bar
				if(self.flick):
					temptext = self.text + '|'					
				else:
					temptext = self.text					
					
				self.flick=not self.flick
				self.flicker=pygame.time.get_ticks()
				self.dirty = 1					

		if not self.dirty:
			return
				
		self.textImg = self.font.render( temptext, 1, self.textColor )		
		self.image.blit( self.emptyImg, (0,0) )
		self.image.blit( self.textImg, self.textPos )	
		self.dirty = 0

	def get_Text(self):
		return self.text
		
	def set_Text(self, newText):
		self.text = newText
		self.dirty = 1		
	
	def get_click_state(self):
		return self.set_click_state
	
	def set_pos(self, pos):
		self.rect.center = (self.screen_size[0]*pos[0],self.screen_size[1]*pos[1])
		

	def get_rect(self):
		return self.rect




