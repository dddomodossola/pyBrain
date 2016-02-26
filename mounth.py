import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import types

class Mounth(EventDispatcher):
	def __init__(self,parent):
		super(Mounth,self).__init__()
		self.parent = parent
		
		self.components = {}
		self.components[0] = Color( 1, 0.3, 0 )
		self.components[1] = Line(points=[0,0, 50, 0], width=1)
		self.add_to_render_chain()

		self.parent.add_to_clock_chain(self)

		#add method
		self.parent.eat = types.MethodType( eat, self.parent )
		
		self.parent.mounth = self

		#2 bits - sweet / acid
		self.sense_status = 0
	
	def update_sense_status(self,modeler):
		x = self.parent.pos_x + math.cos( (self.parent.gl_rot.angle)/180.0*math.pi ) * (self.parent.size)
		y = self.parent.pos_y + math.sin( (self.parent.gl_rot.angle)/180.0*math.pi ) * (self.parent.size)

		entit = modeler.get_at( x, y )
		
		if entit != None:
			if entit.is_acid():
				self.sense_status = 1
			else:
				self.sense_status = 2
		else:
			self.sense_status = 0
		
	
	def add_to_render_chain(self):
		for c in self.components.values():
			self.parent.add_to_render_chain(c)
		
	def clock(self,modeler):
		self.parent.modeler = modeler
		self.update_sense_status(modeler)
		

def eat(self):
	if not('modeler' in dir(self)):
		return
	x = self.pos_x + math.cos( (self.gl_rot.angle)/180.0*math.pi ) * (self.size)
	y = self.pos_y + math.sin( (self.gl_rot.angle)/180.0*math.pi ) * (self.size)
	entit = self.modeler.get_at( x, y )
	if entit != None:
		#print("_________________eating something")
		if entit.is_acid():
			entit.damage(1)
			self.power = self.power - 1
			#print("_________________acid")
		else:
			entit.damage(1)
			self.power = self.power + 0.3
			#print("_________________eating sweet")
	
