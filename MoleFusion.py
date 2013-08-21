import os

from modules.LanguageMenu import LanguageMenu
from modules.MainMenu import MainMenu

import pygame
from pygame.locals import *

from xml.sax import make_parser
from modules.Configuration import *
from modules.Constants import Constants

if __name__=="__main__":

	parser = make_parser()
	curHandler = Configuration()
	parser.setContentHandler(curHandler)
	parser.parse(open("config/config.xml"))
	
	pygame.init()
	Constants.SCREEN=pygame.display.set_mode(curHandler.getRes())
	pygame.display.set_caption(curHandler.getName())  
	pygame.mouse.set_visible(curHandler.getMouseVisibility())
	pygame.mixer.init()
	
	l = LanguageMenu()
	l.run()
	m = MainMenu()
	m.run()
