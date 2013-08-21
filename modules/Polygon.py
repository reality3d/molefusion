import pygame
from pygame.locals import *

from math import *

from Atom import *

from Constants import Constants

class Polygon:
	"""Polygon class"""
	def __init__(self,gamecontainer):
		
		self.screen=Constants.SCREEN
		self.gamecontainer=gamecontainer
		self.pointlist=[]
		self.delaytime=10
				
		self.polyaddtime=pygame.event.Event(Constants.POLYADDTIME, {})
		pygame.time.set_timer(Constants.POLYADDTIME, self.delaytime)
		
		self.active = False
		self.activetime = 0
		self.distance=self.get_distance(self.pointlist)
		self.fadepolygonlist=[]
		

	def __del__(self):
		pygame.time.set_timer(Constants.POLYADDTIME, 0)
		
	def get_pointlist(self):
		return self.pointlist
	
	def add_point(self,point):
		self.pointlist.append(point)

	def get_time(self):
		return self.activetime
				
	def change_time(self,time):
		self.activetime+=time
		
	def get_linetime(self):
		return self.delaytime
		
	def alive(self):
		return self.active

	def set_alive(self,value):
		self.active= value
	
	def reset(self):
		self.pointlist=[[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]]
		self.activetime = 0
	
	def get_distance(self,points):
		
		distance=0
		if len(points)>1:
			for i in range(len(points)-1):
				distance+=sqrt((points[i+1][0]-points[i][0])*(points[i+1][0]-points[i][0]) + (points[i+1][1]-points[i][1])*(points[i+1][1]-points[i][1]))		
		return distance
	
	def get_points_number(self):
		return len(self.pointlist)
		
	def check_similarity(self):	
	
		if abs(pygame.mouse.get_pos()[0]-self.pointlist[len(self.pointlist)-1][0])>0 and abs(pygame.mouse.get_pos()[1]-self.pointlist[len(self.pointlist)-1][1])>0:
				return False
		return True	


	def insidepoly(self,polygon,point):

		p1 = polygon[0]
		p2 = None
		xinters= None
		counter= 0
		
		for i in range(len(polygon)-1):
			p2 = polygon [i%len(polygon)]
			if point[1]>min(p1[1],p2[1]):
				if point[1]<=max(p1[1],p2[1]):
					if point[0]<=max(p1[0],p2[0]):
						if p1[1]!=p2[1]:
							xinters = (point[1]-p1[1])*(p2[0]-p1[0])/(p2[1]-p1[1])+p1[0]							
							if (p1[0]==p2[0]) or (point[0] <=xinters):
								counter+=1
			p1 = p2
		if counter % 2==0:
			return False
		else:
			return True							       

	def check_intersection(self,lastline):
		if len(self.pointlist)>=3:
			
			x3,y3 = float(lastline[0][0]),float(lastline[0][1])
			x4,y4 = float(lastline[1][0]),float(lastline[1][1])
			
			deltalastx = x4 - x3
			deltalasty = y4 - y3
					
			for i in range(len(self.pointlist)-3):			
				
				x1,y1=float(self.pointlist[i][0]),float(self.pointlist[i][1])
				x2,y2=float(self.pointlist[i+1][0]),float(self.pointlist[i+1][1])
											
				deltax = x2 - x1
				deltay = y2 - y1
				
				denom=(deltalasty*deltax - deltalastx*deltay ) 
				if denom!=0.0:
					ua= (deltalastx*(y1-y3) - deltalasty*(x1-x3)) / denom 
					ub= (deltax*(y1-y3) - deltay*(x1-x3)) / denom
				
					if ua>=0 and ua<=1.0 and ub>=0 and ub<=1.0:
						x = x1 + ua*(x2 - x1)
						y = y1 + ua*(y2 - y1) 
						#print i,"at ",x,y,"with ua,ub",ua,ub
						return i,[x,y]					
		return -1,-1				 

	def draw(self):
		
		if(self.active):

			line,point=self.check_intersection([self.pointlist[len(self.pointlist)-2] , self.pointlist[len(self.pointlist)-1]])
			if line!=-1:
				point= [int(point[0]),int(point[1])]
				
				#First and last point of the poly will be the same
				self.pointlist[line]=point
				self.pointlist[len(self.pointlist)-1]=point
				atom_inside_list=[]
				atom_type = None
				for i in self.gamecontainer.atoms:
					if self.insidepoly(self.pointlist[line:],i.get_pos()):
						if atom_type == None:
							atom_inside_list.append(i)
							atom_type = i.get_type()
						elif i.get_type() == atom_type:
							atom_inside_list.append(i)
						else:
							atom_inside_list=[]
							break
				
				if(len(atom_inside_list)>1):
					atom_inside_list.sort(cmp,Atom.get_mass,True)
					atom_inside_list[0].set_childCount(len(atom_inside_list[1:]))
					for i in atom_inside_list[1:]:
						i.set_state("targeting")
						i.set_target(atom_inside_list[0])
							

				#pygame.draw.lines(self.screen, (255,200,30), False,self.pointlist[line:],10)			
				if len(self.pointlist[line:])>2:		
					self.fadepolygonlist.append(FadePolygon(line,self.pointlist,100,2000))
				self.reset()
				self.active= False

			self.rect = pygame.draw.aalines(self.screen, (255,255,180), False,self.pointlist + [[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]],3)	
		for i in self.fadepolygonlist[:]:				
			i.draw()
			if i.get_alpha()<=0:
				del i


class FadePolygon:
	"""Fade Polygon class"""
	def __init__(self,line,pointlist,alpha,time):
		
		self.screen=Constants.SCREEN
		self.polyscreen=self.screen.copy()
		self.polyscreen.convert_alpha()
		self.polyscreen.fill((0,0,0,0))
		self.polyscreen.set_colorkey((0,0,0,0))
		self.alpha=alpha
		self.polyscreen.set_alpha(self.alpha)
		self.line=line
		self.pointlist=pointlist
		self.fadeout=True
		self.time_speed=pygame.time.Clock()
		self.timefade=time
		self.time=0
		

	def get_alpha(self):
		return self.alpha
		
	def draw(self):
		
		if self.time<self.timefade:
			self.time_speed.tick()
			self.time+=self.time_speed.get_time()
			self.rect = pygame.draw.polygon(self.polyscreen, (255,255,180) , self.pointlist[self.line:], 0)
			self.polyscreen.set_alpha(self.alpha-(float(self.time)/self.timefade)*255)
			self.screen.blit(self.polyscreen,(0,0))
			