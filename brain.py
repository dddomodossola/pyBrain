class NeuroBase():
	def __init__(self,senseNeurones,motoNeurones,feedBackwardSize):
		#super(NeuroBase,self).__init__()
		self.m_senseNeurones = senseNeurones
		self.m_motoNeurones = motoNeurones
		self.m_sublayerSize = pow( 2, self.m_senseNeurones ) #teachable stratus
		self.m_sublayer = [] #list
		self.initInputSublayer()
		
		self.last_activations = list()
		self.last_activations_size = feedBackwardSize
		
	def initInputSublayer(self):
		for i in range(0,self.m_sublayerSize):
			self.m_sublayer.append(None)
		
	def activate(self,binInput):
		#print("NeuroBase activate: " + bin(binInput))
		self.m_lastBinInput = binInput
		if self.m_sublayer[binInput] == None:
			self.m_sublayer[binInput] = [] #list
			for i in range(0,pow(2,self.m_motoNeurones)):
				value = dict()
				value['score'] = 0.0
				value['id'] = i #corresponds to the output activation binary description
				self.m_sublayer[binInput].append(value)
			
		output = self.getCandidateOutput( self.m_lastBinInput )
		
		self.last_activated_output_key = self.getCandidateOutputKey( self.m_lastBinInput )
		mem_key = self.last_activated_output_key
		self.last_activations.append(mem_key)
		if len(self.last_activations)>self.last_activations_size:
			self.last_activations.pop(0)
			
		return output['id']
		
	#now it implements a simple best result condition but can use other methods 
	def getCandidateOutput(self,lastInput):
		candidate = None
		for key in self.m_sublayer[lastInput]:
			#print("evalating: ", key, "  --->  ",key['id'])
			if (candidate == None) or (candidate['score'] < key['score']):
				candidate = key
		return candidate
		
		#now it implements a simple best result condition but can use other methods 
	def getCandidateOutputKey(self,lastInput):
		candidate = None
		candidateKey = 0
		for key in self.m_sublayer[lastInput]:
			if (candidate == None) or (candidate['score'] < key['score']):
				candidate = key
				candidateKey = key['id']
		return candidateKey
		
	#set the feed for the last output
	def feedback(self,feed):
		
		if not('last_activated_output_key' in dir(self)):
			return
		key = self.last_activated_output_key #self.getCandidateOutputKey( self.m_lastBinInput )
		self.m_sublayer[self.m_lastBinInput][key]['score'] = self.m_sublayer[self.m_lastBinInput][key]['score'] + feed
		
		for key in self.last_activations:
			self.m_sublayer[self.m_lastBinInput][key]['score'] = self.m_sublayer[self.m_lastBinInput][key]['score'] + feed
		
		
#it manages the base of brain and in addition it keep memories
class Brain():
	def __init__(self,senseNeurones,motoNeurones,memInputSize,memOutputSize,feedBackwardSize=1):
		#super(Brain,self).__init__()
		self.m_senseNeurones = senseNeurones
		self.m_motoNeurones = motoNeurones
		self.m_memInputSize = memInputSize
		self.m_memOuputSize = memOutputSize
		
		self.m_neuroBase = NeuroBase(senseNeurones+(memInputSize*senseNeurones)+(memOutputSize*motoNeurones),motoNeurones,feedBackwardSize)
		self.m_memInput = "".zfill(memInputSize*senseNeurones)
		self.m_memOutput = "".zfill(memOutputSize*motoNeurones)
		
	def activateInput(self,binInput):
		
		#print( "input layer: ", self.itos(binInput,self.m_senseNeurones) + self.m_memInput + self.m_memOutput )
		output = self.m_neuroBase.activate( self.stoi( self.itos(binInput,self.m_senseNeurones) + self.m_memInput + self.m_memOutput) )
		
		if self.m_memInputSize>0:
			self.m_memInput = self.m_memInput[:self.m_senseNeurones*(self.m_memInputSize-1)]
			self.m_memInput = self.itos(binInput,self.m_senseNeurones) + self.m_memInput
			
		if self.m_memOuputSize>0:
			self.m_memOutput = self.m_memOutput[:self.m_motoNeurones*(self.m_memOuputSize-1)]
			self.m_memOutput = self.itos(output,self.m_motoNeurones) + self.m_memOutput
			
		#print( "output layer: ", self.itos(output,self.m_motoNeurones) )
		return output
	
	"""
		atThisInput = the bits values not considering the memories
		maskBinInput = at 0 the bits to consider important for the decision
		expectedOutput = the output to expect
	"""
	def teach(self,atThisInput,maskBinInput,expectedOutput,strength):
		lenInput = self.m_senseNeurones+self.m_senseNeurones*self.m_memInputSize+self.m_motoNeurones*self.m_memOuputSize
		for bi in range(0,pow(2,lenInput)):
			for ii in range(0,pow(2,self.m_motoNeurones)):
				binInput = bi & ((maskBinInput<<self.m_senseNeurones*self.m_memInputSize+self.m_motoNeurones*self.m_memOuputSize)+(pow(2,self.m_senseNeurones*self.m_memInputSize+self.m_motoNeurones*self.m_memOuputSize)-1))
				binInput = binInput ^ (atThisInput<<self.m_senseNeurones*self.m_memInputSize+self.m_motoNeurones*self.m_memOuputSize)
				output = self.m_neuroBase.activate( self.stoi( self.itos(binInput,lenInput)) )
				if output==expectedOutput:
					self.m_neuroBase.feedback(strength)
					#print("at this input: " + self.itos(binInput,lenInput) + "     setting output: " + self.itos(output,self.m_motoNeurones) )
				else:
					self.m_neuroBase.feedback(-strength)
	
	def feedback(self,feed):
		self.m_lastFeed = feed
		self.m_neuroBase.feedback(feed)
	
	def itos(self,val,size):
		ret = bin(val)[2:]
		ret = ret.zfill(size)
		return ret
		
	def stoi(self,val):
		return int(val,2)
		
		
		
		
# possbility to create a super-stratus layer over the brain that does not consider the binary input but the strenght of an input
# coverting it into a series of binary possible relevat input. These relevant possible input combination can be 
# evaluated (and so kept in consideration) by another binary (probably the best solution) network or by a sequential testing
		
"""
HOW IT WORKS
	The attention strategy used from the uman brain is based on the concept of variations.
	For example:
		Looking at a land horizon, there is a lighthouse. It's the first think you will see, it grabs the attention.
		But, after a brief curious look, it seems to be not important because its repetitive blinking.
		Hey, that's a wind, the three moves.. and than not important... and so on
		
	So, as explained, the changes in the inputs are the basic concept. It's important to reproduce the mechanism 
	thanks to the brain remove the importance on the repetitive situation.
	
	And so, what about the introspective attention? When a brain thinks? ...
	
	Wait wait. 
	Contiuing the example:
		A killer is behind you, no other things are important. Here is only the killer and your savage.
	
	There is something of intelligent on this. A separate network? I don't know. But looking in my memories,
	I remember that, a part of brain, called brainstem, is dedicated to the savage ad survival functions.
	So, considering this, the attention system can be implemented using another neural network.
	
WHAT IT DOES
	It seems to select, at base principle, between different sense organs. And in additin, it transfer the attention to the
	introspection.
	When a new input comes to the brain, the "animal" drives all the sensors to the source of the input. When someone touches 
	your hand, you feel the touch and try to drive your eye on the sensing part of the skin, or differently to the person 
	who have touched you.
	This is incomplete.. The search of the person who have touched you is a complex operation. It's important to find the basic
	thing.
	
	When it drives other sensors to the source of difference, it try to get more information about it. Well.
	When you are reading a book, you are basically unable to ear other things. So, why? Because, to interprete the content
	of the first source it can't broke that flow of infotmation... mmm... because the different concepts are related to each other.
	It seems to be right.
	
	The important elements found:
		- the driving of other sense organs to the source of changes
		- the filter of other inputs!
		
	The filter.
	Yes, because earing the television, and focusing on it your attention, makes other sounds to be discarded.
	Discarded or... Or it's possible that the output for other inputs are null.
	In the case of filtering the situation becomes hard to implement. In the second solution, we have to do nothing.
	
AND SO
	Looking at a bomb, I know that it can explode (and cause an high sound level) because I looked at it exploding and earing 
	the sound (simultaneously). Whitout attention I need a lot of experiences to connect the cause/effect relation ( and so a 
	lot of time is required to "understand" ).

IMPLEMENTATION AND TESTING
	What to do:
		Increase the complexity of the base network, dividing the inputs in groups (input organs).
		Or differently, a puzzle of base network can be attached to get a more flexible brain. I prefer this solution
		but, can it work?
		
		
		
IMPORTANTE NOTA
	L'attenzione decide su quali input bisogna decidere l'output e cosa deve andare nella memoria a breve termine
"""

b=Brain(2,1,1,1)
b.activateInput(1)