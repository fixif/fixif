# coding=utf8

"""
This class describes the Realization object
"""


__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Anastasia Volkova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fipogen.SIF import SIF
from fipogen.func_aux import dynMethodAdder
from fipogen.LTI import Filter
from fipogen.LTI import dSS

import numpy as np


from os import remove

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


# TODO: tester pour voir pourquoi le @dynMethodAdder ne marche pas... (avec pytest, notamment)
#@dynMethodAdder
class Realization(SIF):
	"""
	a Realization is a structured SIF object implementing a particular filter
	Inherit from a SIF, and also contains:
	- _filter: the filter that it implements
	- _varNameT, _varNameX, _varNameU, _varNameY : lists of the name of the intermediate variables (varNameT), the states (varNameX), the inputs (varNameU) and the outputs (varNameY)
	"""
	def __init__(self, filter, JtoS, dJtodS=None, structureName="", varNameTX=None):
		"""
		the Realization object is built from the matrices J, K, L, M, N, P, Q, R and S, and a filter
		Parameters
		----------
		- JtoS: tuple (J, K, L, M, N, P, Q, R, S)
		- dJtodS: tuple (dJ, dK, dL, dM, dN, dP, dQ, dR, dS) -> if None, they are computed from J to S matrices (0 if the coefficient is close to a power of 2 (with epsilondZ error))

		- varNameTX: (varNameT, varNameX), where varNameT and varNameX are two lists containing the name of the variables T and X, respectively
		- filter: the filter implemented by the Realization
		- strucureName: name of a structure

		Returns
		-------
		a Realization object
		"""

		# call the parent class constructor
		# see http://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods for super() and some comments
		SIF.__init__( self, JtoS, dJtodS)

		# name of the variables t, x, u and y
		if varNameTX is None:
			self._varNameT = genVarName( 't', self._l)
			self._varNameX = genVarName( 'x', self._n)
		else:
			self._varNameT = varNameTX[0]
			self._varNameX = varNameTX[1]
		self._varNameU = genVarName( 'u', self._q)
		self._varNameY = genVarName( 'y', self._p)


		self._MSB = None
		self._LSB = None

		# store the filter
		if filter is not None:
			self._filter = filter
		else:
			# build the filter from the SIF...
			self._filter = Filter( tf=self.to_dTF() )

		# store the structure infos
		self._structureName = structureName

		# store the run module (that contains C functions generated to "evaluate" the realization (double, FxP, multiprecision, etc.))
		self._runModule = None

	def __del__(self):
		# remove the module file (.so) when it exists
		if self._runModule is not None:
			remove( self._runModule.__file__ )

	@property
	def MSB(self):
		return self._MSB

	@property
	def LSB(self):
		return self._LSB

	@property
	def filter(self):
		return self._filter

	@property
	def name(self):
		return "Realization `%s` for filter `%s`"%(self._structureName, self._filter.name )

	def __str__(self):
		return self.name + "\n" + SIF.__str__(self)



	def quantize(self, q, rnd = 'n'):
		"""
		Given a positive integer q this function quantizes matrix Z of the current realiaztion to
		q bits with rounding to nearest ('n') (by default), up ('u') or down ('d')

		Z[i,j] = round(Z[i,j] * 2** -q) * 2**q for round-to-nearest
		Z[i,j] = ceil(Z[i,j] * 2** -q) * 2**q for round-up
		Z[i,j] = floor(Z[i,j] * 2** -q) * 2**q for round-down




		Parameters
		----------
		q
		rnd

		Returns
		-------

		"""
		Rq = self


		if not isinstance(q, int) or q == 0:
			raise ValueError('Vannot quantize the realiaztion: q must be a strictly positive int')

		if q < 0:
			q = abs(q)

		m, n = Rq.Z.shape

		Rq.Z = np.matrix([[Rq.Z[i,j] * 2 ** (q) for i in range(0,m)] for j in range(0,n)])

		if rnd == 'n':
			Rq.Z = np.around(Rq.Z)
		elif rnd == 'u':
			Rq.Z = np.matrix([[np.ceil(Rq.Z[i,j]) for i in range(0,m)] for j in range(0,n)])
		elif rnd == 'd':
			Rq.Z = np.matrix([[np.floor(Rq.Z[i,j]) for i in range(0,m)] for j in range(0,n)])
		else:
			raise ValueError('Cannot quantize the realiaztion: rounding mode specifier is invalid, can have n, u or d ')

		Rq.Z = np.matrix([[Rq.Z[i,j] * 2 ** (-q) for i in range(0,m)] for j in range(0,n)])

		return Rq














				# def compute_LSB_allvar(self, l_y_out):
	#
	# 	l_y_out = np.matrix([l_y_out])
	#
	# 	# construct the error-filter
	# 	deltaSIF = self.computeDeltaSIF()
	#
	# 	# compute the WCPG of the error filter
	# 	wcpgDeltaH = deltaSIF.dSS.WCPG()
	#
	# 	# we repartition the error budget equally for all variables
	# 	c = self.l + self.n + self.p
	#
	# 	# In order to respect the overall error |deltaY(k)| < 2^(l_y_out-1)
	# 	# we need to compute the temporary, state and output variables with LSB l_i
	# 	# l_i = max(l_y_out) - g_i-1
	# 	# where the correction term g_i is computed via
	# 	# g_i = 1 + max_j { ceil( log2 ( c * wcpgDeltaH[j, i] ) )}
	#
	# 	g = np.bmat([1 + max(np.ceil(np.log2(c * wcpgDeltaH[:, i]))) for i in range(0, c)])
	#
	# 	for x in (g == np.inf):
	# 		if x.any():
	# 			print 'Divided by zero\n'
	#
	# 	lsb = np.bmat([max(l_y_out) - g - np.ones(l_y_out.shape)])
	#
	# 	return lsb
	#
	# def generate_inputs(self, u_bar, N):
	# 	u = np.bmat(np.zeros([1, N]))
	# 	u[0, 0] = self.dSS.D
	# 	for i in range(0, N):
	# 		u[0, i] = u_bar * np.sign(self.dSS.C * (self.dSS.A ** i) * self.dSS.B)
	#
	# 	return u
	#
	# def compute_MSB_allvar(self, u_bar):
	#
	# 	# self._Z = np.bmat([[-J, M, N], [K, P, Q], [L, R, S]])
	#
	# 	C1 = np.bmat([[np.eye(self.l, self.l)], [np.zeros([self.n, self.l])], [self.L]])  # L
	# 	C2 = np.bmat([[np.zeros([self.l, self.n])], [np.eye(self.n, self.n)], [self.R]])  # R
	# 	C3 = np.bmat([[np.zeros([self.l, self.q])], [np.zeros([self.n, self.q])], [self.S]])  # S
	#
	# 	# building an extended SIF
	# 	S_ext = SIF((self.J, self.K, C1, self.M, self.N, self.P, self.Q, C2, C3))
	#
	# 	# print "New number of outputs: "
	# 	# print S_ext.p
	#
	# 	wcpg = S_ext.dSS.WCPG()
	#
	# 	# print "WCPG:"
	# 	# print wcpg
	#
	# 	y_bar = wcpg * u_bar
	# 	msb = np.bmat([np.ceil(np.log2(x)) for x in y_bar])
	#
	# 	return msb
	#
	# def compute_MSB_allvar_extended(self, u_bar, lsb_t, lsb_x, lsb_y):
	#
	# 	# building L, R and S matrices for the extended SIF, which will have
	# 	# a vector (t,x,y) as an output vector
	# 	C1 = np.bmat([[np.eye(self.l, self.l)], [np.zeros([self.n, self.l])], [self.L]])  # L
	# 	C2 = np.bmat([[np.zeros([self.l, self.n])], [np.eye(self.n, self.n)], [self.R]])  # R
	# 	C3 = np.bmat([[np.zeros([self.l, self.q])], [np.zeros([self.n, self.q])], [self.S]])  # S
	#
	# 	# building an extended SIF
	# 	S_ext = SIF((self.J, self.K, C1, self.M, self.N, self.P, self.Q, C2, C3))
	#
	# 	wcpg = S_ext.dSS.WCPG()
	#
	# 	# compute the error filter deltaH which corresponds to the extended SIF
	# 	deltaH = S_ext.computeDeltaSIF()
	# 	wcpgDeltaH = deltaH.dSS.WCPG()
	#
	# 	# compute msb via formula
	# 	# msb_i = ceil( log2 ( (<<H>> * u_bar)_i + (<<deltaH>> * 2^lsb_ext)_i ))
	#
	# 	y_bar = wcpg * u_bar
	#
	# 	# lsb_ext2 = np.matrix([ lsb_ext[0, 0:deltaH.l] lsb_ext[0, deltaH.l:deltaH.l + deltaH.n] lsb_ext[0] ])
	# 	lsb_bar = np.concatenate((lsb_t, lsb_x, lsb_t, lsb_x, lsb_y), axis=0)
	# 	lsb_bar = np.bmat([lsb_bar])
	#
	# 	lsb_bar = np.matrix([2 ** lsb_bar[0, i] for i in range(0, lsb_bar.size)])
	# 	delta_bar = wcpgDeltaH * lsb_bar.transpose()
	#
	# 	if (y_bar.size == delta_bar.size):
	# 		msb = np.bmat([np.ceil(np.log2(y_bar[i] + delta_bar[i])) for i in range(0, delta_bar.size)])
	# 		return msb
	# 	else:
	# 		print 'Something went wrong, error with sizes :( \n'
	# 		return 0
	#

