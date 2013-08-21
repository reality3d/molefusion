import xml.dom.minidom

class HighScores:
	"""HighScores Class"""
	
	def __init__(self):
		
	
		self.datasource = open("highscores/highscores.xml","r")
		self.dom = xml.dom.minidom.parse(self.datasource)
		self.datasource.close()
		self.users=self.dom.getElementsByTagName("user")
		self.highscores=[]
		self.read_HighScores()
	
	
	def read_HighScores(self):
		for i in self.users:
			self.highscores.append(NamePoints(i.getAttribute("name"),int(i.getAttribute("points"))))
		self.highscores.sort(cmp,NamePoints.get_points,True)

	def get_HighScores(self):
		return self.highscores
	
	def insert_HighScores(self,name,points):
		user = self.dom.createElement("user")
		user.setAttribute( "name", name)
		user.setAttribute( "points", points)
		self.dom.documentElement.appendChild(user)

	def flush(self):
		self.datasource = open("highscores/highscores.xml","w+")
		self.dom.writexml(self.datasource)
		self.datasource.close()
		
	def __del__(self):
		self.datasource = open("highscores/highscores.xml","w+")
		self.dom.writexml(self.datasource)
		self.datasource.close()
		

class NamePoints:
	"""Name Points Tuple"""
	
	def __init__(self,name,points):
		
		self.name  = name
		self.points = points
	
	def get_name(self):
		return self.name

	def get_points(self):
		return int(self.points)