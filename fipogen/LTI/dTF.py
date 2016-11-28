#coding=utf8

# This class describes a SISO transfer function
from numpy.random.mtrand import randint, rand

_author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import mpmath
from numpy import ndenumerate, array, zeros, matrix, matrix
from numpy import matrix as mat
from numpy import diagflat, zeros, ones, r_, atleast_2d, fliplr
from scipy.signal import tf2ss
from scipy.linalg import norm
from mpmath import *
from fipogen.func_aux import mpc_get_real

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


	def to_dSS(self, form="ctrl"):
		"""
		Transform the transfer function into a state-space
		Parameters:
			- form: controllable canonical form ('ctrl') or observable canonical form ('obs')

		"""
		#TODO: code it without scipy

		from fipogen.LTI import dSS
		if form=='ctrl':
			A = mat( diagflat(ones((1, self.order-1)), 1) )
			A[self.order-1,:] = fliplr( -self.den[0,1:] )
			B = mat( r_[ zeros((self.order-1, 1)), atleast_2d(1) ] )
			C = mat( fliplr( self.num[0,1:] ) - fliplr( self.den[0,1:] )*self.num[0,0] )
			D = mat( atleast_2d(self.num[0,0]) )
		elif form=='obs':
			#TODO!!
			A,B,C,D = tf2ss( array(self.num)[0,:], array(self.den)[0,:] )
		else:
			raise ValueError( 'dTF.to_dSS: the form "%s" is invalid (must be "ctrl" or "obs")'%form )

		return dSS(A,B,C,D)


	def assert_close(self, other, eps=1e-7):
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

		assert( norm(snum-onum)<eps )
		assert( norm(sden-oden)<eps )

	def WCPG_tf(self):

		r"""
		Compute the Worst Case Peak Gain of the state space

		.. math::
			\langle \langle H \rangle \rangle \triangleq |D| + \sum_{k=0}^\infty |C * A^k * B|

		Using algorithm developed in paper :
		[CIT001]_

		.. [CIT001]
			Lozanova & al., calculation of WCPG

		"""
		# compute the WCPG value if it's not already done
		if self._WCPG is None:

			try:
				num = array(self.num)
				denum = array(self.den)
				num_size = num.shape
				den_size = denum.shape
				W = empty((1, 1), dtype=float64)

				code = "return_val = WCPG_ABCD( &W[0,0], &A[0,0], &B[0,0], &C[0,0], &D[0,0], n, p, q);"
				support_code = 'extern "C" int WCPG_ABCD(double *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q);'
				err = inline(code, ['W', 'A', 'B', 'C', 'D', 'n', 'p', 'q'], support_code=support_code,
							 libraries=["WCPG"])
				if err == 0:
					# change numpy display formatter, so that we can display the full coefficient in hex (equivalent to printf("%a",...) in C)
					set_printoptions(formatter={'float_kind': lambda x: x.hex()})
					print(self)
					raise ValueError("WCPG_tf: cannot compute WCPG")
				self._WCPG = mat(W)
			except:
				raise ValueError("dSS: Impossible to compute WCPG matrix. Is WCPG library really installed ?")

		return self._WCPG


def TFmp_to_dSSmp(b, a):
	b = mpc_get_real(b)
	a = mpc_get_real(a)
	p = 1
	q = 1
	N = max(b.rows, a.rows)
	nb = b.rows
	na = a.rows

	D = b[nb-1, 0]		# D = b_0

	if a[na - 1] != mpf('1.0'):
		a = [element / a[na-1] for element in a]
		for i in range(0, na):
			a[i, 0] = a[i] / a[na-1]

	if na > nb:
		N = na
		beta = mp.zeros(N, 1)
		for i in range(0, nb):
			beta[i,0] = b[i]









def iter_random_dTF(number , order = (5, 10)):
	"""
	Generate some n-th order random (stable or not) SISO transfer functions

	Parameters:
		- number: number of state-space to generate
		- order: tuple (mini,maxi) order of the filter (default:  random between 5 and 10)

	Returns:
		- returns a generator of dTF objects (to use in a for loop for example)

	..Example::
		#>>> sys = list( iter_random_dTF( 12, (10,20)) )
		#>>> for S in iter_random_dTF( 12, (10,20)):
		#>>>		print( S.num )

	"""
	for i in range(number):
		yield random_dTF( order )



def random_dTF( order = (5, 10) ):
	"""
	Generate a n-th order random transfer function (not necessary stable)
	Parameters:
		- order: tuple (mini,maxi) order of the filter (default:  random between 5 and 10)
	"""
	n = randint(*order)
	num = mat(rand(1,n))
	den = mat(rand(1,n))
	return dTF( num, den)

