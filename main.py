import sys

#output and error redirection
sys.stdout = open("./stdout.txt","w+b",0)
sys.stderr = open("./stderr.txt","w+b",0)

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from kivy.event import *
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock
from kivy.properties import *
from kivy.interactive import *

#from kivy.uix.codeinput import CodeInput
#from pygments.lexers import CythonLexer

from plugsLoader import PlugsLoader

import pickle


app = None

class Modeler(Widget,EventDispatcher):
	plugIndex = NumericProperty(0)
	
	def __init__(self, plugs_loader):
		super(Modeler, self).__init__()
		self.plugs_loader = plugs_loader
		self.plugs = {}
		self.selectedPlug = None
		Clock.schedule_interval(self.clock, 1.0/60.0)
	
	def __del__(self):
		for m in self.plugs.values():
			if '__del__' in dir(m):
				m.__del__()
				
	def on_press(self):
		print( 'Modeler on_press' )

	def clock(self,*largs):
		for k in self.plugs.keys():
			self.plugs[k].clock(self)
			if self.plugs[k].deletable:
				del(self.plugs[k])
				

	def get_at(self,x,y):
		for m in self.plugs.values():
			if m.touch_quest(x,y):
				return m
		return None

	def get_at_multiple(self,x,y):
		ret = list()
		for m in self.plugs.values():
			if m.touch_quest(x,y):
				ret.append(m)
		return ret

		
	def on_touch_down(self,touch):
		super(Modeler,self).on_touch_down(touch)
		t = touch
		t.x = t.x - t.x%50 +25
		t.y = t.y - t.y%50 +25
		print(dir(touch))
		if not self.collide_point(t.x,t.y):
			return False
		selected = False
		for m in self.plugs.values():
			if m.touched(t):
				selected = True
				self.selectedPlug = m
				
		if not selected:
			plug = self.plugs_loader.build_selected( self.canvas, t )
			if plug != None:
				self.plugs[ self.plugIndex ] = plug
				self.plugIndex = self.plugIndex + 1
				self.selectedPlug = plug


	def on_touch_move(self,touch):
		pass
		
	def on_touch_up(self,touch):
		pass
		
	def delete_plug(self,bt_instance):
		if self.selectedPlug!=None:
			self.selectedPlug.remove()
			self.selectedPlug.deletable = True
		


class InteractiveShell(BoxLayout):
	def __init__(self):
		super(InteractiveShell,self).__init__(orientation='vertical',size_hint=(0.3,1.0))
		
		self.text_input = TextInput(font_size='10px',multiline = True,size_hint=(1.0,0.9) )
		
		self.code_input = TextInput(font_size='10px',size_hint=(0.9,1.0)) #CodeInput(lexer=CythonLexer(),size_hint=(0.9,1.0))
		
		cmd = Button(text='exec',size_hint=(0.1,1.0))
		cmd.bind(on_press=self.exec_code)
		
		hbox = BoxLayout(orientation='horizontal',size_hint=(1.0,0.1))
		
		
		hbox.add_widget( self.code_input )
		hbox.add_widget( cmd )
		self.add_widget( hbox )
		self.add_widget( self.text_input )
		
	def exec_code(self,bt_instance):
		global app
		#self.text_input.text = self.text_input.text + '\n' + ">>> " + self.code_input.text
		print( ">>> " + self.code_input.text )
		try:
			exec(self.code_input.text)
			f = open("./stdout.txt","r+b")
			self.text_input.text = f.read()
			f.close()
		except Exception as e:
			self.text_input.text = self.text_input.text + '\n' + "____exception: " + repr(e)
			print("____exception: " + repr(e))
		
		
	
class TestPlatform(App):
	def build(self):
		root = BoxLayout(orientation='horizontal')
		
		plugs_loader = PlugsLoader()
		
		self.modeler = Modeler( plugs_loader )
		
		bt_delPlug = Button(text='del',size_hint=(1.0,0.2))
		bt_delPlug.bind(on_press=self.modeler.delete_plug)
		
		vbox = BoxLayout(orientation='vertical',size_hint=(0.2,1.0))
		vbox.add_widget( bt_delPlug )
		vbox.add_widget( plugs_loader )
		root.add_widget( vbox )
		root.add_widget( self.modeler )
		#root.add_widget( InteractiveShell() )
		
		return root
	
	def __del__(self):
		self.modeler.__del__()

	
if __name__ == "__main__":
	global app
	app = TestPlatform()
	app.run()
	#interactiveLauncher = InteractiveLauncher(t)
	#interactiveLauncher.run()
	app.__del__()