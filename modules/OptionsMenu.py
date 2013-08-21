import pygame
from pygame.locals import *

from Constants import Constants

from FadeTransition import FadeTransition

from Menu import Menu
from LanguageMenu import LanguageMenu
from GW_Button import GW_Button
from GW_Label import GW_Label
from GW_TextInput import GW_TextInput
from GuiWidgetManager import GuiWidgetManager

from xml.sax import make_parser
from Localization import Localization

import os 

class OptionsMenu(Menu):
	"Options Menu"
	
	def __init__(self):
		"Sets up the options menu"
		
		Menu.__init__(self,"MoleFusion Options Menu","sprites/back1.jpg")
		
		self.parser = make_parser()
		self.curHandler = Localization()
		self.parser.setContentHandler(self.curHandler)
		self.parser.parse(open("languages/OptionsMenu_" + Constants.LANGUAGE + ".xml"))
	
		self.title = GW_Label(self.curHandler.getText("title"),(0.5,0.1),(27,22,24))
		
		self.name = GW_Label(self.curHandler.getText("name"),(0.5,0.2),(255,255,255))
		self.inputname = GW_TextInput((0.5,0.3),24,0.4,Constants.PLAYERNAME)
		
		self.language = GW_Button(self.curHandler.getText("language"),(0.5,0.5),(255,255,255))
		self.language.add_eventhandler("onmouseclick",self.language_onmouseclick)
						
		self.returnMain = GW_Button(self.curHandler.getText("returnMain"),(0.5,0.8),(255,255,255))
		self.returnMain.add_eventhandler("onmouseclick",self.returnMain_onmouseclick)
		
		self.widget_man = GuiWidgetManager([self.title,self.name,self.inputname,self.language,self.returnMain])
		
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
		f = FadeTransition(500,Constants.FADECOLOR,"to")
		del f
		Constants.PLAYTIME = pygame.mixer.music.get_pos()
		self.exit=True
		self.widget_man.set_draw(False)
		Constants.PLAYERNAME = self.inputname.get_Text()
		pygame.event.clear()
		
	def language_onmouseclick(self,event):
		self.language.onmouseclick(event)
		self.on_exit()
		l = LanguageMenu()
		l.run()
		self.language.onmouseclickup(event)
		self.reload_titles()		
		self.on_enter()
		pygame.mixer.music.play()
		
	def returnMain_onmouseclick(self,event):
		self.returnMain.onmouseclick(event)
		self.on_exit()
	
	def reload_titles(self):
		self.parser.parse(open("languages/OptionsMenu_" + Constants.LANGUAGE + ".xml"))
		self.name.set_title(self.curHandler.getText("name"))
		self.title.set_title(self.curHandler.getText("title"))
		self.language.set_title(self.curHandler.getText("language"))
		self.returnMain.set_title(self.curHandler.getText("returnMain"))	
				
	def run(self):
		while 1 and self.exit==False:
			self.time_speed.tick(Constants.FPS)
			for event in pygame.event.get():
				if event.type == QUIT:
					os._exit(0)

				elif event.type == KEYDOWN:
					if (not self.widget_man.has_input_focus()):
						if(event.key == K_ESCAPE):
							return
					else:
						pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
				else:
					pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
						
			self.widget_man.run()


			
		
		








