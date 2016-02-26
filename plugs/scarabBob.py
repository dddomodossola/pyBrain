from body import Body
from legs import Legs
from mounth import Mounth
from touchSense import TouchSense
from brain import Brain
import pickle
from kivy.graphics import *

name = 'scarabBob'
icon = 'scarabBob.png'


"""
		touch right				walk right
		touch up				walk up		
		touch left				walk left
		touch down				walk down
		
		mounth sense sweet		eat
		mounth sense acid
"""

class ScarabBob(Body):
	def __init__(self,canvas,pos):
		global icon
		super(ScarabBob,self).__init__(canvas,pos)
		self.name = "ScarabBob"
		self.gl_shape.source='./icons/'+icon
		Legs( self )
		Mounth( self )
		TouchSense( self )
		
		try:
			self.brain = pickle.load(open("./last_brain","r+"))
			#self.brain.teach( int(b'010000',2), int(b'001111',2), int(b'10000',2), -50000000.0 )	#do not eat when is acid
		except Exception:
			self.brain = Brain( 6, 5, 1, 1, 0)
			self.brain.teach( int(b'100000',2), int(b'001111',2), int(b'10000',2), 100000.0 )	#when is sweet eat
			"""self.brain.teach( int(b'000001',2), int(b'110000',2), int(b'00001',2), 1000.0 )		#move to what you are touching
			self.brain.teach( int(b'000010',2), int(b'110000',2), int(b'00010',2), 1000.0 )
			self.brain.teach( int(b'000100',2), int(b'110000',2), int(b'00100',2), 1000.0 )
			self.brain.teach( int(b'001000',2), int(b'110000',2), int(b'01000',2), 1000.0 )
			self.brain.teach( int(b'001001',2), int(b'110000',2), int(b'00001',2), 1000.0 )
			self.brain.teach( int(b'000101',2), int(b'110000',2), int(b'00001',2), 1000.0 )
			self.brain.teach( int(b'000011',2), int(b'110000',2), int(b'00001',2), 1000.0 )
			self.brain.teach( int(b'000110',2), int(b'110000',2), int(b'00010',2), 1000.0 )
			self.brain.teach( int(b'001010',2), int(b'110000',2), int(b'00010',2), 1000.0 )
			self.brain.teach( int(b'001100',2), int(b'110000',2), int(b'00100',2), 1000.0 )
			self.brain.teach( int(b'000110',2), int(b'110000',2), int(b'00100',2), 1000.0 )
			self.brain.teach( int(b'010000',2), int(b'001111',2), int(b'10000',2), -500000.0 )	#do not eat when is acid
			self.brain.teach( int(b'010000',2), int(b'001110',2), int(b'00001',2), 1000.0 )	#walk away when acid
			self.brain.teach( int(b'010000',2), int(b'001101',2), int(b'00010',2), 1000.0 )	#walk away when acid
			self.brain.teach( int(b'010000',2), int(b'001011',2), int(b'00100',2), 1000.0 )	#walk away when acid
			self.brain.teach( int(b'010000',2), int(b'000111',2), int(b'01000',2), 1000.0 )	#walk away when acid
			self.brain.teach( int(b'000001',2), int(b'111110',2), int(b'00001',2), 500.0 )
			self.brain.teach( int(b'000010',2), int(b'111101',2), int(b'00010',2), 500.0 )
			self.brain.teach( int(b'000100',2), int(b'111011',2), int(b'00100',2), 500.0 )
			self.brain.teach( int(b'001000',2), int(b'110111',2), int(b'01000',2), 500.0 )"""

		
	def __del__(self):
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>saving brain")
		pickle.dump(self.brain,open("./last_brain","w"))
	
	def clock(self,modeler):
		super(ScarabBob,self).clock(modeler)
		inputs = (self.touch_sense.touch_state + (self.mounth.sense_status << 4)) & int(b'111111',2)
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
	return ScarabBob