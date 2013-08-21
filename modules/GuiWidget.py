import pygame
from pygame.locals import *

from Event import Event

class GuiWidget(pygame.sprite.Sprite):
	"Generic Gui Widget"

	def __init__(self):
		"Sets up the widget"
		pygame.sprite.Sprite.__init__(self)
		self.focus = 0
		self.mouse_over=0
		self.dirty = 1
		self.active = 1
		self.eventhandlers = {}
		
		self.eventhandlers['onmouseover']=self.onmouseover
		self.eventhandlers['onmouseout']=self.onmouseout
		self.eventhandlers['onfocus']=self.onfocus
		self.eventhandlers['onblur']=self.onblur

	def onmouseover(self,event):
		self.mouse_over=1
		
	def onmouseout(self,event):
		self.mouse_over=0
		
	def onfocus(self,event):
		self.focus=1
		
	def onblur(self,event):
		self.focus=0
		

	def add_eventhandler(self, name, function):
		self.eventhandlers[name]=function
	
	def remove_eventhandler(self, name):
		try:
			del self.eventhandlers[name]
			self.eventhandlers[name]=eval("self." + name) #Original object handlers, if any
		except KeyError: #handler not defined
			pass	
		
	def get_focus(self):
		return self.focus
	
	def get_mouse_over(self):
		return self.mouse_over
		
		
	def set_focus(self, val):
		self.focus = val
		
	def set_active(self, val):
		self.active = val
	
	def get_active(self):
		return self.active
	
	def notify(self, event):
		try:
			self.eventhandlers[event.get_name()](event.get_event())
		except KeyError: #handler not defined
			pass

	def set_screen_size(self, size):
		self.screen_size = size
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)		
	
		

