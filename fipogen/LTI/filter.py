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
from numpy.random import seed as numpy_seed, randint, choice
from re import compile


regRF = compile("RandomFilter-\(([0-9]+),([0-9]+)\)/\(([0-9]+),([0-9]+)\)/\(([0-9]+),([0-9]+)\)-([0-9]+)")	# used to recognize random filter names



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

	@property
	def p(self):
		"""
		Returns the number of input
		"""
		if self._dTF:
			return 1
		else:
			return self._dSS.p


	@property
	def q(self):
		"""
		Returns the number of outputs
		"""
		if self._dTF:
			return 1
		else:
			return self._dSS.q



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



def iter_random_Filter( number, n = (5, 10), p = (1, 5), q = (1, 5), seeded=True, type='all'):
	"""
	Generate some n-th order stable random filter
	Parameters
		----------
		- number: number of Butterworth filters generated
		- n: tuple (mini (incl.) ,maxi (exclus.)) for the number of states (default:  random between 5 and 10)
		- p: tuple (mini (incl.) ,maxi (exclus.)) for the number of outputs (default: random between 1 and 5), used for 'MIMO' and 'SIMO' filters
		- q: tuple (mini (incl.) ,maxi (exclus.)) for the number of inputs (default: random between 1 and 5), used for 'MIMO' and 'MISO' filters
		- seeded: (boolean) indicates if the random dSS should be done with a particular seed or not (in order to be reproductible, the seed is stored in the name of the filter)
		- type: (string) indicates the type of the filter : 'MIMO', 'SISO', 'SIMO', 'MISO', or 'all'
			-> 'SISO', 'MISO' or 'SIMO' will fix p and/or q to 1, even if another value is given for p or q
			-> for 'all', it randomly choose one among 'MIMO', 'SISO', 'SIMO' and 'SISO'

	"""
	pq = {'SISO':( (1,2), (1,2) ), 'SIMO': (p,(1,2)), 'MISO': ((1,2),q), 'MIMO': (p,q)}

	seeds = [randint(0, 1e9) if seeded else None for i in range(number)]  # generate a particular seed for each random dSS, or None (if seeded is set to False)

	for s in seeds:
		if type not in pq.keys():
			type = choice( pq.keys() )
		yield random_Filter(n=n, p=pq[type][0], q=pq[type][1], seed=s)





def random_Filter(n=(5,10), p=(1,5), q=(1,5), seed=None, name=None):
	"""
	Generate a n-th order stable filter, with q inputs and p outputs

	Parameters
	----------
		- n: tuple (mini,maxi) number of states (default:  random between 5 and 10)
		- p: tuple (mini (incl.) ,maxi (exclus.)) for the number of outputs
		- q: tuple (mini (incl.) ,maxi (exclus.)) for the number of inputs
		- seed: if not None, indicates the seed toi use for the random part (in order to be reproductible, the seed is stored in the name of the filter)
		- name: used to build a random filter from a string (a name of a filter previously built with random_Filter)
			-> should be of the form 'RandomFilter-(5,10)/(1,2)/(1,10)-12345678'

	Returns a Filter object
	"""
	if name:
		m=regRF.match(name)
		if m:
			res = tuple( map( int, m.groups()) )
			n = res[0:2]
			p = res[2:4]
			q = res[4:6]
			seed = res[6]
		else:
			raise ValueError( "randomFilter: the string should be a valid string, ie be like (RandomFilter-(5,10)/(1,2)/(1,10)-12345678'")
	# change the seed if asked
	if seed:
		numpy_seed(seed)
		t= n+p+q+(seed,)
		name = 'RandomFilter-(%d,%d)/(%d,%d)/(%d,%d)-%d'%t	# for example 'RandomFilter-(5,10)/(1,2)/(1,10)-12345678' for a MISO filter (#states between 5 and 10, #inputs between 1 and 10), seed=12345678)
	else:
		name = 'RandomFilter'
	# choose random size
	nn = randint(*n)
	pp = randint(*p)
	qq = randint(*q)
	# return a Filter from a random dSS
	return Filter( ss=random_dSS(nn, pp, qq), name=name, stable=True)