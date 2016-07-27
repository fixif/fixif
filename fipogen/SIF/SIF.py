# coding=utf8

"""
This class describes the SIF object
"""


__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fipogen.LTI import dSS
from fipogen.func_aux import dynMethodAdder, python2mpf_matrix
import numpy as np

from numpy import c_, r_, eye, zeros, matrix as mat
from numpy.linalg import inv
from math import log
from copy import copy


def isTrivial ( x, epsilon ):
	"""
	isTrivial(x, epsilon)

	Checks if a parameter is trivial, ie if the parameter is a power of 2

	:math:`x` is trivial if :

	.. math::
		\abs{ \abs{x} - 2^p } < \epsilon 2^p

	where :math:`\epsilon` is a relative error used as threshold

	return value is boolean
	"""
	if x==0:
		return True
	p = round( log(abs(x),2) )
	alpha = log(abs(x),2) - p

	return abs(alpha) < epsilon*(1-epsilon/2)





@dynMethodAdder
class SIF(object):
	"""
	Special Implicit Form (formely FWR, Finite Wordlength Realization)

	- 'l','m','n','p' : dimensions of the realization, set from JtoS, and checked with __check_set_dimensions__
		- 'l' intermediate variables
		- 'n' states
		- 'p' outputs
		- 'q' inputs


	- 'J, K, L, M, N, P, Q, R, S' matrices 'J' to 'S' (excluding 'O')
	- 'Z' is a big matrix regrouping all matrixes from 'J' to 'S'

	- 'dJ, dK, dL, dM, dN, dP, dQ, dR, dS' are matrixes :math:`\delta J` to :math:`\delta S`
	thoses matrices represent exactly implemented parameters :
	.. math::
		\delta(Z)_{ij} \left\lbrace\begin{aligned}
			0 if Z_{ij} \pm 2, p \in \mathbb{Z}\\
			1 otherwise
		\end{aligned}\right.
	'dZ' is :math:`\delta Z`

	- 'AZ, BZ, CZ, DZ' matrixes :math:`A_Z, B_Z, C_Z, D_Z` and associated state-space dSS

	When a SIF object is created, it is *not* possible to change its dimensions 'l,m,p,q' nor fields 'AZ,BZ,CZ,DZ'
	JOJO : Fields 'Z, dZ' are constructed from 'J' to 'S' and 'dJ' to 'dS' respectively, so those are
	Fields 'Z, dZ' are redundant with fields 'J ... S' but they can both be useful

	Changing 'Z' automatically changes fields 'J' to 'S' and reciprocally, 'dZ' changes 'dJ' to 'dS' respectively.

	'AZ, BZ, CZ, DZ' are deduced accordingly

	"""

	epsilondZ = 1e-8    # used to deduced dJ, dK, dL, dM, dN, dP, dQ, dR and dS matrices when they are not specified


	def __init__ ( self, JtoS, dJtodS=None):
		"""
		the SIF object is built from the matrices J, K, L, M, N, P, Q, R and S
		Parameters
		----------
		JtoS: tuple (J, K, L, M, N, P, Q, R, S)
		dJtodS: tuple (dJ, dK, dL, dM, dN, dP, dQ, dR, dS) -> if None, they are computed from J to S matrices (0 if the coefficient is close to a power of 2 (with epsilondZ error))
		plant: dSS object corresponding to the plant if we are in Closed-Loop context

		Returns
		-------
		a SIF object
		"""
		#  set and check sizes
		self._l, self._n, self._p, self._q = self._check_dimensions(JtoS)
		self._build_Z(JtoS)
		self._invJ = inv(JtoS[0])		#TODO: do it properly (no need to call inv() )
		self._build_fromZ()

		# build _dZ, the associated state space _dSS (contains AZ, BZ, CZ, DZ, gramians, etc.), _M1 _M2 _N1 _N2 and the *_bar matrices
		self._build_dZ( dJtodS )


	def _build_Z( self, JtoS ):
		"""
		build Z or dZ depending on provided matrix tuple
		"""
		J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in JtoS]
		self._Z = np.bmat( [[-J, M, N], [K, P, Q], [L, R, S]] )


	def _build_AZtoDZ( self ):
		# compute AZ, BZ, CZ and DZ matrices
		AZ = self.K * self._invJ * self.M + self.P
		BZ = self.K * self._invJ * self.N + self.Q
		CZ = self.L * self._invJ * self.M + self.R
		DZ = self.L * self._invJ * self.N + self.S
		# and store them in a dSS object
		self._dSS = dSS(AZ, BZ, CZ, DZ)


	def _build_M1M2N1N2( self ):
		# compute the useful matrices M1, M2, N1 and N2
		self._M1 = c_[self.K * self._invJ, eye(self._n), zeros((self._n, self._p))]
		self._M2 = c_[self.L * self._invJ, zeros((self._p, self._n)), eye(self._p)]
		self._N1 = r_[self._invJ * self.M, self.AZ, self.CZ ]
		self._N2 = r_[self._invJ * self.N, self.BZ, self.DZ]


	def _build_dZ( self, dJtodS ):
		"""
		Build dZ form dJ to dS matrices
		If None, then build dZ from Z
		'dJ, dK, dL, dM, dN, dP, dQ, dR, dS' are matrixes :math:`\delta J` to :math:`\delta S`
		thoses matrices represent exactly implemented parameters :
		.. math::
			\delta(Z)_{ij} \left\lbrace\begin{aligned}
				0 if Z_{ij} \pm 2, p \in \mathbb{Z}\\
				1 otherwise
			\end{aligned}\right.
		'dZ' is :math:`\delta Z`
		"""
		if dJtodS is None:
			self._dZ = np.vectorize( lambda x: int(not isTrivial(x, SIF.epsilondZ))) ( self._Z)
		else:
			dJ, dK, dL, dM, dN, dP, dQ, dR, dS = [np.matrix(X) for X in dJtodS]
			self._dZ = np.bmat( [[dJ, dM, dN], [dK, dP, dQ], [dL, dR, dS]] )



	def _build_fromZ( self ):
		self._build_AZtoDZ()
		self._build_M1M2N1N2()


	# Only matrix Z is kept in memory
	# JtoS extracted from Z matrix, dJtodS from dZ resp.
	@property
	def invJ( self ):
		return self._invJ

	# AZ to DZ getters
	@property
	def AZ( self ):
		return self._dSS._A

	@property
	def BZ( self ):
		return self._dSS._B

	@property
	def CZ( self ):
		return self._dSS._C

	@property
	def DZ( self ):
		return self._dSS._D

	@property
	def dSS(self):
		return self._dSS

	# Wo and Wc are from AZ to DZ state space
	@property
	def Wo( self ):
		return self._dSS.Wo

	@property
	def Wc( self ):
		return self._dSS.Wc


	# Z, dZ getters
	@property
	def Z( self ):
		return self._Z

	@property
	def Zcomp(self):
		"""
		Zcomp is the matrix Z modified, used for the computation
		it's Z, except that the term `J` has zeros on its diagonal
		"""
		Zcomp = copy(self._Z)
		Zcomp[0:self._l,0:self._l] = -self.J + eye(self._l) # to set to 0 the diagonal terms of J
		return Zcomp


	@property
	def dZ( self ):
		return self._dZ

	# Z, dZ setters
	@Z.setter
	def Z( self, mymat ):
		self._Z = mymat
		self._invJ = inv(self.J)
		self._build_fromZ()

	@dZ.setter
	def dZ( self, mymat ):
		self._dZ = mymat


	#  JtoS getters
	@property
	def JtoS(self):
		return self.J, self.K, self.L, self.M, self.N, self.P, self.Q, self.R, self.S

	@property
	def J( self ):
		return -self._Z[0: self._l, 0: self._l]

	@property
	def K( self ):
		return self._Z[self._l: self._l + self._n, 0: self._l]

	@property
	def L( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, 0:self._l]

	@property
	def M( self ):
		return self._Z[0: self._l, self._l: self._l + self._n]

	@property
	def N( self ):
		return self._Z[0: self._l, self._l + self._n: self._l + self._n + self._q]

	@property
	def P( self ):
		return self._Z[self._l: self._l + self._n, self._l: self._l + self._n]

	@property
	def Q( self ):
		return self._Z[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q]

	@property
	def R( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n]

	@property
	def S( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q]


	# dJtodS getters
	@property
	def dJ( self ):
		return -self._dZ[0: self._l, 0: self._l]

	@property
	def dK( self ):
		return self._dZ[self._l: self._l + self._n, 0: self._l]

	@property
	def dL( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, 0:self._l]

	@property
	def dM( self ):
		return self._dZ[0: self._l, self._l: self._l + self._n]

	@property
	def dN( self ):
		return self._dZ[0: self._l, self._l + self._n: self._l + self._n + self._q]

	@property
	def dP( self ):
		return self._dZ[self._l: self._l + self._n, self._l: self._l + self._n]

	@property
	def dQ( self ):
		return self._dZ[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q]

	@property
	def dR( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n]

	@property
	def dS( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q]


	# JtoS setters
	# J to N : we rebuild all matrices
	#TODO: is it really useful ?
	@J.setter
	def J( self, mymat ):
		self._Z[0: self._l, 0: self._l] = - mymat
		self._invJ = inv(mymat)
		self._build_fromZ()

	@K.setter
	def K( self, mymat ):
		self._Z[self._l: self._l + self._n, 0: self._l] = mymat
		self._build_fromZ()

	@L.setter
	def L( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, 0:self._l] = mymat
		self._build_fromZ()

	@M.setter
	def M( self, mymat ):
		self._Z[0: self._l, self._l: self._l + self._n] = mymat
		self._build_fromZ()

	@N.setter
	def N( self, mymat ):
		self._Z[0: self._l, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()

	@P.setter
	def P( self, mymat ):
		self._Z[self._l: self._l + self._n, self._l: self._l + self._n] = mymat
		self._build_dZ()
		self._build_AZtoDZ()

	@Q.setter
	def Q( self, mymat ):
		self._Z[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()

	@R.setter
	def R( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n] = mymat
		self._build_fromZ()

	@S.setter
	def S( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()


	# dJtodS setters
	# we only modify dZ matrix so no need to rebuild anything
	@dJ.setter
	def dJ( self, mymat ):
		self._dZ[0: self._l, 0: self._l] = mymat

	@dK.setter
	def dK( self, mymat ):
		self._dZ[self._l: self._l + self._n, 0: self._l] = mymat

	@dL.setter
	def dL( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, 0:self._l] = mymat

	@dM.setter
	def dM( self, mymat ):
		self._dZ[0: self._l, self._l: self._l + self._n] = mymat

	@dN.setter
	def dN( self, mymat ):
		self._dZ[0: self._l, self._l + self._n: self._l + self._n + self._q] = mymat

	@dP.setter
	def dP(self, mymat ):
		self._dZ[self._l: self._l + self._n, self._l: self._l + self._n] = mymat

	@dQ.setter
	def dQ( self, mymat ):
		self._dZ[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q] = mymat

	@dR.setter
	def dR( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n] = mymat

	@dS.setter
	def dS( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q] = mymat


	def _check_dimensions( self, JtoS ):
		"""
		Compute the size 'l, n, p, q' of SIF
		Check size of matrices 'J' to 'S'
		Instead of ad-hoc tests, we have a list of required sizes (empty at the beginning), and we check the consistency, matrix after matrix
		"""

		l = []  # we keep the size of the matrices in 2-element lists (size+name of the matrix that gives the size)
		n = []
		p = []
		q = []
		matrices = [ ("J",l,l), ("K",n,l), ("L",p,l), ("M",l,n), ("N",l,q), ("P",n,n), ("Q",n,q), ("R",p,n), ("S",p,q) ]

		# we check every matrix
		for X, (name,a,b) in zip( JtoS, matrices ):
			# get the size if it's the first time we see them
			if not a:
				a.extend( [X.shape[0], name] )
			if not b:
				b.extend( [X.shape[1], name] )
			# check for consistency
			if (a[0],b[0]) != X.shape:
				pb = a[1] if a[0]!=X.shape[0] else b[1]
				raise ValueError( "The matrix %s is a %dx%d matrix, instead of being a %dx%d matrix (to be consistent with matrix %s)" % (name, X.shape[0], X.shape[1], a[0], b[0], pb) )

		return (l[0],n[0], p[0], q[0])


	@property
	def size( self ):
		"""
		Returns size of realization : a tuple (l, n, p, q)
		"""

		return (self._l, self._n, self._p, self._q)

	@property
	def n(self):
		return self._n
	@property
	def p(self):
		return self._p
	@property
	def q(self):
		return self._q
	@property
	def l(self):
		return self._l


	def __str__( self ):
		"""
		Returns a string describing the SIF
		"""
		def plural ( n ):
			return 's' if n>1 else ''

		mystr = "l={0}, n={1}, p={2}, q={3} ({0} intermediate variable{4}, {1} state{5}, {3} input{7}, {2} output{6})\n".format(
			self._l, self._n, self._p, self._q, plural(self._l), plural(self._n), plural(self._p), plural(self._q))
		mystr += "Z = \n" + str(self._Z) + "\n"

		mystr += "dZ = \n" + str(self._dZ) + "\n"

		return mystr



	def simulate(self, u):
		"""
		Compute the outputs of the SIF with the inputs u
		2 dimension is time (N samples)
		Parameters:
			- u: a q*N matrix
		Returns:
			- y: a p*N matrix
		"""
		u=mat(u)
		N = u.shape[1]
		if u.shape[0] != self._q:
			raise ValueError( "SIF.simulate: u should be a %d*N matrix"%self._q )
		y = mat(zeros( (self._p,N) ))

		xk = mat(zeros( (self._n,1) ))	# TODO: add the possibility to start with a non-zero state

		# loop to compute the outputs
		for i in range(N):
			xkp1 = self.AZ*xk + self.BZ*u[:,i]
			y[:,i] = self.CZ*xk + self.DZ*u[:,i]
			xk = xkp1

		return y



	def simulateMP(self, u, prec):
		"""
		Compute the outputs of the SIF with the inputs u
		2 dimension is time (N samples)
		Parameters:
			- u: a q*N matrix
		Returns:
			- y: a p*N matrix
		"""

		import mpmath as mp

		N = u.shape[1]
		if u.shape[0] != self._q:
			raise ValueError( "SIF.simulate: u should be a %d*N matrix"%self._q )

		mp.mp.dps = prec
		mp.mp.pretty = False
		u = python2mpf_matrix(u)
		#u=mp.matrix(u)



		AZ = python2mpf_matrix(self.AZ)
		BZ = python2mpf_matrix(self.BZ)
		CZ = python2mpf_matrix(self.CZ)
		DZ = python2mpf_matrix(self.DZ)

		y = mp.zeros(self._p,N)
		#y = python2mpf_matrix(zeros( (self._p,N) ))
		xk = mp.zeros(self._n,1)
		#xk = python2mpf_matrix(zeros( (self._n,1) ))	# TODO: add the possibility to start with a non-zero state

		# loop to compute the outputs
		for i in range(N):
			xkp1 = AZ*xk + BZ*u[:,i]
			y[:,i] = CZ*xk + DZ*u[:,i]
			xk = xkp1

		return y










	def simplify(self):




		return self

	def computeDeltaSIF(self):
		"""Compute an error filter deltaH which takes an error-vector as inputs
		it has follwing form:
			J M (I 0 0)^T
			K P (0 I 0)^T
			L R (0 0 I)^T
				"""
		E1 = np.bmat([np.eye(self.l, self.l), np.zeros([self.l, self.n]), np.zeros([self.l, self.p])])  # N
		E2 = np.bmat([np.zeros([self.n, self.l]), np.eye(self.n, self.n), np.zeros([self.n, self.p])])  # Q
		E3 = np.bmat([np.zeros([self.p, self.l]), np.zeros([self.p, self.n]), np.eye(self.p, self.p)])  # S

		deltaH = SIF((self.J, self.K, self.L, self.M, E1, self.P, E2, self.R, E3))
		return deltaH




	def to_dTF(self):
		"""Convert into a dTF object
		"""
		return self.dSS.to_dTF()


	@property
	def Hu(self):
		"""return the Hu state-space"""
		return dSS(self.AZ, self.BZ, self._N1, self._N2)

	@property
	def Hepsilon(self):
		return dSS(self.AZ, self._M1, self.CZ, self._M2)