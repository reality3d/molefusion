import pygame
from pygame.locals import *

from EventManager import EventManager

from Constants import Constants
from GameTime import GameTime
from Score import Score
from Polygon import Polygon
from Atom import Atom
from random import *
from HighScores import *
from HighScoresMenu import HighScoresMenu
from FadeTransition import FadeTransition

from Math_Funcs import *

import os

from xml.sax import make_parser
from Localization import Localization

class Level:
	"Level Base class"

	def __init__(self,score,time):
		"Initialises resources and start level"
		
		self.background=pygame.image.load("sprites/sky.jpg")
		self.background.convert() #for blitting more faster
		
		self.screen=Constants.SCREEN
		self.score = score
		self.display_items = pygame.sprite.Group()
		self.timeclock = GameTime((0.05,0.05),time)		
		self.display_items.add(self.timeclock,self.score)
		
		self.time_speed=pygame.time.Clock()
		self.time=0.0
		
		self.quit = False
		self.pause = False
		self.start = False
		self.completed = False
		self.gameover = False
		self.message = None
		
		self.polygon=Polygon(self)
		self.event_manager = EventManager(self)
		self.on_enter()

	def get_score_object(self):
		return self.score
	
	def set_score_object(self, score_object):
		self.score = score_object
	
	def on_enter(self):
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
		self.start = True
		self.pause = True
		self.timeclock.delete_timer()
		self.message = MessageBox(self,3000)
		self.display_items.add(self.message)


		
	def on_exit(self):
		self.display_items.remove(self.timeclock)
		del self.polygon
		del self.timeclock
		if self.completed == False: #end of game, so music fadeout
			pygame.mixer.music.fadeout(500)
		f = FadeTransition(500,Constants.FADECOLOR,"to")
		del f
		
	
	def run(self):
		
		while 1:
			
			self.time+=self.time_speed.tick(Constants.FPS)
			
			if self.gameover and (not self.pause):				
				self.pause = True
				self.polygon.reset()
				self.timeclock.delete_timer()
				self.message = MessageBox(self,4000)
				self.display_items.add(self.message)
			
			if self.completed and (not self.pause):
				self.pause = True
				self.polygon.reset()
				self.timeclock.delete_timer()
				self.message = MessageBox(self,4000)
				self.display_items.add(self.message)
				self.polygon.set_alive(False)
				self.polygon.reset()
			
			if self.quit:
				self.on_exit()
				if self.gameover == True:
					h = HighScores()
					h.insert_HighScores(Constants.PLAYERNAME,str(self.score.get_score()))
					hlist = HighScores().get_HighScores()
					if len(hlist)<5 or self.score.get_score() > hlist[4].get_points():
						h.flush()
					pygame.event.clear()
					highscores = HighScoresMenu("sprites/sky.jpg")
					highscores.run()
					return False
				else:
					return
			
			
			self.event_manager.run()
			self.screen.blit(self.background, (0, 0))
			self.display_items.update()			
			self.display_items.draw(self.screen)
			self.atoms.update()			
			self.atoms.draw(self.screen)
			
			if self.start == True  and self.pause == False:
				self.display_items.remove(self.message)
				self.message = None
				self.start = False
				self.polygon.set_alive(False)
				self.polygon.reset()
				self.timeclock.add_timer()
				
			if not self.pause:
				self.polygon.draw()					
			pygame.display.flip()
			


class Level_1(Level):
	"Level_1"

	def __init__(self,score):
		"Initialises resources and start level"
		
		self.atoms = pygame.sprite.Group()
		self.ntype=2 #number of atom classes
		self.level = 1
		
		for i in range(4):
			self.atoms.add(Atom((random(),random()),"green",1.0,self))

		for i in range(4):
			self.atoms.add(Atom((random(),random()),"blue",1.0,self))
			
		Level.__init__(self,score,35)
		
		pygame.mixer.music.load("music/menu.ogg")
		pygame.mixer.music.play(-1)


class Level_2(Level):
	"Level_2"

	def __init__(self,score):
		"Initialises resources and start level"
		
		self.atoms = pygame.sprite.Group()
		self.ntype=2 #number of atom classes
		self.level = 2
		
		for i in range(10):
			self.atoms.add(Atom((random(),random()),"green",1.0,self))

		for i in range(10):
			self.atoms.add(Atom((random(),random()),"blue",1.0,self))
			
		Level.__init__(self,score,75)
			
class Level_3(Level):
	"Level_3"

	def __init__(self,score):
		"Initialises resources and start level"
		
		self.atoms = pygame.sprite.Group()
		self.ntype=3 #number of atom classes
		self.level = 3
		
		for i in range(12):
			self.atoms.add(Atom((random(),random()),"green",1.25,self))

		for i in range(12):
			self.atoms.add(Atom((random(),random()),"blue",0.75,self))
			
		for i in range(12):
			self.atoms.add(Atom((random(),random()),"red",1.0,self))		
			
		Level.__init__(self,score,152)
	
	def on_exit(self):
		Level.on_exit(self)
		h = HighScores()
		h.insert_HighScores(Constants.PLAYERNAME,str(self.score.get_score()))
		hlist = HighScores().get_HighScores()
		if len(hlist)<5 or self.score.get_score() > hlist[4].get_points():
			h.flush()
			pygame.event.clear()
			highscores = HighScoresMenu("sprites/sky.jpg")
			highscores.run()



class MessageBox(pygame.sprite.Sprite):
	"MessageBox class"

	def __init__(self,gamecontainer,time):
		"Initialises resources "
		
		pygame.sprite.Sprite.__init__(self)
	
		self.parser = make_parser()
		self.curHandler = Localization()
		self.parser.setContentHandler(self.curHandler)
		self.parser.parse(open("languages/MessageBox_" + Constants.LANGUAGE + ".xml"))
		
		self.gamecontainer=gamecontainer
		self.time_start=self.gamecontainer.time
		self.time=0.0
		self.endtime = time
		self.dirty = 1
	
		self.screen_size=Constants.SCREEN.get_size() 
		self.image=pygame.image.load("sprites/back_letters.png")
		self.image.convert_alpha()
		self.rect  = self.image.get_rect()
		self.rect.centerx = 0.5*self.screen_size[0]
		self.rect.centery = 0.5*self.screen_size[1]
		self.state = "grow"
		self.scale = 0.0
		
		self.font = pygame.font.Font(os.path.join("fonts","verdana.ttf"), 24)
		
		if self.gamecontainer.start == True:
			self.fontimg = self.font.render( self.curHandler.getText("level") + " " + str(self.gamecontainer.level), True , (230,240,255,255) )
			rect = self.fontimg.get_rect()			
			self.image.blit(self.fontimg,(self.rect.width/2 - rect.width/2,100))
			
		elif self.gamecontainer.completed == True:
			self.fontimg = self.font.render( self.curHandler.getText("finish"), True , (230,240,255,255) )
			rect = self.fontimg.get_rect()			
			self.image.blit(self.fontimg,(self.rect.width/2 - rect.width/2,80))
			self.fontimg = self.font.render( self.curHandler.getText("points"), True , (230,240,255,255) )
			rect = self.fontimg.get_rect()			
			self.image.blit(self.fontimg,(self.rect.width/2 - rect.width/2,110))
			self.fontimg = self.font.render( str(self.gamecontainer.timeclock.get_time()*15), True , (255,255,235,255) )
			rect = self.fontimg.get_rect()			
			self.image.blit(self.fontimg,(self.rect.width/2 - rect.width/2,140))
			self.gamecontainer.score.change(self.gamecontainer.timeclock.get_time()*15)
		
		elif self.gamecontainer.gameover == True:
			self.fontimg = self.font.render( self.curHandler.getText("over"), True , (230,240,255,255) )
			rect = self.fontimg.get_rect()	
			self.image.blit(self.fontimg,(self.rect.width/2 - rect.width/2,100))
			
		self.original=self.image.copy()
		
		
	def update(self):

		self.time= self.gamecontainer.time - self.time_start
		
		if self.time > self.endtime:
			if self.gamecontainer.start == True:
				self.gamecontainer.pause = False
			else:
				self.gamecontainer.quit = True

		elif self.time > self.endtime*0.1 and self.time < self.endtime*0.9:
			self.state = "stop"
			self.dirty = 0
		
		elif self.time > self.endtime*0.9:
			self.state = "shrink"
			self.dirty = 1
			self.scale = cosine_Interpolate((1.0,0.0),(self.time-(self.endtime*0.9))/(self.endtime*0.1))
					
		else:
			self.scale = cosine_Interpolate((0.0,1.0),self.time/(self.endtime*0.1))

			
		if not self.dirty:
			return
		
		self.image = pygame.transform.rotozoom(self.original,0.0,self.scale)
		self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
		self.dirty=1