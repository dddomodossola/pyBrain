import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from entity import Entity
from kivy.clock import Clock
import time

name = 'tree'
icon='tree1.png'

class Tree(Entity):

	def __init__(self,canvas,pos):
		super(Tree, self).__init__(canvas,pos)
		self.name = 'Tree'
		self.gl_shape.source = './icons/tree1.png'
		print( 'new tree' )
		
	def clock(self,modeler):
		super(Tree,self).clock(modeler)

	def on_power(self,instance,value):
		super(Tree,self).on_power(instance,value)

def do():
	print( 'modul tree do' )
	return Tree