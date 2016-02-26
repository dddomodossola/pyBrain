import os
import imp

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

selectedClass=None

class PlugWidget( BoxLayout ):
	def __init__(self, path, fileName):
		super(PlugWidget,self).__init__(orientation='horizontal',height=60)
		self.path = path
		self.file_name = fileName

		modul = imp.load_source( fileName, path + fileName )
		self.modul = modul
		
		print( dir( modul ) )

		img = Image( source='./icons/'+modul.icon )

		cmd = Button( text=fileName )
		cmd.bind( on_press=self.selected )
		self.add_widget( img )
		self.add_widget( cmd )
		
	def selected(self,instance):
		global selectedClass
		selectedClass = self.modul.do()

class PlugsLoader( BoxLayout ):
	def __init__( self, path='./plugs/' ):
		super(PlugsLoader,self).__init__(orientation='vertical',size_hint=(1.0,1.0),background_color=(1.0,1.0,1.0))
		dirList = os.listdir( path )
		for fileName in dirList:
			if( fileName.endswith(".py") ):
				print( 'PlugsLoader init found: ' + fileName )
				plug = PlugWidget( path, fileName )
				self.add_widget( plug )

	def build_selected(self,p1,p2):
		global selectedClass
		if selectedClass!=None:
			return selectedClass(p1,p2)
