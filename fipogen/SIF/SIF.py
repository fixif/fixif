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
from fipogen.func_aux.dynMethodAdder import dynMethodAdder
import numpy as np

from numpy import c_, r_, eye, zeros, all, transpose
from numpy.linalg import inv
from math import log



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


def genVarName(baseName, nbVar):
	"""
	Generate a list of variable name, based on the basedName and the number of variable
	genVarName( 'u', nbVar) returns:
	- 'u(k)' if nbVar == 1
	- otherwise [ 'u_1(k)', 'u_2(k)', ..., 'u_n(k)' ]
	"""
	if nbVar == 1:
		return [ baseName + '(k)' ]
	else:
		return [ baseName+"_{%d}(k)"%(i+1) for i in range(nbVar) ]



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

	- varNameT, varNameX, varNameU, varNameY : lists of the name of the intermediate variables (varNameT), the states (varNameX), the inputs (varNameU) and the outputs (varNameY)

	"""

	epsilondZ = 1e-8    # used to deduced dJ, dK, dL, dM, dN, dP, dQ, dR and dS matrices when they are not specified


	def __init__ ( self, JtoS, dJtodS=None, plant=None, varNameTX=None):
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
		self._invJ = inv(JtoS[0])
		self._build_fromZ()

		# default plant
		self._plant = plant  # calculate intermediate matrixes

		# build _dZ, the associated state space _dSS (contains AZ, BZ, CZ, DZ, gramians, etc.), _M1 _M2 _N1 _N2 and the *_bar matrices
		self._build_dZ( dJtodS )

		# name of the variables t, x, u and y
		if varNameTX is None:
			self._varNameT = genVarName( 't', self._l)
			self._varNameX = genVarName( 'x', self._n)
		else:
			self._varNameT = varNameTX[0]
			self._varNameX = varNameTX[1]
		self._varNameU = genVarName( 'u', self._q)
		self._varNameY = genVarName( 'y', self._p)




	# 	# sensitivity measures
	#
	# 	#  Not calculated at instance creation, consumes time and not always useful
	# 	# All measures are initialized as None.
	#
	# 	#  When the optimization routine is used, two possible ways :
	# 	# - recalculate the value from scratch
	# 	# - use the existing value and UYW matrixes to get new value (if is_use_UYW_transform set to true)
	#
	# 	# Open-Loop and Closed-Loop
	#
	#
	#
	# 	self._qeasureTypes = ['OL', 'CL']
	#
	# 	self._qsensH = { key: None for key in self._qeasureTypes }
	# 	self._qsensPole = { key: None for key in self._qeasureTypes }
	# 	self._RNG = { key: None for key in self._qeasureTypes }
	#
	# 	# CL only
	# 	self._qstability = None
	#
	# 	# the values of those parameters needs to be kept
	# 	#  because we have to test those against the user's input or program input
	# 	#  to know if spitting out the old result is correct or if a recalculation is needed
	# 	self._qsensPole_moduli = None
	#
	# 	# Those parameters has to be defined in each subclass
	# 	# list of available methods for optimization of current form
	# 	# self._avail_formOpt = None
	# 	# currently used method for optimization
	# 	# self._formOpt = None
	#
	# 	# set UYW attributes
	# 	# those attributes are not used unless UYW transformation is possible on the form
	# 	self._U = None
	# 	self._invU = None
	# 	self._Y = None
	# 	self._W = None
	#
	# # two different cases : or we can use UYW transform, or we cannot
	# # this should be modified in each subclass AFTER using the init routine of SIF class
	# #  if a class variable is used it implies using a metaclass
	# # if an object attribute is used it implies that it's not the cleanest way,
	# # programmatically wise but avoids error (changing val at instance level does not,
	# # by reference change the value at the superclass level
	# # self.is_use_UYW_transform = True
	#
	# # in fact there are many different cases here : either we can use the UYW transform
	# # self._formOpt = 'UYW'
	# # or we can use the gammaDelta transform
	# # self._formOpt = 'gammaDelta'
	# # or we can use the delta transform
	# # 'delta'
	#
	# # this parameter has to be set in each SIF subclass
	#
	# # self._formOpt = None
	#
	# # _dynMethodAdder(SIF)




	def _build_Z ( self, JtoS ):
		"""
		build Z or dZ depending on provided matrix tuple
		"""
		J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in JtoS]
		self._Z = np.bmat( [[-J, M, N], [K, P, Q], [L, R, S]] )


	def _build_AZtoDZ ( self ):
		# compute AZ, BZ, CZ and DZ matrices
		AZ = self.K * self._invJ * self.M + self.P
		BZ = self.K * self._invJ * self.N + self.Q
		CZ = self.L * self._invJ * self.M + self.R
		DZ = self.L * self._invJ * self.N + self.S
		# and store them in a dSS object
		self._dSS = dSS(AZ, BZ, CZ, DZ)


	def _build_M1M2N1N2 ( self ):
		# compute the useful matrices M1, M2, N1 and N2
		self._q1 = c_[self.K * self._invJ, eye(self._n), zeros((self._n, self._p))]
		self._q2 = c_[self.L * self._invJ, zeros((self._p, self._n)), eye(self._p)]
		self._N1 = r_[self._invJ * self.M, eye(self._n), zeros((self._q, self._n))]
		self._N2 = r_[self._invJ * self.N, zeros((self._n, self._q)), eye(self._q)]

	def _build_dZ ( self, dJtodS ):
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



	def _build_fromZ ( self ):
		self._build_AZtoDZ()
		self._build_M1M2N1N2()


	# Only matrix Z is kept in memory
	# JtoS extracted from Z matrix, dJtodS from dZ resp.
	@property
	def invJ ( self ):
		return self._invJ

	# AZ to DZ getters
	@property
	def AZ ( self ):
		return self._dSS._A

	@property
	def BZ ( self ):
		return self._dSS._B

	@property
	def CZ ( self ):
		return self._dSS._C

	@property
	def DZ ( self ):
		return self._dSS._D

	@property
	def dSS(self):
		return self._dSS

	# Wo and Wc are from AZ to DZ state space
	@property
	def Wo ( self ):
		return self._dSS.Wo

	@property
	def Wc ( self ):
		return self._dSS.Wc


	# Z, dZ getters
	@property
	def Z ( self ):
		return self._Z

	@property
	def dZ ( self ):
		return self._dZ

	# Z, dZ setters
	@Z.setter
	def Z ( self, mymat ):
		self._Z = mymat
		self._invJ = inv(self.J)
		self._build_fromZ()

	@dZ.setter
	def dZ ( self, mymat ):
		self._dZ = mymat


	#  JtoS getters
	@property
	def JtoS(self):
		return self.J, self.K, self.L, self.M, self.N, self.P, self.Q, self.R, self.S

	@property
	def J ( self ):
		return -self._Z[0: self._l, 0: self._l]

	@property
	def K ( self ):
		return self._Z[self._l: self._l + self._n, 0: self._l]

	@property
	def L ( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, 0:self._l]

	@property
	def M ( self ):
		return self._Z[0: self._l, self._l: self._l + self._n]

	@property
	def N ( self ):
		return self._Z[0: self._l, self._l + self._n: self._l + self._n + self._q]

	@property
	def P ( self ):
		return self._Z[self._l: self._l + self._n, self._l: self._l + self._n]

	@property
	def Q ( self ):
		return self._Z[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q]

	@property
	def R ( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n]

	@property
	def S ( self ):
		return self._Z[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q]


	# dJtodS getters
	@property
	def dJ ( self ):
		return -self._dZ[0: self._l, 0: self._l]

	@property
	def dK ( self ):
		return self._dZ[self._l: self._l + self._n, 0: self._l]

	@property
	def dL ( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, 0:self._l]

	@property
	def dM ( self ):
		return self._dZ[0: self._l, self._l: self._l + self._n]

	@property
	def dN ( self ):
		return self._dZ[0: self._l, self._l + self._n: self._l + self._n + self._q]

	@property
	def dP ( self ):
		return self._dZ[self._l: self._l + self._n, self._l: self._l + self._n]

	@property
	def dQ ( self ):
		return self._dZ[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q]

	@property
	def dR ( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n]

	@property
	def dS ( self ):
		return self._dZ[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q]


	# JtoS setters
	# J to N : we rebuild all matrixes
	@J.setter
	def J ( self, mymat ):
		self._Z[0: self._l, 0: self._l] = - mymat
		self._invJ = inv(mymat)
		self._build_fromZ()

	@K.setter
	def K ( self, mymat ):
		self._Z[self._l: self._l + self._n, 0: self._l] = mymat
		self._build_fromZ()

	@L.setter
	def L ( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, 0:self._l] = mymat
		self._build_fromZ()

	@M.setter
	def M ( self, mymat ):
		self._Z[0: self._l, self._l: self._l + self._n] = mymat
		self._build_fromZ()

	@N.setter
	def N ( self, mymat ):
		self._Z[0: self._l, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()

	@P.setter
	def P ( self, mymat ):
		self._Z[self._l: self._l + self._n, self._l: self._l + self._n] = mymat
		self._build_dZ()
		self._build_AZtoDZ()

	@Q.setter
	def Q ( self, mymat ):
		self._Z[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()

	@R.setter
	def R ( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n] = mymat
		self._build_fromZ()

	@S.setter
	def S ( self, mymat ):
		self._Z[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q] = mymat
		self._build_fromZ()


	# dJtodS setters
	# we only modify dZ matrix so no need to rebuild anything
	@dJ.setter
	def dJ ( self, mymat ):
		self._dZ[0: self._l, 0: self._l] = mymat

	@dK.setter
	def dK ( self, mymat ):
		self._dZ[self._l: self._l + self._n, 0: self._l] = mymat

	@dL.setter
	def dL ( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, 0:self._l] = mymat

	@dM.setter
	def dM ( self, mymat ):
		self._dZ[0: self._l, self._l: self._l + self._n] = mymat

	@dN.setter
	def dN ( self, mymat ):
		self._dZ[0: self._l, self._l + self._n: self._l + self._n + self._q] = mymat

	@dP.setter
	def dP ( self, mymat ):
		self._dZ[self._l: self._l + self._n, self._l: self._l + self._n] = mymat

	@dQ.setter
	def dQ ( self, mymat ):
		self._dZ[self._l: self._l + self._n, self._l + self._n: self._l + self._n + self._q] = mymat

	@dR.setter
	def dR ( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, self._l: self._l + self._n] = mymat

	@dS.setter
	def dS ( self, mymat ):
		self._dZ[self._l + self._n: self._l + self._n + self._p, self._l + self._n: self._l + self._n + self._q] = mymat


	def _check_dimensions ( self, JtoS ):
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
	def size ( self ):
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


	def __str__ ( self ):
		"""
		Returns a string describing the SIF
		"""
		def plural ( n ):
			return 's' if n>1 else ''

		mystr = "l={0}, n={1}, p={2}, q={3} ({0} intermediate variable{4}, {1} state{5}, {3} input{7}, {2} input{6})\n".format(
			self._l, self._n, self._p, self._q, plural(self._l), plural(self._n), plural(self._p), plural(self._q))
		mystr += "Z = \n" + str(self._Z) + "\n"

		mystr += "dZ = \n" + str(self._dZ) + "\n"

		return mystr



	# plant setter and getter (if plant is modified, then all matrices relative to SIF-plant couple are recalculated)
	@property
	def plant ( self ):
		return self._plant

	@plant.setter
	def plant ( self, myplant ):
		self._plant = myplant
		self._build_plantSIF()




	#############################
	# pas encore vu/inclus/testé


	#
	#
	# #  U, Y, W attributes
	# @U.setter
	# def U ( self, mymat ):
	# 	if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._n:
	# 		raise (ValueError, 'Wrong dimension for U')
	# 	self._U = np.matrix(mymat)
	# 	self._invU = inv(self._U)
	#
	# @Y.setter
	# def Y ( self, mymat ):
	# 	if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._l:
	# 		raise (ValueError, 'Wrong dimension for Y')
	# 	self._Y = np.matrix(mymat)
	#
	# @W.setter
	# def W ( self, mymat ):
	# 	if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._l:
	# 		raise (ValueError, 'Wrong dimension for W')
	# 	self._W = np.matrix(mymat)
	#
	#


	#
	#
	# def _build_plantSIF ( self ):
	#
	# 	"""
	# 	This function sets intermediate matrixes
	# 	for sensitivity measurements
	# 	"""
	#
	# 	# dimensions of self.plant system
	#
	# 	l, m2, n, p2 = self.size
	# 	np, p, m = self.plant.size
	#
	# 	m1 = m - m2
	# 	p1 = p - p2
	#
	# 	if p1 <= 0 or m1 <= 0:
	# 		raise (ValueError, "dimension error : check self.plant and realization dimension")
	#
	# 	B1 = self.plant.B[:, 0:p1]
	# 	B2 = self.plant.B[:, p1:p]
	# 	C1 = self.plant.C[0:m1, :]
	# 	C2 = self.plant.C[m1:m, :]
	#
	# 	D11 = self.plant.D[0:m1, 0:p1]  # correct bug from matlab code
	# 	D12 = self.plant.D[0:m1, p1:p]
	# 	D21 = self.plant.D[m1:m, 0:p1]
	# 	D22 = self.plant.D[m1:m, p1:p]
	#
	# 	if not (all(D22 == zeros(D22.shape))):
	# 		raise (ValueError, "D22 needs to be null")
	#
	# 	# closed-loop related matrices
	# 	self._Abar = r_[c_[self.plant.A + B2 * self.DZ * C2, B2 * self.CZ], c_[self.BZ * C2, self.AZ]]
	# 	self._Bbar = r_[B1 + B2 * self.DZ * D21, self.BZ * D21]
	# 	self._Cbar = c_[C1 + D12 * self.DZ * C2, D12 * self.CZ]
	# 	self._Dbar = D11 + D12 * self.DZ * D21
	#
	# 	# intermediate matrices
	# 	self._q1bar = r_[
	# 		c_[B2 * self.L * self.invJ, zeros((np, n)), B2], c_[self.K * self.invJ, eye(n), zeros((n, p2))]]
	# 	self._q2bar = c_[D12 * self.L * self.invJ, zeros((m1, n)), D12]
	# 	self._N1bar = r_[
	# 		c_[self.invJ * self.N * C2, self.invJ * self.M], c_[zeros((n, np)), eye(n)], c_[C2, zeros((m2, n))]]
	# 	self._N2bar = r_[self.invJ * self.N * D21, zeros((n, p1)), D21]
	#

	# def _translate_Z_AZtoDZ_W ( self ):
	# 	"""
	# 	Calculate Z, AZtoDZ and W in the same function to factorize invU calculation
	# 	"""
	#
	# 	# _build_Z
	# 	#             J                     K                        L              M                     N              P                        Q                 R              S
	# 	self._build_Z((self.Y * self.J * self.W, self.invU * self.K * self.W, self.L * self.W, self.Y * self.M * self.U,
	# 				   self.Y * self.N, self.invU * self.P * self.U, self.invU * self.Q, self.R * self.U, self.S))
	#
	# 	self._invJ = inv(self.J)
	#
	# 	# _build_AZtoDZ
	#
	# 	self._AZ = self.invU * self._AZ * self.U
	# 	self._BZ = self.invU * self._BZ
	# 	self._CZ = self._CZ * self.U
	# 	# self._DZ = self._DZ not modified by transformation
	#
	# 	self._Z_dSS = dSS(self._AZ, self._BZ, self._CZ, self._DZ)
	#
	# 	# update Wo and Wc if they exist
	# 	if self._Wo is not None:
	# 		self._Wo = transpose(self.U) * self._Wo * self.U
	#
	# 	if self._Wc is not None:
	# 		self._Wc = self.invU * self._Wc * transpose(self.invU)



	# @staticmethod
	# def _check_MeasureType ( fname, target, words ):
	#
	# 	if target not in words:
	# 		raise (ValueError, '{0} type not recognized (use {1})'.format(fname, ' OR '.join(words)))
	#
	# # Function to set default UYW matrixes, called in inheriting classes after init
	# def _set_default_UYW ( self ):
	#
	# 	self.U = np.matrix(eye(self._n))
	# 	self.Y = np.matrix(eye(self._l))
	# 	self.W = self.Y
	#
	# # Functions to calculate measures.
	# # We keep updated closed-loop measures with stored plant at SIF instance level
	#
	# # MsensH
	# def MsensH ( self, measureType='OL', plant=None ):
	#
	# 	"""
	# 	If plant is specified here, CL will *always* be recalculated (we don't compare input with existing self._plant)
	# 	We need input of measureType with plant = None, to get access to the stored CL value without recalculating it.
	#
	# 	inst.MsensH(measureType='CL') gives the stored value for closed-loop case without recalculation (if there's a value)
	# 	or calculates from stored plant (if there's no stored value)
	# 	"""
	#
	# 	self._check_MeasureType('MsensH', measureType, self._qeasureTypes)
	#
	# 	is_calc_modified = False
	#
	# 	#  force CL calculation if there's a plant defined in call
	# 	if plant is not None:
	#
	# 		self.plant = plant  # calculate or recalculate intermediate bar matrixes
	# 		measureType = 'CL'
	# 		is_calc_modified = True
	#
	# 	elif measureType == 'CL' and self.plant is None:
	#
	# 		raise (NameError, 'Cannot provide MsensH closed-loop measure as no plant is defined')
	#
	# 	if (self._qsensH[measureType] is None) or (is_calc_modified):
	#
	# 		self._qsensH[measureType] = self.calc_MsensH(measureType)
	#
	# 	return self._qsensH[measureType]
	#
	# # MsensPole
	# def MsensPole ( self, measureType='OL', plant=None, moduli=1 ):
	#
	# 	self._check_MeasureType('MsensPole', measureType, self._qeasureTypes)
	#
	# 	is_calc_modified = False
	#
	# 	if plant is not None:
	#
	# 		self.plant = plant  # calculate or recalculate intermediate bar matrixes
	# 		measureType = 'CL'
	# 		is_calc_modified = True
	#
	# 	elif measureType == 'CL' and self.plant is None:
	#
	# 		raise (NameError, 'Cannot provide MsensPole closed-loop measure as no plant is defined')
	#
	# 	if not (moduli == self._qsensPole_moduli):  # dangerous if not integer value
	#
	# 		self._qsensPole_moduli = moduli
	# 		is_calc_modified = True
	#
	# 	if (self._qsensPole[measureType] is None) or (is_calc_modified):
	#
	# 		self._qsensPole[measureType] = self.calc_MsensPole(measureType, moduli)
	#
	# 	return self._qsensPole[measureType]
	#
	# # RNG
	# def RNG ( self, measureType='OL', plant=None, eps=None, is_rebuild_dZ=False ):
	#
	# 	self._check_MeasureType('RNG', measureType, self._qeasureTypes)
	#
	# 	is_calc_modified = False
	#
	# 	if plant is not None:
	#
	# 		self.plant = plant  # trigger recalculation of plantSIF intermediate matrixes by calling setter
	# 		measureType = 'CL'
	# 		is_calc_modified = True
	#
	# 	elif measureType == 'CL' and self.plant is None:
	#
	# 		raise (NameError, 'Cannot provide RNG closed-loop measure as no plant is defined')
	#
	# 	if (eps != self._eps) and not (eps is None):
	#
	# 		self._eps = eps
	# 		is_calc_modified = True
	# 		is_rebuild_dZ = True
	#
	# 	if is_rebuild_dZ:
	# 		self._build_dZ()
	#
	# 	if (self._RNG[measureType] is None) or is_calc_modified:
	#
	# 		self._RNG[measureType] = self.calc_RNG(measureType, self._eps)
	#
	# 	return self._RNG[measureType]
	#
	# # Mstability
	# def Mstability ( self, plant=None, moduli=1 ):
	#
	# 	is_calc_modified = False
	#
	# 	if plant is not None:
	#
	# 		self.plant = plant
	# 		is_calc_modified = True
	#
	# 	elif self.plant is None:
	#
	# 		raise (NameError, 'Cannot provide Mstability measure as no plant is defined')
	#
	# 	if not (moduli == self._qsensPole_moduli):
	#
	# 		self._qsensPole_moduli = moduli
	# 		is_calc_modified = True
	#
	# 	if (self._qstability is None) or is_calc_modified:
	#
	# 		self._qstability = self.calc_Mstability(moduli)
	#
	# 	return self._qstability
	#
	# # Hypothesis : plant is kept UNCHANGED from start to end of _recalc routine
	#
	# # Sensitivity criterions are recalculated if they already exist. If they exist as None, they're untouched
	#
	# # This is not needed because if we use the "dumb" method we need to recalculate everything from the start
	# # so we're going to use the regular __init__ from class
	#
	# def _recalc_sensitivity ( self ):
	#
	# 	for cur_type in self._qeasureTypes:
	#
	# 		if self._qsensH[cur_type] is not None:
	# 			self._qsensH[cur_type] = None
	# 			self.MsensH(measureType=cur_type)
	#
	# 		if self._qsensPole[cur_type] is not None:
	# 			self._qsensPole[cur_type] = None
	# 			self.MsensPole(measureType=cur_type)
	#
	# 		if self._RNG[cur_type] is not None:
	# 			self._RNG[cur_type] = None
	# 			self.RNG(measureType=cur_type)
	#
	# 	if self._qstability is not None:
	# 		self._qstability = None
	# 		self.Mstability()
	#
	# # use the UYW transform to get
	# # equivalent realization from existing realization
	# # new values of sensitivity measurements
	#
	# #  Order of calculations is fundamental here, otherwise we are not efficient :
	# # RNG needs no other measure calculated
	# #  MsensH needs no other measure calculated
	# # MsensPole needs MsensH calculation
	# # Mstability needs MsensPole calculation
	#
	# #  So, to MsensH and MsensPole are free once you want Mstability.
	# # MsensH is free once you want MsensPole
	#
	# def _translate_realization ( self, is_rebuild_dZ=False ):
	# 	"""
	# 	This function calculates an equivalent realization by updating all instance attributes
	# 	that needs to be updated
	#
	# 	As a first step we update Z by transforming it,
	# 	then the associated state space
	# 	then Wo and Wc if they exist (and they should already exist otherwise they are going to be recalculated then transformed, for example for RNG)
	# 	but if RNG has already been calculated, then they exist.
	# 	We should then try to see if there is a UYW transform that needs old value of Wo and Wc, and that needs not to be calculated by initial routine
	#
	# 	"""
	#
	# 	# translate from self.U, self.Y, self.W, self.invU
	# 	self._translate_Z_AZtoDZ_W()
	#
	# 	# mimic matlab code (could it destroy information during the process, if some coeffs go under the threshold after translation to equivalent form ??)
	# 	if is_rebuild_dZ:
	# 		self._build_dZ()
	#
	# 	# rebuild remaining matrixes used in sensitivity calculations
	# 	self._build_M1M2N1N2()
	#
	# 	# if there's a plant, let's rebuild all bar matrixes
	# 	if self.plant is not None:
	# 		self._build_plantSIF()
	#
	# 	# we don't call _set_check_dimensions bacause SIF dimension should remain the same
	#
	#
	# 	for cur_type in self._qeasureTypes:
	# 		# no need to check for Mstability because if it is present, then MsensPole has been calculated for CL case
	# 		if (self._RNG[cur_type] is not None) or (self._qsensPole[cur_type] is not None):
	# 			is_calc_T1T2 = True
	# 			break
	# 	else:
	#
	# 		is_calc_T1T2 = False
	#
	# 	# not necessary if we only need MsensH
	# 	if is_calc_T1T2:
	#
	# 		T1, T2 = self.calc_transform_UYW()
	#
	# 	for cur_type in self._qeasureTypes:
	#
	# 		# uses
	# 		# - previous value of self._RNG[cur_type]
	# 		# - new value of Wo calculated from UYW transform
	# 		# - previous value of dZ
	# 		# - previous value of M1M2Wobar for CL calculation
	# 		if self._RNG[
	# 			cur_type] is not None:  # use instance attribute here, not  self.RNG() otherwise we're going to calculate it. set to None initially)
	# 			self.transform_UYW_RNG(cur_type, T1)
	#
	# 		if self._qsensH[cur_type] is not None:
	# 			self.transform_UYW_MsensH(cur_type)  #  FIXME uses bruteforce method ATM
	# 		# self._qsensH[cur_type] = None
	# 		# self.MsensH(measureType=cur_type) # UYW transform for MsensH not defined
	#
	# 		if self._qsensPole[cur_type] is not None:
	# 			self.transform_UYW_MsensPole(cur_type, T1, T2)
	#
	# 	if self._qstability is not None:
	# 		self.transform_UYW_Mstability(T1, T2)
	#
	#
	#
	#
	#
	# @property
	# def U ( self ):
	# 	return self._U
	#
	# @property
	# def Y ( self ):
	# 	return self._Y
	#
	# @property
	# def W ( self ):
	# 	return self._W
	#
	# @property
	# def invU ( self ):
	# 	return self._invU


# Add additional methods SIF_othermoethods.py
# from modules in current folder
#_dynMethodAdder(SIF)
