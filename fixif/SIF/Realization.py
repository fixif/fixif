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
from fixif.SIF.Realization_algorithms import R_algorithm
from fixif.SIF.Realization_FxP import R_FxP
from fixif.SIF.Realization_implementation import R_implementation
from fixif.LTI import Filter
from fixif.FxP import Constant
import numpy as np
from copy import copy

from fixif.SIF import generateNames



class Realization(SIF, R_algorithm, R_FxP, R_implementation):
	"""
	a Realization is a structured SIF object implementing a particular filter
	Inherit from a SIF, and also contains:
	- _filter: the filter that it implements
	- _varNameT, _varNameX, _varNameU, _varNameY : lists of the name of the intermediate variables (varNameT), the states (varNameX), the inputs (varNameU) and the outputs (varNameY)

	Some other methods are defined in the mixin classes R_algorithm, R_FxP and R_implementation
	# see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY and http://www.qtrac.eu/pyclassmulti.html

	"""

	def __init__(self, filt, JtoS, dJtodS=None, structureName="", varNameT=None, varNameX=None):
		"""
		the Realization object is built from the matrices J, K, L, M, N, P, Q, R and S, and a filter
		Parameters
		----------
		- JtoS: tuple (J, K, L, M, N, P, Q, R, S)
		- dJtodS: tuple (dJ, dK, dL, dM, dN, dP, dQ, dR, dS) -> if None, they are computed from J to S matrices (0 if the coefficient is close to a power of 2 (with epsilondZ error))

		- varT_Name and varX_Name: lists containing the name of the variables T and X, respectively (more precisely, list of tuple (name,shift) where the shift indicates shift in time: ('t',0) means t(k) and ('x_1',-3) means x_1(k-3)
		- filter: the filter implemented by the Realization
		- strucureName: name of a structure

		Returns
		-------
		a Realization object
		"""

		# call the parent class constructor
		super(Realization, self).__init__(JtoS, dJtodS)

		# names (list) of the variables t, x, u and y
		self._varNameT = generateNames('t', self._l) if varNameT is None else varNameT
		self._varNameX = generateNames('x', self._n) if varNameX is None else varNameX
		self._varNameU = generateNames('u', self._q)
		self._varNameY = generateNames('y', self._p)


		self._MSB = None
		self._LSB = None

		# store the filter
		if filt is not None:
			self._filter = filt
		else:
			# build the filter from the SIF...
			# self._filter = Filter(tf=self.to_dTF())
			self._filter = Filter(ss=self.dSS)
			# TODO: check if this is sometimes useful (or if the Reazilation is always created with a Filter -> I think it *must* be built with a Filter)

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

