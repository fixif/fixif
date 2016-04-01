# coding: utf8

"""
This file contains Object and methods for a Linear Time Invariant System (called Filter)
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from fipogen.LTI import dSS,dTF, random_dSS
from numpy.random import seed as numpy_seed, randint

class Filter(object):
	"""
	A LTI (Linear Time Invariant) object is described either a transfer function and state-space
	"""

	def __init__(self, num=None, den=None, A=None, B=None, C=None, D=None, tf=None, ss=None, stable=None, name='noname'):
		"""
		Create a Filter from numerator and denominator OR from A,B,C,D matrices
		Parameters
		----------
		num, den: numerator and denominator of the transfer function
		A,B,C,D: State-Space matrices
		dTF: a dTF object
		dSS: a dSS object
		"""
		self._dSS = None
		self._dTF = None
		self._name = name

		if A is not None and B is not None and C is not None and D is not None:
			self._dSS = dSS( A, B, C, D)
		elif num is not None and den is not None:
			self._dTF = dTF( num, den)
		elif tf is not None:
			self._dTF = tf
		elif ss is not None:
			self._dSS = ss
		else:
			raise ValueError( 'Filter: the values given to the Filter constructor are not correct')

		# is the filter stable?
		if stable is None:
			#TODO: compute the eigenvalues to know if it is stable or not
			self._stable = False
		else:
			self._stable = stable



	@property
	def dSS(self):
		if self._dSS is None:
			self._dSS = self._dTF.to_dSS()
		return self._dSS


	@property
	def dTF(self):
		if not self.isSISO():
			raise ValueError( 'Filter: cannot convert a MIMO filter to dTF (not yet)')
		if self._dTF is None:
			self._dTF = self._dSS.to_dTF()
		return self._dTF

	@property
	def name(self):
		return self._name


	def isSISO(self):
		"""
		Returns True if the lti filter is a Single Input Single Output filter
		"""
		if self._dTF or self._dSS.D.shape == (1,1):
			return True
		else:
			return False


	def isStable(self):
		"""
		Returns True if the filter is known to be stable
		"""
		return self._stable


	def isButter(self):
		"""
		Returns True if the filter is known to be a Butterworth filter
		"""
		from fipogen.LTI import Butter
		return self.__class__ == Butter


	def __repr__(self):
		return self._name



def iter_random_Filter( number, n = (5, 10), p = (1, 5), q = (1, 5), seeded=True):
	"""
	Generate some n-th order stable random filter
	Parameters
		----------
		- number: number of Butterworth filters generated
		- n: (int) The order of the filter
		- n: tuple (mini,maxi) number of states (default:  random between 5 and 10)
		- p: number of outputs (default: 1)
		- q: number of inputs (default: 1)
		- seeded: (boolean) indicates if the random dSS should be done with a particular seed or not (in order to be reproductible, the seed is stored in the name of the filter)

	"""
	seeds = [randint(0, 1e9) if seeded else None for i in range(number)]  # generate a particular seed for each random dSS, or None (if seeded is set to False)
	for s in seeds:
		yield random_Filter(n=n, p=p, q=q, seed=s)





def random_Filter(n, p, q, seed=None):
	"""
	Generate a n-th order stable filter, with q inputs and p outputs

	Parameters
	----------
		- n: tuple (mini,maxi) number of states (default:  random between 5 and 10)
		- p: number of outputs (default: 1)
		- q: number of inputs (default: 1)
		- seed: if not None, indicates the seed toi use for the random part (in order to be reproductible, the seed is stored in the name of the filter)

	Returns a Filter object
	"""
	# change the seed if asked
	if seed:
		numpy_seed(seed)
		name = 'RandomFilter-%d'%seed
	else:
		name = 'RandomFilter'
	# choose random size
	nn = randint(*n)
	pp = randint(*p)
	qq = randint(*q)
	# return a Filter from a random dSS
	return Filter( ss=random_dSS(nn, pp, qq), name=name, stable=True)