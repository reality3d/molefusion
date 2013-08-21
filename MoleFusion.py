import sys
import os

sys.path.append("modules")

from LanguageMenu import LanguageMenu
from MainMenu import MainMenu

import pygame
from pygame.locals import *

from xml.sax import make_parser
from Configuration import *
from Constants import Constants

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
