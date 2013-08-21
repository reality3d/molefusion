import pygame
from pygame.locals import *

from Math_Funcs import *
from math import *
from random import *

import Perlin

import os

from Constants import Constants

class Atom(pygame.sprite.Sprite):
	"""Atom actor class"""
	
	images_blue=[]
	images_green=[]
	images_red=[]
	def __init__(self,pos,type,velocity,gamecontainer):
		
		pygame.sprite.Sprite.__init__(self)
		
		self.screen_size=Constants.SCREEN.get_size()
		
		self.gamecontainer = gamecontainer
		
		self.type = type
		
		if self.type == "blue":
			if len(Atom.images_blue) == 0:
				for i in os.listdir("sprites/atom_blue"):
					Atom.images_blue.append(pygame.image.load("sprites/atom_blue/" + i))
					Atom.images_blue[-1] = Atom.images_blue[-1].convert_alpha() #for blitting more faster
				
			
		if self.type == "green":
			if len(Atom.images_green) == 0:
				Atom.images_green.append(pygame.image.load("sprites/atom_green/atom_1.png"))
				Atom.images_green[-1] = Atom.images_green[-1].convert_alpha()
				
		if self.type == "red":
			if len(Atom.images_red) == 0:
				Atom.images_red.append(pygame.image.load("sprites/atom_red/atom_1.png"))
				Atom.images_red[-1] = Atom.images_red[-1].convert_alpha()

		self.image = eval("Atom.images_" + self.type + "[0]")
		self.original=self.image.copy()
		self.rect  = self.image.get_rect()	
		self.x = pos[0]
		self.y = pos[1]
		self.rect.center = (self.screen_size[0]*self.x,self.screen_size[1]*self.y)
		
		self.dirty=0
		
		
		self.angle = radians(360.0)*random()
		self.randomphase = [35.0*random(),35.0*random()]
		self.time_speed =pygame.time.Clock()
		self.dt =0.0
		self.time =0.0
		self.time1 =0.0
		self.angle = 0.0
		self.acum = [0.0,0.0] #Since screen space is integer
		self.noise = Perlin.SimplexNoise();
		
		self.mass = 0.25
		
		self.state="normal"
		self.target_time=0.0
		self.childCount=0
		self.combo=0
		self.scorecombo = 0
		self.fade_score = False
		self.velocityfactor = velocity
		
		self.frame = 0
		self.increasesize = True
		self.animtime = 0.0

	def get_pos(self):
		return (self.rect.centerx,self.rect.centery)

	def get_angle(self):
		return self.angle
	
	def set_angle(self,angle):
		self.angle = angle
	
	def get_type(self):
		return self.type

	def get_mass(self):
		return self.mass
	
	def get_state(self):
		return self.state

	def set_state(self,state):
		self.state = state
	
	def set_target(self,target):		
		self.target_object = target
		
	def set_childCount(self,count):
		""" Number of childs that will be fusionated with father"""
		self.childCount = count
		self.combo = count


	def delete_child(self,child):
		""" When an atom is fusioned with another bigger the child atom
			says the bigger atom to delete him """
			
		self.childCount-=1		
		self.mass += child.get_mass()/1.5

		#self.frame += 1
		#self.increasesize = not self.increasesize
		
		self.gamecontainer.atoms.remove(child)
		del child
		
		if self.childCount==0:
			pygame.mixer.Sound("sounds/points.ogg").play()
			extra = 0			
			if self.combo > 1:
				extra = self.combo*5
			self.scorecombo = self.combo*10 + extra
			self.gamecontainer.score.change(self.scorecombo)#lanza score!
			if(len(self.gamecontainer.atoms) == self.gamecontainer.ntype):#End of level
				self.gamecontainer.completed = True
			self.state = "normal_scoring"

	def strategy_normal(self):
		
		self.dt =float(self.time_speed.tick()/1000.0)
		self.time +=self.dt
		self.velocity = [self.noise.noise2((self.time+self.randomphase[0])/16.0,1.0), self.noise.noise2((self.time + self.randomphase[1])/16.0,1.0)]
		self.velocity_modulus = sqrt(self.velocity[0]*self.velocity[0]+self.velocity[1]*self.velocity[1])
		self.velocity = [self.velocityfactor*self.velocity[0]/self.velocity_modulus,self.velocityfactor*self.velocity[1]/self.velocity_modulus]
		self.angle = -degrees(atan2(self.velocity[1],self.velocity[0]))
		
		self.image = pygame.transform.rotozoom(self.original,self.angle,self.mass)
		self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
		
		#Integer math!
		
		self.acum[0] += self.velocity[0]
		self.acum[1] += self.velocity[1]
		sum = [int(self.acum[0]/1.0),int(self.acum[1]/1.0)]
		if abs(sum[0])>0:
			self.rect.centerx += sum[0]
			self.acum[0] -= sum[0]
		if abs(sum[1])>0:
			self.rect.centery += sum[1]
			self.acum[1] -= sum[1]

	def strategy_scoring(self):
		
		self.time1 +=self.dt
		
		self.font = pygame.font.Font(os.path.join("fonts","verdana.ttf"), 20)
		self.fontimg = self.font.render( str(self.scorecombo), False , (255*abs(sin(self.time1*19.0)),255*abs(sin(self.time1*20.0)),0,255) )
		if self.fade_score == True:
			localalpha = 250 - self.time1*250.0
		else:
			localalpha = self.time1*400.0
			
		self.fontimg.set_alpha(localalpha)
		
		if localalpha > 255  and self.fade_score == False:
			self.time1 = 0.0
			self.fade_score = True
			
		self.image.blit(self.fontimg,(5,0))
		
		if localalpha <= 0 and self.fade_score == True:
			self.state = "normal"
			self.fade_score = False
			self.time1 = 0.0
				
		
	def strategy_targeting(self):
		
		self.dt=float(self.time_speed.tick()/1000.0)
		self.target_time += self.dt
		
		if(self.target_time>0.5):
			self.target_object.delete_child(self)
		else:
			if(abs(self.target_object.get_angle() - self.angle)>180.0):
				self.angle = -(360.0 - self.angle)
			else:
				self.angle = cosine_Interpolate((self.angle,self.target_object.get_angle()),self.target_time*1.5/1.25)
			
			self.image = pygame.transform.rotozoom(self.original,self.angle,self.mass)
			self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))			
			self.rect.centerx = cosine_Interpolate((self.get_pos()[0],self.target_object.get_pos()[0]),self.target_time*1.5/1.25)
			self.rect.centery = cosine_Interpolate((self.get_pos()[1],self.target_object.get_pos()[1]),self.target_time*1.5/1.25)
		
	def update(self):
		
		#self.animtime += self.dt
		#if self.increasesize:
			#if self.frame > len(eval("Atom.images_" + self.type)) - 1:
			#	self.frame = 0
		#	self.image = eval("Atom.images_" + self.type + "[" + str(self.frame) + "]")
		#	self.original=self.image.copy()
		#	self.increasesize = not self.increasesize
		#	self.animtime = 0.0
			
		if self.state == "normal":
			self.strategy_normal()
		elif self.state == "targeting":
			self.strategy_targeting()
		elif self.state == "normal_scoring":
			self.strategy_normal()
			self.strategy_scoring()			
	
			
		if self.rect.right<=0:
			self.rect.left=self.screen_size[0]
		elif  self.rect.left >=self.screen_size[0]:
			self.rect.left=0-self.rect.width
		
		
		if self.rect.bottom<=0:
			self.rect.top=self.screen_size[1]
		elif  self.rect.top >= self.screen_size[1]:
			self.rect.top=0-self.rect.height
		
			

