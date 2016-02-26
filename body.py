import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from entity import Entity
from kivy.clock import Clock
import time

class Body(Entity):

	def __init__(self,canvas,pos):
		super(Body, self).__init__(canvas,pos)
		self.name = 'animal'
		self.gl_shape.source = './icons/scarab1.png'
		self.last_power=self.power
		self.last_hungry_time=self.creation_time
	
	def clock(self,modeler):
		super(Body,self).clock(modeler)
		if time.time()-self.last_hungry_time > 0.30:
			self.hungry()
			self.last_hungry_time=time.time()

	def hungry(self):
		self.power = self.power - 0.1

	def on_power(self,instance,value):
		super(Body,self).on_power(instance,value)
		feed=self.power-self.last_power
		
		self.brain.feedback(feed)
		self.last_power=self.power


"""	def represent_settings(self, setting_panel):
		for pname in self.properties():
			prop = self.property(pname)
			widget = self.widget_for_property( pname,prop )
			if widget != None:
				setting_panel.add_widget( widget )
			
	def widget_for_property(self, pname, prop):
		widget = None
		if type(prop) is NumericProperty:
			widget = TextInput( text = str( self.getter(pname)(prop) ), focus=True, multiline=False )
			widget.bind( on_validate_text = self.setter(pname) )
		return widget
"""