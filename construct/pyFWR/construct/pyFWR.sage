from sage.structure.sage_object import SageObject


# class StateSpace( SageObject):
# 	# construct
# 	def __init__(self, A, B, C, D, Te, symbols={}):
# 		self.A = A
# 		self.B = B
# 		self.C = C
# 		self.D = D
# 		self.Te = Te	# sampling period (in s) : 0 for continus time, -1 for discrete time unknown
# 		self.symbols = symbols	# dict of symbols and their numerical values
# 	
# 	# l2 norm
# 	def l2norm(self):
# 		# evaluate the system
# 		if symbols:
# 			A = self.A.substitute(symbols).n()
# 			B = self.B.substitute(symbols).n()
# 			C = self.C.substitute(symbols).n()
# 			D = self.D.substitute(symbols).n()
# 		else:
# 			A = self.A
# 			B = self.B
# 			C = self.C
# 			D = self.D
# 		return 0


def sa2ma_string(M):
	if M.ncols()==0 or M.nrows()==0:
		return "zeros(%d,%d)"%(M.nrows(), M.ncols())
	else:
		return matlab.sage2matlab_matrix_string(M)
#-> faire un ticket dans sage, avec correction


def nontrivial(X,epsilon):
	Y=copy(X)
	def _nv(x):
		if abs(x)<epsilon or abs(x-1)<epsilon or abs(x+1)<epsilon:
			return 0
		else:
			return 1

	return Y.apply_map( _nv )


class pyFWR( SageObject):

	# constructor
	def __init__(self, J,K,L,M,N,P,Q,R,S, name, symbols={}, plant=(),epsilon=1e-6):
 		self.J = J
 		self.K = K
 		self.L = L
 		self.M = M
 		self.N = N
 		self.P = P
 		self.Q = Q
 		self.R = R
 		self.S = S
 		self.name = name		# name of the realization
 		self.symbols = symbols	# dict of symbols and their numerical values
 		self.plant = plant		# = (Aplant, Bplant, Cplant, Dplant)

		self.deltaJ, self.deltaK,self.deltaL, self.deltaM, self.deltaN,  self.deltaP, self.deltaQ, self.deltaR, self.deltaS = [ nontrivial(X,epsilon) for X in [J,K,L,M,N,P,Q,R,S] ]
	
		# dimensions
		#l,m,n,p = self.__check_dimensions__()
		
		# A_Z, B_Z, C_Z, D_Z
		invJ = J**-1
		self.AZ = K*invJ*M + P
		self.BZ = K*invJ*N + Q
		self.CZ = L*invJ*M + R
		self.DZ = L*invJ*N + S
		
		# A_Zbar, B_Znar, C_Zbar, D_Zbar
		# (=A_Z, B_Z, C_Z, D_Z) if there is no plant
		if plant:
			#todo
			print "todo"
		else:
			self.AZb = self.AZ
			self.BZb = self.BZ
			self.CZb = self.CZ
			self.DZb = self.DZ
		
		# M_1, M_2, N_1, N_2
		#if plant:
			#todo
			#pass
		#else:
			#self.M1 = block_matrix( 1,3, [ self.K*invJ, identity_matrix(n)
			#pass

		
	# return the Z matrix
	def Z(self):
		return block_matrix( 3, 3, [-self.J, self.M, self.N, self.K, self.P, self.Q, self.L, self.R, self.S], subdivide=True)
	def deltaZ(self):
		return block_matrix( 3, 3, [-self.deltaJ, self.deltaM, self.deltaN, self.deltaK, self.deltaP, self.deltaQ, self.deltaL, self.deltaR, self.deltaS], subdivide=True)
		
	# latex output
	def _latex_(self):
		return latex(self.Z())

	
	# text output
	def _repr_(self):
		return "FWR Object : "+self.name
	
	# return the size of the realization
	#def size(self):
	#	return (self.l, self.m, self.n, self.p)


	def dHdZ(self):
		T1 = matlab.eval ('R = FWR( %s,%s,%s,%s,%s,%s,%s,%s,%s );'%(tuple(sa2ma_string(x.substitute(self.symbols).n()) for x in [self.J, self.K, self.L, self.M, self.N, self.P, self.Q, self.R, self.S] )))
		
		print ('R = FWR( %s,%s,%s,%s,%s,%s,%s,%s,%s );'%(tuple(sa2ma_string(x.substitute(self.symbols).n()) for x in [self.J, self.K, self.L, self.M, self.N, self.P, self.Q, self.R, self.S] )))
		
		
		
		T2 = matlab.eval('[M MZ] = MsensH(R);')
		return matrix(RR,matlab('MZ'))
		
	
	def error_tf_normalized(self):
	
		def _lg2(x):
			if not x:
				return x
			elif x!=0:
				return 2**floor(log(abs(x))/log2.n())
			else:
				return 0 		# don't care
				
		dHdZ = self.dHdZ()	
		log2Z = self.Z().substitute(values).n().apply_map( _lg2)
		M1 = dHdZ.elementwise_product(log2Z).elementwise_product(self.deltaZ())

		sum = M1.norm('frob')**2
		
		sum2 = 0
		for theta in values:
			M2 = dHdZ.elementwise_product( self.Z().derivative(theta).substitute(values).n() )*_lg2( values[theta] )
			sum2 += M2.norm('frob')**2
		
		return sum,sum2,sum+sum2





		
		
def DirectFormII( num, den, symbols={}):
	
	# normalisation des coefs
	a0 = den[0]
	num = [ c/a0 for c in num ]
	den = [ c/a0 for c in den ]
	n = max(len(num),len(den))
	
	J = matrix(1,1,1)
	K = block_matrix(2,1,[1,zero_matrix(n-2,1)],subdivide=False)
	L = matrix(1,1,num[0])
	M = matrix([ -c for c in den[1:] ])
	N = matrix(1,1,1)
	P = block_matrix(2,2,[0, zero_matrix(1,1), identity_matrix(n-2), 0],subdivide=False)
	Q = zero_matrix(n-1,1)
	R = matrix(1,n-1,num[1:])
	S = matrix(1,1,0)
	
	return pyFWR( J, K, L, M, N, P, Q, R, S, name='Direct Form II', symbols=symbols )
	
	
	