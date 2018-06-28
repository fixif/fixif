# coding=utf8

"""
This class describes the Realization object
"""


__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fixif.SIF import SIF

from fixif.LTI import Filter
from fixif.FxP import Constant
import numpy as np
from copy import copy

import mpmath

def genVarName(baseName, nbVar):
	"""
	Generate a list of variable name, based on the basedName and the number of variable
	genVarName( 'u', nbVar) returns:
	- 'u(k)' if nbVar == 1
	- otherwise [ 'u_1(k)', 'u_2(k)', ..., 'u_n(k)' ]
	"""
	if nbVar == 1:
		return [baseName + '(k)']
	else:
		return [baseName + "_{%d}(k)" % (i+1) for i in range(nbVar)]


class Realization(SIF):
	"""
	a Realization is a structured SIF object implementing a particular filter
	Inherit from a SIF, and also contains:
	- _filter: the filter that it implements
	- _varNameT, _varNameX, _varNameU, _varNameY : lists of the name of the intermediate variables (varNameT), the states (varNameX), the inputs (varNameU) and the outputs (varNameY)
	"""

	# add the methods defined in other files
	# see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY and http://www.qtrac.eu/pyclassmulti.html
	from fixif.SIF.Realization_algorithms import algorithmLaTeX
	from fixif.SIF.Realization_FxP import _compute_LSB, _compute_MSB, compute_MSB_allvar_extended
	from fixif.SIF.Realization_implements import implementCdouble, makeModule, runCdouble


	def __init__(self, filt, JtoS, dJtodS=None, structureName="", varNameTX=None):
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
		super(Realization, self).__init__(JtoS, dJtodS)

		# name of the variables t, x, u and y
		if varNameTX is None:
			self._varNameT = genVarName('t', self._l)
			self._varNameX = genVarName('x', self._n)
		else:
			self._varNameT = varNameTX[0]
			self._varNameX = varNameTX[1]
		self._varNameU = genVarName('u', self._q)
		self._varNameY = genVarName('y', self._p)


		self._MSB = None
		self._LSB = None

		# store the filter
		if filt is not None:
			self._filter = filt
		else:
			# build the filter from the SIF...
			self._filter = Filter(tf=self.to_dTF())

		# store the structure infos
		self._structureName = structureName

		# store the run module (that contains C functions generated to "evaluate" the realization (double, FxP, multiprecision, etc.))
		self._runModule = None


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
	def structureName(self):
		return self._structureName

	@property
	def name(self):
		return "Realization `%s` for filter `%s`" % (self._structureName, self._filter.name)

	def __str__(self):
		return self.name + "\n" + SIF.__str__(self)


	def quantize(self, w):
		"""
		This funciton returns a new realization where the coefficients are quantized on wl bits
		(quantization is round-to-nearest only)

		basically, a coefficient x is modified in round(x*2^l)*2^-l,
		where l is its LSB, defined by l=w-m-1
		and m is its MSB : m=ceil(log2(abs(x))

		This "rule" has some exceptions (because 2's complement representation is not symetric),
		and and they are managed in Constant class

		Parameters:
		- w: word-length used for the quantization of the coefficients

		Returns: a new realization
		"""

		def quantize(x, wl):
			"""Simple function to quantized x with w bits (fixed-point style)"""

			return Constant(x, wl=wl, signed=True).approx if x else 0

		# check arguments
		if not isinstance(w, int) or w <= 0:
			raise ValueError('Cannot quantize the realiaztion: q must be a strictly positive int')

		# copy the realization and quantized the matrix Z
		R = copy(self)
		quantizeMat = np.vectorize(lambda x: quantize(x, w), otypes=[np.float])
		R.Z = quantizeMat(R.Z)
		return R

