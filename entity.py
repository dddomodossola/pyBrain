import math
from kivy.graphics import *
from kivy.properties import *
from kivy.event import *
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import time

class Entity(EventDispatcher):
	name = StringProperty( "object" )
	selected = BooleanProperty(False)
	size = NumericProperty(50)
	pos_x = NumericProperty(0)
	pos_y = NumericProperty(0)
	power = NumericProperty(100)
	deletable = BooleanProperty(False)
	
	def __init__(self,canvas,pos):
		super(Entity, self).__init__()
		
		self.creation_time = time.time()

		self.info_lbl=Label(text=self.name,font_size=9)

		self.gl_push = PushMatrix()
		self.gl_pos = Translate(self.pos_x,self.pos_y,0)
		self.gl_rot = Rotate(0,0,0,1)
		self.gl_contours_shape = Line(points=[0, 0, 
											  0, self.size, 
											  self.size, self.size,
											  self.size, 0,
											  0, 0], width=1)
		self.gl_shape = Rectangle(size=(self.size, self.size), source='mtexture1.png')
		self.gl_color = Color( 1.0, 1.0, 1.0 )
		self.gl_pop = PopMatrix()

		self.canvas = canvas
		
		self.sub_gl_components={}
		self.parts={}


			
		self.add_to_render_chain( self.gl_pos )
		self.add_to_render_chain( self.info_lbl.canvas )
		self.add_to_render_chain( self.gl_rot )
		self.add_to_render_chain( self.gl_color )
		self.add_to_render_chain( Translate(-self.size/2, -self.size/2,0) ) #in this way, all the renderings of the attachable elements (like legs) will consider the centre of the entity as zero	
		
		self.add_to_render_chain( self.gl_shape )
		self.add_to_render_chain( self.gl_contours_shape )
		
		
		self.add_to_render_chain( Translate(self.size/2, self.size/2,0) )

		#self.init_canvas()
		
		self.pos_x = pos.x
		self.pos_y = pos.y
		
	
	def clock(self, modeler):
		if self.selected:
			self.info_lbl.font_size=12
			self.info_lbl.font_bold=True
		else:
			self.info_lbl.font_size=9
			self.info_lbl.font_bold=False
		self.info_lbl.text = self.name + '\nx: ' + str(self.pos_x) + '\ny: ' + str(self.pos_y) + '\npower: ' + str(self.power)
		for p in self.parts.values():
			if 'clock' in dir(p):
				p.clock(modeler)

	def add_to_clock_chain(self,part):
		self.parts[len(self.parts)]=part
		
	def init_canvas(self):
		self.canvas.add( self.gl_push )
		for k in self.sub_gl_components.keys():
			self.canvas.add( self.sub_gl_components[k] )
		self.canvas.add( self.gl_pop )

	def remove(self):
		self.canvas.remove( self.gl_push )
		for c in self.sub_gl_components.values():
			self.canvas.remove(c)
		self.canvas.remove( self.gl_pop )
	
	def add_to_render_chain(self,canvas_comp):
		if canvas_comp in self.sub_gl_components.values():
			return
		self.remove()
		self.sub_gl_components[len(self.sub_gl_components)]=canvas_comp
		self.init_canvas()

	def touched(self, pos):
		self.selected = ((math.sqrt( (self.pos_x - pos.x)**2 + (self.pos_y - pos.y)**2 ))<self.size)
		return self.selected
	
	def touch_quest(self, x, y):
		return ((math.sqrt( (self.pos_x - x)**2 + (self.pos_y - y)**2 )) < (self.size/2.0) )
		
	def on_size(self, instance, value):
		print("new value for size: ", value)
		self.gl_shape.size = (value,value)
		
	def on_selected(self, instance, value):
		print("selection changed")
		"""if value:
			self.gl_color.r = 1.0
			self.gl_color.g = 0.4
			self.size = 18
		else:
			self.gl_color.r = 0.4
			self.gl_color.g = 1.0
			self.size = 15"""
			
	def on_pos_x(self, instance, value):
		self.gl_pos.x = value

	def on_pos_y(self, instance, value):
		self.gl_pos.y = value
	
	def on_power(self,instance,value):
		if self.power <= 0:
			self.remove()
			self.deletable = True

	def damage(self,quantity):
		self.power = self.power - quantity

	def is_acid(self):
		return False

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