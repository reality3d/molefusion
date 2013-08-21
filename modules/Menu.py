import pygame
from pygame.locals import *

from Constants import Constants

class Menu:
	"Base user menu"
	
	def __init__(self, title, background):
		"Sets up the menu"
		
		
		
		self.screen = Constants.SCREEN
		self.title = title
		self.background=pygame.image.load(background)
		Constants.BACKGROUND=self.background
		self.background.convert() #for blitting more faster

	def run(self):
		"run loop"
	
	def on_enter(self):
		pass
	
	def on_exit(self):
		pass



