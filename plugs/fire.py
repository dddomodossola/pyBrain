import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from entity import Entity
from kivy.clock import Clock
import time

name = 'fire'
icon='fire4.png'

class Fire(Entity):

	def __init__(self,canvas,pos):
		super(Fire, self).__init__(canvas,pos)
		self.name = 'Fire'
		self.gl_shape.source = './icons/fire4.png'
		print( 'new fire' )
		
	def clock(self,modeler):
		super(Fire,self).clock(modeler)
		models_list = modeler.get_at_multiple(self.pos_x,self.pos_y)
		for m in models_list:
			if m!=self:
				m.damage(0.01)

	def on_power(self,instance,value):
		super(Fire,self).on_power(instance,value)
		
	def is_acid(self):
		return True

def do():
	print( 'modul tree do' )
	return Fire