import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import types

class TouchSense(EventDispatcher):
	def __init__(self,parent):
		super(TouchSense,self).__init__()
		self.parent = parent
		
		self.components = {}
		self.components[len(self.components)] = Color( 1, 1, 1 )
		self.add_to_render_chain()

		self.parent.add_to_clock_chain(self)

		#add method
		#self.parent.move_relative = types.MethodType( move_relative, self.parent )

		self.parent.touch_sense = self
		
		#4 bits - right / up / left / down
		self.touch_state = 0 #output value
		
	def add_to_render_chain(self):
		for c in self.components.values():
			self.parent.add_to_render_chain(c)
		
	def clock(self,modeler):
		inputs_state = 0
		#right test
		i1 = 0
		i2 = 0
		i3 = 0
		i4 = 0
		i=1
		for i in range(1,20):
			if modeler.get_at( self.parent.pos_x + i*self.parent.size, self.parent.pos_y ) != None:
				i1 = 1
		
		#up test
		for i in range(1,20):
			if modeler.get_at( self.parent.pos_x, self.parent.pos_y + i*self.parent.size ) != None:
				i2 = 2
			
		#left test
		for i in range(1,20):
			if modeler.get_at( self.parent.pos_x - i*self.parent.size, self.parent.pos_y ) != None:
				i3 = 4

		#down test
		for i in range(1,20):
			if modeler.get_at( self.parent.pos_x, self.parent.pos_y - i*self.parent.size ) != None:
				i4 = 8

		self.touch_state = i1 + i2 + i3 + i4
		
#def move_relative(self, x, y):
#	self.pos_x = self.pos_x + x
#	self.pos_y = self.pos_y + y
