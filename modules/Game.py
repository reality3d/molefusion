import pygame
from pygame.locals import *

from EventManager import EventManager

from Constants import Constants
from GameTime import GameTime
from Score import Score
from Polygon import Polygon
from Atom import Atom
from random import *
from Levels import *

import os

class Game:
	"The totality of existence"

	def __init__(self):
		"Initialises resources"
		
		self.exit=False
		self.score = Score((0.9,0.05),0)
		self.levels=["Level_1(self.score)","Level_2(self.score)","Level_3(self.score)"]
		
	def on_enter(self):
		pass
	
	def on_exit(self):
		pass
	
	def run(self):
		"Executes the levels"		
		for i in self.levels:
			l = eval(i)
			if(l.run() == False): #Game has finished
				break

				

		
		



