from xml.sax.handler import ContentHandler

class Localization(ContentHandler):
	"""Localization Class"""
	
	def __init__(self):
		
		self.identifiers={}

	def startElement(self, name, attrs):
		if name == "option" or name == "img":
			self.identifiers[attrs.get("id")]=attrs.get("value")
		return
	
	def getText(self,key):
		return self.identifiers[key]

