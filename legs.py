import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import types

class Legs(EventDispatcher):
	def __init__(self,parent):
		super(Legs,self).__init__()
		self.parent = parent
		
		self.components = {}
		self.components[len(self.components)] = Color( 1, 1, 1 )
		self.components[len(self.components)] = Line(points=[5, 3, 0, -5], width=2)
		self.components[len(self.components)] = Line(points=[5,-3, 0, 5], width=2)
		self.components[len(self.components)] = Line(points=[0,3, 0, 5], width=2)
		self.components[len(self.components)] = Line(points=[0,-3, 0, 5], width=2)
		self.components[len(self.components)] = Line(points=[-5 ,3, 0 , -5], width=2)
		self.components[len(self.components)] = Line(points=[-5 ,-3, 0, 5], width=2)
		self. add_to_render_chain()

		self.parent.add_to_clock_chain(self)

		#add method
		self.parent.move_relative = types.MethodType( move_relative, self.parent )
		self.parent.walk = types.MethodType( walk, self.parent )
		self.parent.rotate_relative = types.MethodType( rotate_relative, self.parent )
		self.parent.walk_up = types.MethodType( walk_up, self.parent )
		self.parent.walk_down = types.MethodType( walk_down, self.parent )
		self.parent.walk_left = types.MethodType( walk_left, self.parent )
		self.parent.walk_right = types.MethodType( walk_right, self.parent )

		self.parent.legs = self

		self.parent.walkable_area_width = 500
		self.parent.walkable_area_height = 500


	def add_to_render_chain(self):
		for c in self.components.values():
			self.parent.add_to_render_chain(c)
		
	def clock(self,modeler):
		self.parent.walkable_area_width = modeler.width
		self.parent.walkable_area_height = modeler.height
		#self.parent.walk(3.3)

def move_relative(self, x, y):
	self.pos_x = self.pos_x + x
	self.pos_y = self.pos_y + y
	if (self.pos_x > self.walkable_area_width) and (x>0):
		self.pos_x = self.walkable_area_width- self.walkable_area_width%x + 25
	if (self.pos_y > self.walkable_area_height) and (y>0):
		self.pos_y = self.walkable_area_height- self.walkable_area_height%y + 25
	if self.pos_x < 0:
		self.pos_x = 25.0
	if self.pos_y < 0:
		self.pos_y = 25.0

def walk_up(self):
	target_angle = 90.0
	if self.gl_rot.angle!=target_angle:
		self.gl_rot.angle = target_angle
		return
	self.move_relative( 0.0, 50 )
	
def walk_down(self):
	target_angle = 270.0
	if self.gl_rot.angle!=target_angle:
		self.gl_rot.angle = target_angle
		return
	self.move_relative( 0.0, -50 )

def walk_left(self):
	target_angle = 180.0
	if self.gl_rot.angle!=target_angle:
		self.gl_rot.angle = target_angle
		return
	self.move_relative( -50, 0.0 )

def walk_right(self):
	target_angle = 0.0
	if self.gl_rot.angle!=target_angle:
		self.gl_rot.angle = target_angle
		return
	self.move_relative( 50, 0.0 )

	
def walk(self,dist):
	self.pos_x = self.pos_x + math.cos( (self.gl_rot.angle-0)/180.0*math.pi ) * dist
	self.pos_y = self.pos_y + math.sin( (self.gl_rot.angle-0) /180.0*math.pi ) * dist
	
def rotate_relative(self, angle):
	self.gl_rot.angle = self.gl_rot.angle + angle
	