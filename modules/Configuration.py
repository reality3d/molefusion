from xml.sax.handler import ContentHandler

class Configuration(ContentHandler):
	"""Configuration Class"""
	
	def __init__(self):
		
	
		self.name=""	
		self.x=""
		self.y=""
		self.mouse=0
		self.isnameElement=0
		self.fullscreen="no"

	def startElement(self, name, attrs):
		if name == "name":
			self.isnameElement=1		
		elif name == "resolution":
			self.x = int(attrs.get("x"))
			self.y = int(attrs.get("y"))
		elif name == "mouse":
			self.mouse = int(attrs.get("visible"))
		elif name == "fullscreen":
			self.fullscreen = int(attrs.get("value"))
		return
	
	def endElement(self, name):
		if name == "name":
			self.isnameElement=0
		return			
	
	def characters(self,ch):
		if self.isnameElement==1:
			self.name+=ch
			
	def getName(self):
		return self.name

	def getRes(self):
		return (self.x,self.y)

	def getMouseVisibility(self):
		return self.mouse

	def getFullscreen(self):
		return self.fullscreen