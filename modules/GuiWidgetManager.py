import pygame
from pygame.locals import *

from GW_TextInput import GW_TextInput
from Event import Event

from Constants import Constants

class GuiWidgetManager:
	"Widget Manager Container"

	def __init__(self , widgetlist):
		"Sets up the widget Manager"
		
		self.background=Constants.BACKGROUND
		self.screen=Constants.SCREEN
		self.widgets = pygame.sprite.RenderUpdates() #RenderUpdates Sprite Group type
		self.widgetlist = widgetlist   #internal list for indexable access
		for widget in widgetlist:
			self.widgets.add(widget)
		self.currentfocus=-1 #by default no widgets focused
		self.draw=True
	
	def set_draw(self,value):
		self.draw=value
	
	def get_widgets(self):
		return self.widgets
	
	def has_input_focus(self):
		return isinstance(self.currentfocus,GW_TextInput)
	
	def run(self):
		for event in pygame.event.get():		#Process events
			if event.type == MOUSEMOTION:	
				for widget in self.widgetlist:
					if(widget.get_active()):	#Is active or disabled?
						if(widget.get_rect().collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])):
							if(not widget.get_mouse_over()):	#Was already mouse over it?
								widget.notify(Event("onmouseover",event))
								#print "onmouseover"
					
						elif widget.get_mouse_over(): #Widget was mouseover and mouse has gone out
							widget.notify(Event("onmouseout",event))
							#print "onmouseout"
				
			elif event.type == MOUSEBUTTONDOWN and event.button==1: #Left Mouse click
				for widget in self.widgetlist:
					if(widget.get_active()):
						if(widget.get_rect().collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])):
							widget.notify(Event("onmouseclick",event))
							#print "onmouseclick"							
							if(not widget.get_focus()):
								widget.notify(Event("onfocus",event))
								self.currentfocus=widget
								#print "onfocus"							
					
						elif widget.get_focus():
							widget.notify(Event("onblur",event))
							if(widget==self.currentfocus):#We could have put the focus already on another widget!
								self.currentfocus=-1
							#print "onblur"
			
			elif event.type == MOUSEBUTTONUP and event.button==1:
				for widget in self.widgetlist:
					if(widget.get_active()):
						if(widget.get_rect().collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])):
							widget.notify(Event("onmouseclickup",event))
			
			elif event.type == KEYDOWN:	
				if(self.currentfocus!=-1):
					if(self.currentfocus.get_active()):
						if(isinstance(self.currentfocus,GW_TextInput)):
							if(event.key!=K_ESCAPE and event.key!=K_RETURN):
								self.currentfocus.notify(Event("onkeydown",event))
							else:
								self.currentfocus.notify(Event("onblur",event))
								self.currentfocus=-1
			else:
				pygame.event.post(event) #Reinject the event into the queue for maybe latter process
			
		if self.draw==True:					
			self.widgets.clear(self.screen,self.background)
			self.widgets.update()
			self.rectlist = self.widgets.draw(self.screen)
			pygame.display.update(self.rectlist)




