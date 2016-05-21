""" diagram module
	Hold diagram informations : blocks, lines and relationship 
"""


from lxml import etree
from blocks import *

class System(object):

	def __init__(self, xmlStr, constants):
		"""
		Parameters:
		- xmlStr: string containing the xml
		"""
		self.blocks = {} # a dictionary of sid:block
		self.lines = []
		self.equations = []
		self.constants = constants

		self.tree = etree.fromstring(xmlStr) # load xml from file
		self.syspath = "/ModelInformation/Model/System"

		# For the given system model, build blocks and lines list
		self.blocks, self.lines = self.parsesys(self.tree, self.syspath)
		self.flattendesign() # eliminate subsys block box 
		self.fillblocksiolist() # update in/out blocks list of all blocks
		self.equations = self.buildequations() # build a simplified relationship of all blocks



	def parsesys(self, etree, syspath):		
		"""Give blocks  and lines objects lists	from Block and Line elements in XML
			args : etree of the xml file / path of the <System> tag in the xml
			return : blocks dict  and lines list"""

		blocks = {}
		lines = []
		blockclass = {'Gain':Gain, 'Delay':Delay, 'Sum':Sum, 'SubSystem':SubSystem, 'Inport':Inport, 'Outport':Outport}

		for mysys in etree.xpath(syspath):
			#print etree.getpath(mysys)
			# iter() instead of findall(): recursive search
			blockels = mysys.iter("Block") 
			lineels = mysys.iter("Line")

		## Fill blocks dict
		for b in blockels:
			blocktype = b.get("BlockType")
			try:
				if blocktype=='Gain':
					newblock = blockclass[blocktype](b,self.constants)
				else:
					newblock = blockclass[blocktype](b)
			except KeyError:
				print blocktype + " is an unsupported block"
				sys.exit()
			blocks[b.get("SID")] = newblock 
	
		## Fill lines list
		for l in lineels:
			# find all children 'P' tag
			# there must be only one 'Src
			for p in  l.findall("P"):  
				if p.get("Name") == "Src": 
					srctext = p.text

			# find all 'P' tag recursively
			# there can be more than one 'Dst'
			for p in l.iter("P"):  
				if p.get("Name") == "Dst": 
					dsttext = p.text
					newline = Line(srctext, dsttext)
					lines.append(newline)

		return (blocks,lines)



	def flattendesign(self):
		""" this function eliminate subsystem box by shortcutting their I/O port
			args : blocks list(dict) / lines list"""
		# Susbsystem Processing
		# Manage connection in lines ( can be done in block)
		# --> do it before block inlist / outlist update ( this step rely on lines)
		print "\nSubsystem processing ..."
		i=0
		for subsys in [ b for b in self.blocks.values() if b.type == 'SubSystem']:
			i += 1
			print "subsys : ",i , subsys
			# Subsystem input shortcuting
			for port in range(1, subsys.inports+1):
				# Search block feeding SubSystem
				for line in self.lines:
					if line.dstsid == subsys.sid and line.dstport == str(port):
						sblock = line.srcsid
						sport = line.srcport
						inputline = line
						print "-- inport --"
						print line 
						break
			
				# check existence of inputline ( inport connection)	
				try: 
					inputline
				except NameError:
					print "error - SubSystem : Inport not connected"
					sys.exit()

				# Search in Subsystem connection
				for line in subsys.ioconnex:
					if line.srcsid == subsys.sid and line.srcport == str(port):
						iblock = line.dstsid
						iport = line.dstport
						inportline = line
						print line
						break
				
				try:
					inportline
				except NameError:
					print "error - SubSystem : internal connection"
					sys.exit()

				# Search connected blocks in Subsystem and remake connection
				# (put in a try except block)
				for line in [l for l in self.lines if l.srcsid == iblock and l.srcport == iport]:
					line.srcsid = sblock	
					line.srcport = sport

				# Clean 2 useless lines and 1 block for each port
				self.lines.remove(inputline)	
				subsys.ioconnex.remove(inportline)
				del self.blocks[iblock]	

			# SubSystem Output shortcuting
			for port in range(1, subsys.outports+1):
				# Search line connected to outport in Subsystem
				for line in subsys.ioconnex:
					if line.dstsid == subsys.sid and line.dstport == str(port):
						oblock = line.srcsid
						oport = line.srcport
						outportline = line
						print "-- ouport --"
						print line
						break

				try:
					outportline
				except NameError:
					print "error- SubSystem : internal connection"
					sys.exit()

				# Search block feeding the outport
				for line in self.lines:
					if line.dstsid == oblock and line.dstport == str(oport):
						sblock = line.srcsid
						sport = line.srcport
						sline = line
						print line
						break

				try:		
					sline
				except NameError:
					print "error - Subsystem : Ouport not connected"

				# Search connected blocks in Subsystem
				# ( put in a try except block)
				for line in [l for l in self.lines if l.srcsid == subsys.sid and l.srcport == str(port)]:
					line.srcsid = sblock	
					line.srcport = sport

				# Clean 2 useless lines for each port
				self.lines.remove(sline)	
				subsys.ioconnex.remove(outportline)
				del self.blocks[oblock]

			# delete Subsystem block from blocks list
			del self.blocks[subsys.sid]
	
		# Check subsys variable existence
		try:
			subsys
		except NameError:
			print " no SubSystem"
		# End of SubSystem processing




	def fillblocksiolist(self):
		""" Update blocks inlist and outlist attribute : linked blocks
			inlist : list (dict) of all blocks connected to input ports
			outlist : list of all blocks connected to output port"""
		# need blocks and lines list
		for line in self.lines:
			self.blocks[line.dstsid].inlist[line.dstport] =  self.blocks[line.srcsid]
			self.blocks[line.srcsid].outlist.append(self.blocks[line.dstsid])



	def buildequations(self):
		"""This function build a list of equations object.
			Each "equation" contain for a given block SID its list of 
			input blocks with their associated coefficients"""
		# All next processing will be done on equations list
		equations = []
		for bsid in self.blocks.keys(): 
			neweq = Equation(bsid)
			# we list here all inputs blocks for a given block
			neweq.termes = dict((block.sid, 1.0) for block in self.blocks[bsid].inlist.values()) # python2.6

			# for a gain block : give right coeff for all inputs
			#  bi : input block / termes[bi]: bi coeff
			if self.blocks[bsid].type == 'Gain': 
				for bisid in neweq.termes.keys():
					neweq.termes[bisid] = self.blocks[bsid].gain 
			
			# sum sign handling
			# affect -1.0 to coeff if the sign corresponding to input block is '-'
			if self.blocks[bsid].type == 'Sum':
				curblock = self.blocks[bsid]
				for pi in curblock.inlist.keys():
					if curblock.inportsign[int(pi)-1] == '-': # port number start on '1'
						bi = curblock.inlist[pi] # inlist = {porti:blocki} : block feeding the given input port 
						neweq.termes[bi.sid] = 0 - 1.0 
			
				
			if self.blocks[bsid].type != 'Inport':
				equations.append(neweq)
		return equations

	
	def summerge(self):
		"""To merge cascading 'Sum' Blocks
			Must be called N times if there is N cascading addition"""
		# Important : Must be called before expandeqgain : to detect only the direct connected Sum
		# ( merge is handled in equations list) 
		for eq in self.equations:
			bout = self.getblockbysid(eq.out)
			if bout.type == 'Sum':
				for inp in eq.termes.keys(): # a copy of the dict key / dict is changing during iteration
					inpb =  self.getblockbysid(inp)
					inpcoeff = eq.termes[inp]
					assert abs(inpcoeff) == 1.0 # Sum have no gain
					if inpb.type == 'Sum' and len(inpb.outlist) == 1: # merge if it's not used somewhere else
						# handle here sum sign propagation: coeff2*inpcoeff  
						d = dict((inp2, coeff2*inpcoeff) for (inp2,coeff2) in self.getequation(inp).termes.items())
						eq.termes.update(d)
						del eq.termes[inp]

						subequa = self.getequation(inp)
						self.equations.remove(subequa)


	def expandeqgain(self):
		"""Put gain as Sum coefficient"""
		# It will act on  Sum bloc equation
		# now, we assume there is no cascading gain block
		# and gain will always be before Sum block
		#
		# ? keep cascading gain block : test if the current block is a sum
		# 								and create also an inter var for upstream gain block
		for eq in self.equations:
			for eqin in eq.termes:
				if self.blocks[eqin].type == 'Gain':
					oldgain = eq.termes[eqin]	
					del eq.termes[eqin] 

					gaineq = self.getequation(eqin)
					for gin in gaineq.termes:
						eq.termes[gin] = gaineq.termes[gin] * oldgain


	def isequationused(self,eq): 
		""" Test if an equation is usefull or not
				therefore, we can remove it from list"""
		# build list of all right termes in equations
		# Can not be called while equations is modified
		# to be improved by using dico
		inputs = [] 
		for eq in self.equations:
			print eq
			for block in eq.termes.keys():
				if block not in inputs:
					inputs.append(block)	

			print inputs
	
		if eq.out in inputs:
			return True
		else:
			return False


	def getequation(self, bsid):
		""" Get equation corresponding to a given block sid""" 
		# penser a faire un dico
		for eq in self.equations:
			if eq.out == bsid:
				return eq					
		return None


	def printequations(self):
		print "out {termes:coeff}"
		for eq in self.equations:
			print eq.out, eq.termes


	def getblockbysid(self, sid):
		return self.blocks[sid]

	def getinblocks(self):
	# return a list of all Inports blocks
		inports = []
		for sid in self.blocks.keys():
			block = self.getblockbysid(sid)
			if block.type == 'Inport':
				inports.append(block)
		return inports
	
	def getoutblocks(self):
	# return a list of all Outports blocks
		outports = []
		for sid in self.blocks.keys():
			block = self.getblockbysid(sid)
			if block.type == 'Outport':
				outports.append(block)
		return outports

	def getblocksbytype(self,type):
	# return a list of blocks with a given type : 'Sum', 'Delay', ...
		tblocks = []
		for sid in self.blocks.keys():
			block = self.getblockbysid(sid)
			if block.type == type:
				tblocks.append(block)
		return tblocks	
	
	def printblocks(self):
		print "\x1b[32m\nBlocks list : ", len(self.blocks)
		print "\x1b[0m[SID, BlockType, Name, inputs]"
		for sid in self.blocks:
			block = self.getblockbysid(sid)
			print block.sid, block.type, block.name, [b.sid for b in block.inlist.values()] 

	def printlines(self):
		print "\x1b[32m\nLines list : ", len(self.lines)
		print "\x1b[0m[Src, Dst]"
		for line in self.lines:
			print line

	def getsysvar(self):
		""" Return classified System variables name lists
			input, state, temporary result and output
			(u, x, t, y)"""	
		# there is no special operation in u and x : we can rely on blocks list 
		u = [b.name for b in self.getinblocks()] 
		x = [b.name for b in self.getblocksbytype('Delay')]
		# t and y are modified so we rely on equation list ( this hold final result on block diag processing)
		sum = [self.getblockbysid(teq.out) for teq in self.equations if self.getblockbysid(teq.out).type == 'Sum']
		t = [bs.name for bs in sum if  bs.isoutblock() == False]
		y = [bs.name for bs in sum if  bs.isoutblock() == True]
		# add support for output on Gain block
		g = [xeq.out for xeq in self.equations if self.getblockbysid(xeq.out).type == 'Gain']
		y += [s for s in g if  self.getblockbysid(s).isoutblock() == True]
		return (u,x,t,y)

	

class Equation(object):
	def __init__(self,eqid):
		self.out = eqid
		self.termes = {}

	def __str__(self):
		return str(self.out) + "-" + str(self.termes)

