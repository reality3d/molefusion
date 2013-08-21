import pygame
from pygame.locals import *

from Constants import Constants

from FadeTransition import FadeTransition

from Menu import Menu
from GW_Label import GW_Label
from GuiWidgetManager import GuiWidgetManager

from xml.sax import make_parser
from Localization import Localization

import os 

class ExitMenu(Menu):
	"Exit Menu"
	
	def __init__(self):
		"Set up the Exit menu"
		
		Menu.__init__(self,"MoleFusion Exit Menu","sprites/back1.jpg")
		
		self.parser = make_parser()
		self.curHandler = Localization()
		self.parser.setContentHandler(self.curHandler)
		self.parser.parse(open("languages/ExitMenu_" + Constants.LANGUAGE + ".xml"))
	
		self.title = GW_Label(self.curHandler.getText("title"),(0.5,0.1),(27,22,24))
		
		self.game_by = GW_Label(self.curHandler.getText("game"),(0.5,0.3),(240,255,220))
		self.music_by = GW_Label(self.curHandler.getText("music"),(0.5,0.5),(240,255,220))
		self.web = GW_Label(self.curHandler.getText("web"),(0.5,0.7),(255,255,255))
						
		self.widget_man = GuiWidgetManager([self.title,self.game_by,self.music_by,self.web])
		
		self.time_speed=pygame.time.Clock()
		self.exit=False
		self.on_enter()

	def on_enter(self):
		pygame.event.clear()		
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
		self.exit=False
		self.widget_man.set_draw(True)
	
	def on_exit(self):
		pygame.event.clear()
		f = FadeTransition(2000,Constants.FADECOLOR,"to")
		del f
		self.exit=True
		self.widget_man.set_draw(False)

				
	def run(self):
		while 1 and self.exit==False:
			self.time_speed.tick(Constants.FPS)
			for event in pygame.event.get():
				if event.type == QUIT:
					self.on_exit()
				elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					self.on_exit()
				else:
					pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
						
			self.widget_man.run()


			
		
		








