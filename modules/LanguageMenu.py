import pygame
from pygame.locals import *

from Constants import Constants

from FadeTransition import FadeTransition

from Menu import Menu
from GW_Image import GW_Image
from GW_Label import GW_Label
from GuiWidgetManager import GuiWidgetManager

from Game import Game

import os
import sys

class LanguageMenu(Menu):
	"Language Menu"
	
	def __init__(self):
		"Sets up the Language menu"
		
		Menu.__init__(self,"Language Main Menu","sprites/back1.jpg")

		self.title = GW_Label("Choose Language",(0.5,0.15),(27,22,24))
		
		self.english = GW_Image("sprites/language_engl.png",(0.25,0.35))
		self.english.add_eventhandler("onmouseclick",self.english_onmouseclick)

		self.spanish= GW_Image("sprites/language_espn.png",(0.5,0.35))
		self.spanish.add_eventhandler("onmouseclick",self.spanish_onmouseclick)
		
		self.euskera = GW_Image("sprites/language_eusk.png",(0.75,0.35))
		self.euskera.add_eventhandler("onmouseclick",self.euskera_onmouseclick)

		self.widget_man = GuiWidgetManager([self.title,self.english,self.spanish,self.euskera])
		
		self.time_speed=pygame.time.Clock()
		self.exit=False
		
		self.on_enter()

	def on_enter(self):
		
		self.screen.blit(self.background, (0, 0))	
		pygame.display.flip()
		
		pygame.mixer.music.load(Constants.MENUMUSIC)
		pygame.mixer.music.play(-1)
		self.widget_man.set_draw(True)
		
	def on_exit(self):
		f = FadeTransition(500,Constants.FADECOLOR,"to")
		del f
		self.exit=True
		self.widget_man.set_draw(False)
		pygame.event.clear()
		
	def english_onmouseclick(self,event):
		Constants.LANGUAGE="en"
		self.on_exit()

	def spanish_onmouseclick(self,event):
		Constants.LANGUAGE="es"
		self.on_exit()

	def euskera_onmouseclick(self,event):
		Constants.LANGUAGE="eu"
		self.on_exit()			
				
	def run(self):
		while 1 and self.exit==False:
			for event in pygame.event.get():
				if event.type == QUIT:
					os._exit(0)
										
				else:
					pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
						
			self.widget_man.run()
			self.time_speed.tick(60)
			
		
		








