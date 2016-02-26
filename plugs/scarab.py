from body import Body
from legs import Legs
from mounth import Mounth
from touchSense import TouchSense
from brain import Brain
import pickle
from kivy.graphics import *

name = 'scarab'
icon = 'scarab1.png'


"""
		touch right				walk right
		touch up				walk up		
		touch left				walk left
		touch down				walk down
		
		mounth sense sweet		eat
		mounth sense acid
"""

class Scarab(Body):
	def __init__(self,canvas,pos):
		#global icon
		super(Scarab,self).__init__(canvas,pos)
		self.name = "Scarab"
		#self.gl_shape = Rectangle(size=(self.size, self.size), source='./icons/'+icon)
		Legs( self )
		Mounth( self )
		TouchSense( self )
		
		#try:
		#	self.brain = pickle.load(open("./last_brain","r+"))
		#except Exception:
		self.brain = Brain( 6, 5, 1, 1, 2)
			#self.brain.teach( int(b'100000',2), int(b'001111',2), int(b'10000',2) )

		
	def __del__(self):
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>saving brain")
		#pickle.dump(self.brain,open("./last_brain","w"))
	
	def clock(self,modeler):
		self.name = "asd"
		super(Scarab,self).clock(modeler)
		inputs = (self.touch_sense.touch_state | (self.mounth.sense_status << 4)) & int(b'111111',2)
		outs = self.brain.activateInput( inputs )
		chkwalk = (outs&1) + (outs&2)>>1 + (outs&4)>>2 + (outs&8)>>3
		if chkwalk <= 1:
			if outs&1:
				self.walk_right()
			if outs&2:
				self.walk_up()
			if outs&4:
				self.walk_left()
			if outs&8:
				self.walk_down()
		if outs&16:
			#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>EAT<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			self.eat()
		
		lbli = bin(inputs)
		lbli = lbli.zfill(6)
		
		lblo = bin(outs)
		lblo = lblo.zfill(5)
		self.name = "in: " + lbli + "\nout:" + lblo# + "\n" + self.info_lbl.text
		self.info_lbl.text = self.name + '\nx: ' + str(self.pos_x) + '\ny: ' + str(self.pos_y) + '\npower: ' + str(self.power)
				
	def is_acid(self):
		return True
	
	
def do():
	return Scarab