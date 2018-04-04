# coding=utf-8

#inclure licence CECILL-C

"""This module only contains the class `pyFWR`, that defines a Finite Wordlength Realization"""


import numpy as np
mat = np.matrix	#alias

__author__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__license__ = "CECILL-C"
__version__ = "$Id$"




def isTrivial(x, epsilon):
	"""indicates if is a trivial parameter or not
	only consider 0, 1 or -1 (+/-epsilon)"""
	return abs(x)<epsilon or abs(x-1)<epsilon or abs(x+1)<epsilon

def nonTrivial(X, epsilon=1e-8):
	"""indicates if the coefficients of the matrix X is trivial or not
	only consider 0, 1 or -1 (+/-epsilon)"""
	return np.vectorize( lambda x:int( not isTrivial(x,epsilon) )) (X)
	


class pyFWR( object):
	"""Class pyFWR..."""
	
	def __init__( self, JtoS, name, delta_epsilon=1e-8):
		"""construit la réalisation
		- JtoS : tuple de matrices J,K,L,M,N,P,Q,R,S
		- name : (string) nom de la réalisation
		- delta_epsilon : seuil de tolérance pour la construction des deltaJ, deltaK, ... deltaS
		"""
		
		# attributes
		self.name = name
		
		# J to S (convert them in matrix)
		self.__J, self.__K, self.__L, self.__M, self.__N, self.__P, self.__Q, self.__R, self.__S = [ np.matrix(X) for X in JtoS]
		# check size
		self.__l,self.__m,self.__n,self.__p = self.__check_dimensions__()
		# build Z
		self.__Z = np.bmat( [ [ -self.J, self.M, self.N ], [ self.K, self.P, self.Q], [ self.L, self.R, self.S ] ] )

		# deltaJ to deltaS
		self.deltaJ, self.deltaK, self.deltaL, self.deltaM, self.deltaN, self.deltaP, self.deltaQ, self.deltaR, self.deltaS = [ nonTrivial(X, delta_epsilon) for X in JtoS ]
		
		# open-loop case
		
		# AZ, BZ, CZ and DZ
		invJ = self.J**-1
		self.__AZ = self.K * invJ * self.M + self.P
		self.__BZ = self.K * invJ * self.N + self.Q
		self.__CZ = self.L * invJ * self.M + self.R
		self.__DZ = self.L * invJ * self.N + self.S
		
		# M1, M2, N1 and N2		
		self.__M1 = np.c_[ self.K*invJ, np.eye(self.__n), np.zeros((self.__n,self.__p)) ]
		self.__M2 = np.c_[ self.L*invJ, np.zeros((self.__p,self.__n)), np.eye(self.__p) ]
		self.__N1 = np.r_[ invJ*self.M, np.eye(self.__n), np.zeros((self.__m,self.__n)) ]
		self.__N2 = np.r_[ invJ*self.N, np.zeros((self.__n,self.__m)), np.eye(self.__m) ]		

		
	@property
	def deltaZ(self):
		"""compute deltaZ from deltaJ to deltaS"""
		return np.bmat( [ [ self.deltaJ, self.deltaM, self.deltaN ], [ self.deltaK, self.deltaP, self.deltaQ], [ self.deltaL, self.deltaR, self.deltaS ] ] )
	
	@deltaZ.setter
	def deltaZ( self, deltaZ):
		"""setter for deltaZ
		udpates deltaJ, deltaK, ..., deltaS"""
		l,m,n,p = self.size
		self.__deltaJ = deltaZ[ 0:l , 0:l ]
		self.__deltaK = deltaZ[ l:l+n , 0:l ]
		self.__deltaL = deltaZ[ l+n:l+n+p , 0:l ]
		self.__deltaM = deltaZ[ 0:l , l:l+n ]
		self.__deltaN = deltaZ[ 0:l , l+n:l+n+m ]
		self.__deltaP = deltaZ[ l:l+n , l:l+n ]
		self.__deltaQ = deltaZ[ l:l+n , l+n:l+n+m ]
		self.__deltaR = deltaZ[ l+n:l+n+p , l:l+n ]
		self.__deltaS = deltaZ[ l+n:l+n+p , l+n:l+n+m ]
	

	
	# properties (for read-only attributes)
	# TODO: maybe use a RO class ?
	Z = property( lambda self: self.__Z )
	J = property( lambda self: self.__J )
	K = property( lambda self: self.__K )
	L = property( lambda self: self.__L )
	M = property( lambda self: self.__M )
	N = property( lambda self: self.__N )
	P = property( lambda self: self.__P )
	Q = property( lambda self: self.__Q )
	R = property( lambda self: self.__R )
	S = property( lambda self: self.__S )
	
	#l = property( lambda self: self.__l )
	#m = property( lambda self: self.__m )
	#n = property( lambda self: self.__n )
	#p = property( lambda self: self.__p )
	
	
	def __str__( self):
		"""display the realization"""
		
		def plural(n):
			"""add a 's' if necessary for plural"""
			return (n>1) and 's' or ''
		
		st = "Realization `%s`\n"%(self.name,)
		st += "It has %d input%s, %d output%s, %d state%s and %d intermediate variable%s\n" % (self.__m,plural(self.__m), self.__p, plural(self.__p), self.__n, plural(self.__n), self.__l, plural(self.__l) )
		st += repr(self.Z)
		return st
		
		
	def __check_dimensions__( self):
		"""Compute the size $l$, $m$, $n$ and $p$ of a FWR realization.
	It also checks the concordance of the size of matrices $J$, $K$, $L$, $M$, $N$, $P$, $Q$, $R$, $S$"""
		
		# P (n,n)
		p1,p2 = self.P.shape
		if p1!=p2:
			raise ValueError, 'error with the dimension of P'
		else:
			n=p1
		
		# J (l,l)
		j1,j2 = self.J.shape
		if j1!=j2:
			raise ValueError, 'error with the dimension of J'
		else:
			l = j1

		# K (n,l)
		k1,k2 = self.K.shape
		if (k1!=n) or (k2!=l):
			raise ValueError, 'error with the the dimension of K'

		# L (p,l)
		l1,l2 = self.L.shape
		if l2!=l:
			raise ValueError, 'error with the dimension of L'
		else:
			p = l1

		# M (l,n)
		m1,m2 = self.M.shape
		if (m1!=l) or (m2!=n):
			raise ValueError, 'error with the dimension of M'

		# N (l,m)
		n1,n2 = self.N.shape
		if n1!=l:
			raise ValueError, 'error with the dimension of N'
		else:
			m = n2
		
		# Q (n,m)
		q1,q2 = self.Q.shape
		if (q1!=n) or (q2!=m):
			raise ValueError, 'error with the dimension of Q'

		# R (p,n)
		r1,r2 = self.R.shape
		if (r1!=p) or (r2!=n):
			raise ValueError, 'error with the dimension of R'

		# S (p,m)
		s1,s2 = self.S.shape
		if (s1!=p) or (s2!=m):
			raise ValueError, 'error with the dimension of S'

		return (l,m,n,p)
	


	@property
	def size( self):
		"""return the size of the realization (l,m,n,p)"""
		return self.__l, self.__m, self.__n, self.__p