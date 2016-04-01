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

		# store the filter
		self._filter = filter

		# store the structure infos
		self._structureName = structureName



	@property
	def filter(self):
		return self._filter

	@property
	def name(self):
		return "Realization `%s` for filter `%s`"%(self._structureName, self._filter.name )

	def __str__(self):
		return self.name + "\n" + SIF.__str__(self)