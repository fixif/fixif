"""
sif modules
used to deduce SIF Matrix from SoP equations
"""

__author__ = "Maminionja Ravoson"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Maminionja Ravoson", "Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures.Simulink.diagram import Equation

class Sif(object):
	def __init__(self, l, m, n, p):
		self.l = l # intermediary calculation variables number in the system
		self.m = m # input nbr
		self.n = n # state nbr
		self.p = p # output nbr

		def mat( a, b):
			# Function : Buid a matrix with a given size
			m = [[0.0 for i in range(b)] for j in range(a) ]
			return m
		#Build SIF matrix
		self.J = mat(l,l)
		self.K = mat(n,l) 
		self.L = mat(p,l)
		self.M = mat(l,n)
		self.P = mat(n,n)
		self.R = mat(p,n)
		self.N = mat(l,m)
		self.Q = mat(n,m)
		self.S = mat(p,m)			

	
		
	def build(self, system):
		# Equations and Blocks list in the system are needed for SIF generation
		# /!\ Matrix element value placement depend on variables order
		u = [u.sid for u in system.getinblocks()]
		x = [xeq.out for xeq in system.equations if system.getblockbysid(xeq.out).type == 'Delay']
		sum = [teq.out for teq in system.equations if system.getblockbysid(teq.out).type == 'Sum']
		t = [s for s in sum if  system.getblockbysid(s).isoutblock() == False]
		y = [s for s in sum if  system.getblockbysid(s).isoutblock() == True]
		# add support for output on Gain block
		g = [xeq.out for xeq in system.equations if system.getblockbysid(xeq.out).type == 'Gain']
		y += [s for s in g if  system.getblockbysid(s).isoutblock() == True]

		# TODO: dirty work, just for test, clean useless variables and computation
		# for block labeling : type+sid
		self.u = [system.getblockbysid(i).label for i in u]
		self.x = [system.getblockbysid(i).label for i in x]
		self.t = [system.getblockbysid(i).label for i in t]
		self.y = ["y"+system.getblockbysid(i).label[1:] for i in y]

		# ________________________________________________________
		#
		# patch if there is output in the termes of the equations
		# blocks list
		bsids = []
		for block in system.blocks:
			bsids.append(block)
		# get a new free SID
		def get_new_sid(sids):
			nb = len(sids) + 2
			for tsid in range(1,nb):
				if tsid not in sids:
					sid = tsid
			sids.append(sid) #update local blocks list
			return str(sid) 
		# correct equations
		for outb in y:
			for eq in system.equations:
				feedback = False
				for block in eq.termes:
					if block == outb:
						feedback = True
						break	
				if feedback:
					t.append(outb)
					y.remove(outb)
					new_out = get_new_sid(bsids)
					#bsids.append(new_out) #update done in get_new_sid()
					# add a new equation
					neweq=Equation(new_out)
					neweq.termes[outb] = 1.0
					system.equations.append(neweq)
					y.append(new_out)
					#correct matrix size
					self.l +=1
					def mat( a, b):
						m = [[0.0 for i in range(b)] for j in range(a) ]
						return m
					self.J = mat(self.l,self.l)
					self.K = mat(self.n,self.l) 
					self.L = mat(self.p,self.l)
					self.M = mat(self.l,self.n)
					self.N = mat(self.l,self.m)
					break
		# for block labeling : type+sid
		self.u = ["u"+str(i) for i in u] #[system.getblockbysid(i).label for i in u]
		self.x = ["x"+str(i) for i in x] #[system.getblockbysid(i).label for i in x]
		self.t = ["t"+str(i) for i in t] #[system.getblockbysid(i).label for i in t]
		self.y = ["y"+str(i) for i in y] #["y"+system.getblockbysid(i).label[1:] for i in y]
		#system.printequations()
		#________________________________________________________

		# Fill SIF matrix
		for eq in system.equations:
			if eq.out in y: # output eq
				for block,coeff in eq.termes.items(): # scan current equation inputs
					if block in t:
						self.L[y.index(eq.out)] [t.index(block)] = coeff
					elif block in x:
						self.R[y.index(eq.out)] [x.index(block)] = coeff
					elif block in u:
						self.S[y.index(eq.out)] [u.index(block)] = coeff
		
			elif eq.out in x: # state eq
				for block,coeff in eq.termes.items(): # scan current equation inputs
					if block in t:
						self.K[x.index(eq.out)] [t.index(block)] = coeff
					elif block in x:
						self.P[x.index(eq.out)] [x.index(block)] = coeff
					elif block in u:
						self.Q[x.index(eq.out)] [u.index(block)] = coeff
		
			elif eq.out in t: # intermediate eq
				for block,coeff in eq.termes.items() : # scan current equation inputs
					if block in t:
						self.J[t.index(eq.out)] [t.index(block)] = str(0-coeff)
					elif block in x:
						self.M[t.index(eq.out)] [x.index(block)] = coeff
					elif block in u:
						self.N[t.index(eq.out)] [u.index(block)] = coeff


		# additional assignement for J matrix
		for i in range(self.l):
			for j in range(self.l):
				if i == j:
					self.J[i][j] = 1.0 

	
	
	def __str__(self):
		def strmat(mat):
			# Generate string for a given matrix
			smat = ""
			for line in mat:
				smat += str(line)+"\n"
			return smat

		# Generate SIF matrix string 
		return "\nJ:" + str(self.l) + 'x' + str(self.l) + "\n" + strmat(self.J)+ \
		 "\nK:" + str(self.n) + 'x' +str(self.l) + "\n" + strmat(self.K) + \
		 "\nL:" + str(self.p) + 'x' +str(self.l) + "\n" + strmat(self.L) + \
		 "\nM:" + str(self.l) + 'x' +str(self.n) + "\n" + strmat(self.M) + \
		 "\nP:" + str(self.n) + 'x' +str(self.n) + "\n" + strmat(self.P) + \
		 "\nR:" + str(self.p) + 'x' +str(self.n) + "\n" + strmat(self.R) + \
		 "\nN:" + str(self.l) + 'x' +str(self.m) + "\n" + strmat(self.N) + \
		 "\nQ:" + str(self.n) + 'x' +str(self.m) + "\n" + strmat(self.Q) + \
		 "\nS:" + str(self.p) + 'x' +str(self.m) + "\n" + strmat(self.S) + \
		"\n\nt:" + str(self.t) + \
		"\nx:" + str(self.x) + \
		"\nu:" + str(self.u) + \
		"\ny:" + str(self.y) 

	
	def reorganize(self):
		""" Make J Matrix lower triangular 
			and reorder affected matrix (M, N, K and L)"""
		# need more test <--
		# function to build matrix 
		def mat( a, b):
			# Function : Buid a matrix with a given size
			m = [[0.0 for i in range(b)] for j in range(a) ]
			return m
	
		N = self.l # size of J	
		nodes = {}

		def ladj(J, i): # i : column number
			"""Function that build the list of forward nodes for each node i.
			{node:[node, state, [list of forward nodes]]}"""
			col = [line[i] for line in J]
			adj_list = [index for index, elt in enumerate(col) if (elt != 0 and index != i)]
			return  adj_list 

		# build list of forwards nodes for all nodes
		# --> to browse the graphe easily	
		for i in range(N): # scan all column
			nodes[i] = [i] 
			nodes[i].append(0) 
			nodes[i].append(ladj(self.J,i))		
		
		# toplogical sort by DFS algo :
		# unmarked : 0
		# tempo mark : 1
		# perm mark : 2
		N_VISITED = 0
		lorder = []
		def visit( node , n_visited):
			#print node[0], node[1], node[2]
			
			if node[1] == 1:
				print("\nerror - not a D.A.G !!!")
				sys.exit()
			if node[1] == 0: # not yet visited	
				node[1] = 1
				for m in node[2]:
					n_visited = visit(nodes[m],n_visited)
				node[1] = 2
				n_visited += 1 
				lorder.append(node[0]) # <-- this is the key element here
			return n_visited
		
		# order list
		i=0 # i : index node
		while N_VISITED < N:
			if nodes[i][1] == 0:
				N_VISITED = visit(nodes[i], N_VISITED)
			i +=  1
			if i == N:
				i = 0
		lorder.reverse() # the aim is to have the lorder vector


		# Reorganize J Matrix
		# ( when we have the order of calculation, we can reorganize line then column of J
		#  and accordingly M, N lines and K, L coulumn )
		Jn = mat(N,N)
		# order line : equation order
		for i in range(N): 
			Jn[i] = self.J[lorder[i]]
		# order also column (for var vector consistency)
		self.J = mat(N,N)
		for i in range(N): 
			for j in range(N): 
				self.J[i][j] = Jn[i][lorder[j]]
			#	if i == j:
			#		self.J[i][j] = 1.0


		# Reorganize M and N matrix : order line (equation order)
		# M matrix line reordering
		Mn = mat(self.l,self.n)
		for i in range(self.l): 
			Mn[i] = self.M[lorder[i]]
		self.M = Mn
		# N matrix line reordering
		Nn = mat(self.l,self.m)
		for i in range(self.l): 
			Nn[i] = self.N[lorder[i]]
		self.N = Nn
		#TODO: do J, M and N lines together 


		# Reorganize K and L matrix : order column (variables order)
		# K matrix column reordering
		Kn = mat(self.n,self.l)
		for i in range(self.n): 
			for j in range(self.l): 
				Kn[i][j] = self.K[i][lorder[j]]
		self.K = Kn
		# L matrix column reordering
		Ln = mat(self.p,self.l)
		for i in range(self.p): 
			for j in range(self.l): 
				Ln[i][j] = self.L[i][lorder[j]]
		self.L = Ln

		#Reorganize only t vector
		tn = self.t[:]
		for i in range(N):
			tn[i] = self.t[lorder[i]]
		self.t = tn
	
