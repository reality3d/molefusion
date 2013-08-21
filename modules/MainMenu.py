import pygame
from pygame.locals import *

from Constants import Constants

from FadeTransition import FadeTransition

from Menu import Menu
from OptionsMenu import OptionsMenu
from HighScoresMenu import HighScoresMenu
from ExitMenu import ExitMenu
from HelpMenu import HelpMenu
from GW_Button import GW_Button
from GW_Label import GW_Label
from GuiWidgetManager import GuiWidgetManager

from Game import Game

from xml.sax import make_parser
from Localization import Localization

import os 

class MainMenu(Menu):
	"Main Menu"
	
	def __init__(self):
		"Sets up the menu"
		
		Menu.__init__(self,"MoleFusion Main Menu","sprites/back1.jpg")
		
		self.parser = make_parser()
		self.curHandler = Localization()
		self.parser.setContentHandler(self.curHandler)
		self.parser.parse(open("languages/MainMenu_" + Constants.LANGUAGE + ".xml"))
	
		self.title = GW_Label(self.curHandler.getText("title"),(0.5,0.1),(27,22,24))
		
		self.start = GW_Button(self.curHandler.getText("start"),(0.5,0.3),(255,255,255))
		self.start.add_eventhandler("onmouseclick",self.start_onmouseclick)
		
		self.options = GW_Button(self.curHandler.getText("options"),(0.5,0.45),(255,255,255))
		self.options.add_eventhandler("onmouseclick",self.options_onmouseclick)
		
		self.highscores = GW_Button(self.curHandler.getText("highscores"),(0.5,0.6),(255,255,255))
		self.highscores.add_eventhandler("onmouseclick",self.highscores_onmouseclick)
		
		
		self.help = GW_Button(self.curHandler.getText("help"),(0.5,0.75),(255,255,255))
		self.help.add_eventhandler("onmouseclick",self.help_onmouseclick)
				
		self.quit = GW_Button(self.curHandler.getText("quit"),(0.5,0.9),(255,255,255))
		self.quit.add_eventhandler("onmouseclick",self.quit_onmouseclick)
		
		self.widget_man = GuiWidgetManager([self.title,self.start,self.options,self.highscores,self.help,self.quit])
		
		self.time_speed=pygame.time.Clock()		
		
		self.on_enter()

	def on_enter(self):
		pygame.event.clear()		
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
		
		self.widget_man.set_draw(True)
		
	def on_exit(self):
		pygame.event.clear()
		f = FadeTransition(500,Constants.FADECOLOR,"to")
		del f
		self.widget_man.set_draw(False)
		
	def start_onmouseclick(self,event):
		self.start.onmouseclick(event)
		self.on_exit()
		game = Game()
		game.run()
		self.start.onmouseclickup(event)
		self.on_enter()

	def options_onmouseclick(self,event):
		self.options.onmouseclick(event)
		self.on_exit()
		options = OptionsMenu()
		options.run()
		self.reload_titles()
		self.options.onmouseclickup(event)
		self.on_enter()
		
	def highscores_onmouseclick(self,event):
		self.highscores.onmouseclick(event)
		self.on_exit()
		highscores = HighScoresMenu("sprites/back1.jpg")
		highscores.run()
		self.reload_titles()
		self.highscores.onmouseclickup(event)
		self.on_enter()
	

	def help_onmouseclick(self,event):
		self.help.onmouseclick(event)
		self.on_exit()
		help = HelpMenu()
		help.run()
		self.help.onmouseclickup(event)
		self.reload_titles()
		self.on_enter()
		
	def quit_onmouseclick(self,event):
		self.quit.onmouseclick(event)
		self.on_exit()
		exit=ExitMenu()
		exit.run()
		pygame.event.post(pygame.event.Event(QUIT,{}))
		
	def reload_titles(self):
		self.parser.parse(open("languages/MainMenu_" + Constants.LANGUAGE + ".xml"))
		self.title.set_title(self.curHandler.getText("title"))
		self.start.set_title(self.curHandler.getText("start"))
		self.options.set_title(self.curHandler.getText("options"))
		self.highscores.set_title(self.curHandler.getText("highscores"))
		self.help.set_title(self.curHandler.getText("help"))
		self.quit.set_title(self.curHandler.getText("quit"))
		
				
	def run(self):
		while 1:
			
			self.time_speed.tick(Constants.FPS)
			
			for event in pygame.event.get():
				if event.type == QUIT:
					os._exit(0)

				elif event.type == KEYDOWN and event.key==K_ESCAPE:
					self.quit_onmouseclick(event)
				
				else:
					pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
						
			self.widget_man.run()


			
		
		








