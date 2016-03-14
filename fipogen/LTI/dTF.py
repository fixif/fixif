#coding=utf8

# This class describes a SISO transfer function

_author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from numpy import ndenumerate, array, zeros
from numpy import matrix as mat
from scipy.signal import tf2ss
from scipy.linalg import norm

from numpy.testing import assert_allclose

class dTF(object):

	def __init__(self, num, den):
		"""
		Define a discrete-time SISO transfer function as

		:math:`H(z) = \frac{\sum_i^n num[i] z^-i}{1 + \sum_i^n den[i] z^-i}`
		"""

		den = mat(den)
		num = mat(num)

		if (num.shape[0]!=1) or (den.shape[0]!=1):
			raise ValueError('dTF: num and den should be 1D matrixes')

		# we normalize if den[0] is not equal to 1
		if den[0,0]==0:
			raise ValueError('dTF: The 1st coefficient of the denominator cannot be ZERO !')
		else:
			self._num = num/den[0,0]
			self._den = den/den[0,0]

		# filter order
		if den.shape!=num.shape:
			raise ValueError( 'Numerator and denomintator must have same length !')

		self._order = num.shape[1]-1




	@property
	def num(self):
		return self._num

	@property
	def den(self):
		return self._den

	@property
	def order(self):
		return self._order


	def __str__(self):
		"""pretty print of the transfer function"""
		str_num = " + ".join( str(c)+"z^"+str(-j) if j>0 else str(c) for (i,j),c in ndenumerate(self.num) )
		str_den = " + ".join( str(c)+"z^"+str(-j) if j>0 else str(c) for (i,j),c in ndenumerate(self.den) )

		fraclen = max(len(str_num), len(str_den))
		sp_num = " "*(( fraclen - len(str_num) ) / 2)
		sp_den = " "*(( fraclen - len(str_den) ) / 2)

		str_tf  = "\n"
		str_tf += " "*7 + sp_num + str_num + "\n"
		str_tf += "H(z) = " + '-'*fraclen + "\n"
		str_tf += " "*7 + sp_den + str_den + "\n"

		return str_tf


	def to_dSS(self):
		"""
		Transform the transfer function into a state-space

		"""
		#TODO: code it without scipy
		#TODO: option to choose controlability/observability canonical form
		from fipogen.LTI import dSS
		A,B,C,D = tf2ss( array(self.num)[0,:], array(self.den)[0,:] )
		return dSS(A,B,C,D)


	def assert_close(self, other, rtol=1e-7):
		"""
		asserts that self is "close" to other
		ie the numerator and denominator are close
		Parameters
		----------
		other: dTF object
		"""
		# add zeros for the smallest (in size) numerator so that the comparison can be done
		max_order = max( self.order, other.order)+1
		snum = zeros((1,max_order))
		snum[ :1, :self.num.shape[1] ] = self.num
		onum = zeros((1,max_order))
		onum[ :1, :other.num.shape[1] ] = other.num
		sden = zeros((1,max_order))
		sden[ :1, :self.den.shape[1] ] = self.den
		oden = zeros((1,max_order))
		oden[ :1, :other.den.shape[1] ] = other.den

		assert( norm(snum-onum)<1e-7 )
		assert( norm(sden-oden)<1e-7 )

