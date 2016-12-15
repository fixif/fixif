"""
blocks modules
used to access Blocks and Lines parameters in Simulink Diagram File (xml)
dependance : lxml.etree
arg : each block take in its constructor an etree element, a <tag> form xml 
"""


__author__ = "Maminionja Ravoson"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Maminionja Ravoson", "Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


class Block(object):
	#nbr = 0
	def __init__(self, bel):
		# dependance : lxml.etree
		# arg : etree element - <Block> tag from a slx diagram
		self.sid = bel.get("SID") # find a tag attribute named SID
		self.name = bel.get("Name")
		self.type = bel.get("BlockType")
		self.label = ""
		self.inlist = {}
		self.outlist = []
		#Block.nbr += 1

	def isoutblock(self):
		"""to know if a block is connected to Outport (Output)"""
		# used to determine outputs variables
		for block in self.outlist:
			if block.type == 'Outport':
				return True
		return False

	def __str__(self):
		return self.sid + '-' + self.type + '-' + self.name


class Gain(Block):
	def __init__(self, bel, constants=None):
		if constants is None:
			constants = {}
		super(Gain, self).__init__(bel)
		self.label = "k"+self.sid

		self.gain = 1.0 # assign 1.0 if not present in P tag ( not given by user in diagram)
		for p in bel.findall("P"):
			if p.get("Name") == "Gain":
				if p.text in constants:
					self.gain = constants[ p.text ]
				else:
					# TODO: Warning!! FLOAT conversion !!!!
					#TODO: manage when the conversion is not possible (ie a constant that is not in the constants dictionary
					self.gain = float(p.text)



	def ischained(self):
		"""to know if there is a Gain block in the output of current Gain block
			--> to be used to handle Gain chain"""
		for block in self.outlist:
			if block.type == 'Gain':
				return True
		return False


class Delay(Block):
	def __init__(self, bel):
		super(Delay,self).__init__(bel)
		self.delay = 1 # assign 1 if not present in P tag ( not given by user in diagram)
		self.label = "x"+self.sid
		for p in bel.findall("P"):
			if p.get("Name") == "DelayLength":
				self.delay = int(p.text)


class Sum(Block):
	def __init__(self, bel):
		super(Sum, self).__init__(bel)
		self.outports = 1
		self.inports = 2
		self.inportsign = []
		self.label = "t"+self.sid

		# Determine I/O port number
		for p in bel.findall("P"):
			if p.get("Name") == "Ports":
				iotext = p.text # [2, 1]-> 2 inputs / 1 output

				n = len(iotext)
				iochar = iotext[1:n-1].partition(',')
				self.inports = int(iochar[0])
				self.outports = int(iochar[2])

		# parse input sign string
		for p in bel.findall("P"):
			if p.get("Name") == "Inputs":
				signtext = p.text # |++ -> 1st:+ / 2nd:+
		# process inputs sign string and build input sign list
		for c in signtext:
			if c == '+' or c == '-':
				self.inportsign.append(c)

		# One sign <-> One input port
		assert len(self.inportsign) == self.inports


	def __str__(self):
		return self.sid + '-' + self.name + '-' + str(self.inportsign)


class SubSystem(Block):
	def __init__(self, bel):
		super(SubSystem, self).__init__(bel)
		self.subsysel = bel.find("System") # find a tag (element)
		self.outports = 0
		self.inports = 0
		self.ioconnex = []
		self.label = "sub"+self.sid

		# Find Subsystem I/O port number
		for p in bel.findall("P"):
			if p.get("Name") == "Ports":
				iotext = p.text # [2, 1]-> 2 inputs / 1 output

				n = len(iotext)
				iochar = iotext[1:n-1].partition(',')
				self.inports = int(iochar[0])
				self.outports = int(iochar[2])

		# Find i/o port connection in subsys
		# Generate an imaginary line for each connextion found
		for b in self.subsysel.findall("Block"): # b:block in the subsys
			if b.get("BlockType") == 'Inport':
				srcb = self.sid
				dstb = b.get("SID")
				srcp = '1'
				for p in b.findall("P"):
					if p.get("Name") == 'Port':
						srcp = p.text
				dstp = '1' # scalar Inport

				srctext = srcb + "#out:" + srcp
				dsttext = dstb + "#in:" + dstp
				newline = Line(srctext, dsttext)
				self.ioconnex.append(newline)

			if b.get("BlockType") == 'Outport':
				srcb = b.get("SID")
				dstb = self.sid
				srcp = '1' # scalar Outport

				dstp = '1'
				for p in b.findall("P"):
					if p.get("Name") == 'Port':
						dstp = p.text

				srctext = srcb + "#out:" + srcp
				dsttext = dstb + "#in:" + dstp
				newline = Line(srctext, dsttext)
				self.ioconnex.append(newline)

		# lines number must match I/O ports number
		assert len(self.ioconnex) == self.inports + self.outports


	def __str__(self): # for debug : just print all generated lines
		strio = ""
		for line in self.ioconnex:
			strio += str(line) + " "
		return strio



class Inport(Block):
	def __init__(self, bel):
		super(Inport, self).__init__(bel)
		self.port = 1
		self.label = "u"+self.sid
		for p in bel.findall("P"):
			if p.get("Name") == "Port":
				self.port = p.text



class Outport(Block):
	def __init__(self, bel):
		super(Outport, self).__init__(bel)
		self.port = 1
		self.label = "y"+self.sid
		for p in bel.findall("P"):
			if p.get("Name") == "Port":
				self.port = p.text



class Line(object):
	nbr = 0
	def __init__(self, srctext, dsttext):
		# Check here srctext and sdttext format SID#in/out:port <--
		self.srcsid = self.getblocknum(srctext) 
		self.dstsid = self.getblocknum(dsttext)
		self.srcport =  self.getportnum(srctext)
		self.dstport =  self.getportnum(dsttext)
		Line.nbr += 1

	def getblocknum(self, str):
		# Getting block number in the line String
		# ex : getblocknum('12#out:1') must return '12'
		b = str.partition('#')
		return b[0]		

	def getportnum(self, str):
		port = str.partition(':')
		return port[2]
	
	def __str__(self):
		return "[" + self.srcsid + ":" + self.srcport + ", " \
					+ self.dstsid + ":" + self.dstport + "]"

#TODO
# params par defaut des blocs:
# dans "/ModelInformation/Model/BlockParameterDefaults"

