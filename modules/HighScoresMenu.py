import pygame
from pygame.locals import *

from Constants import Constants

from FadeTransition import FadeTransition

from Menu import Menu
from GW_Label import GW_Label
from GW_Button import GW_Button
from GuiWidgetManager import GuiWidgetManager

from HighScores import *

from xml.sax import make_parser
from Localization import Localization

import os 

class HighScoresMenu(Menu):
	"HighScores Menu"
	
	def __init__(self,background):
		"Set up the HighScores menu"
		
		Menu.__init__(self,"MoleFusion HighScore Menu",background)
		
		self.parser = make_parser()
		self.curHandler = Localization()
		self.parser.setContentHandler(self.curHandler)
		self.parser.parse(open("languages/HighScoresMenu_" + Constants.LANGUAGE + ".xml"))
	
		self.title = GW_Label(self.curHandler.getText("title"),(0.5,0.1),(27,22,24))
		
		self.name_column = GW_Label(self.curHandler.getText("name"),(0.25,0.25),(212,224,130))
		self.points_column = GW_Label(self.curHandler.getText("points"),(0.75,0.25),(212,224,130))
		
		self.returnMain = GW_Button(self.curHandler.getText("returnMain"),(0.5,0.9),(255,255,255))
		self.returnMain.add_eventhandler("onmouseclick",self.returnMain_onmouseclick)
		
		h = HighScores()
		highscorelist = h.get_HighScores()

		self.widgetlist = [self.title,self.name_column,self.points_column,self.returnMain]
		
		for val,i in enumerate(highscorelist[0:5]):
			self.widgetlist.append(GW_Label(i.get_name(),(0.25,0.35+val/10.0),(250,254,210)))
			self.widgetlist.append(GW_Label(str(i.get_points()),(0.75,0.35+val/10.0),(250,254,210)))
				
		self.widget_man = GuiWidgetManager(self.widgetlist)
		
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
		f = FadeTransition(500,Constants.FADECOLOR,"to")
		del f
		self.exit=True
		self.widget_man.set_draw(False)
		
	def returnMain_onmouseclick(self,event):
		self.returnMain.onmouseclick(event)
		self.on_exit()
				
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
					#else:
					#	pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
				else:
					pygame.event.post(event) #Reinject the event into the queue for maybe latter process	
						
			self.widget_man.run()

			
		
		








