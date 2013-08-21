import pygame
from pygame.locals import *

from Constants import Constants

import os

class EventManager:
	"Event Manager system"

	def __init__(self,gamecontainer):
		"Sets up the event manager"
	
		self.gamecontainer=gamecontainer
		self.events = {}
	
	
	def add_event(self,object):
		self.events[id(object)]=object
	
	def remove_event(self,object): #Explicit deletion
		del self.events[id(object)]
		del object
	
	def run(self):
		
		if self.gamecontainer.timeclock.get_time()<=0:
			self.gamecontainer.gameover = True
			return
			
		for event in pygame.event.get():
			if event.type == QUIT:
				self.gamecontainer.timeclock.set_alive(False)
				os._exit(0)#self.gamecontainer.quit=True

			elif event.type == MOUSEBUTTONDOWN and event.button==1:
				if(self.gamecontainer.polygon.alive()):
						self.gamecontainer.polygon.reset()
				else:
						self.gamecontainer.polygon.set_alive(True)
						self.gamecontainer.polygon.reset()
																				
			elif event.type == KEYDOWN and event.key==K_ESCAPE and not self.gamecontainer.start:
				self.gamecontainer.gameover = True
				
			elif event.type == Constants.GAMETIME:
				self.gamecontainer.timeclock.change(-1)
				#self.gamecontainer.timeclock.set_time(self.gamecontainer.time_speed.get_fps())
			
			elif event.type == Constants.POLYADDTIME:
				if(self.gamecontainer.polygon.alive()):
					if(not self.gamecontainer.polygon.check_similarity()):
						self.gamecontainer.polygon.add_point([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]])
					
					self.gamecontainer.polygon.change_time(self.gamecontainer.polygon.get_linetime())
					if self.gamecontainer.polygon.get_time()>2000:
						self.gamecontainer.polygon.set_alive(False)
						self.gamecontainer.polygon.reset()
							
