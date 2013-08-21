class Event:
	"""this is a superclass for any event type"""
	def __init__(self,name,event):
		self.name = name
		self.event = event
		
	def get_name(self):
		return self.name
	
	def get_event(self):
		return self.event