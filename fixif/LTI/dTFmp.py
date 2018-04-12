
_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2016, FIPOgen Project, LIP6"
__credits__ = ["Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Anastasia Volkova"
__email__ = "Anastasia.Volkova@lip6.fr"
__status__ = "Beta"

from numpy.random.mtrand import randint, rand
from fixif.func_aux import python2mpf_matrix, mpf_to_numpy, mpf_matrix_to_sollya
import mpmath
import numpy
#import sollya

class dTFmp(object):

	def __init__(self, b, a):
		"""
		define a discrete transfer function with multiple precision coefficients
		Parameters
		----------
		b -  deg_b x 1 matrix of filter coefficients
		a -  deg_a x 1 matrix of filter coefficients

		Returns
		-------

		"""

		if not isinstance(b, mpmath.matrix) or not isinstance(a, mpmath.matrix):
			if isinstance(b, numpy.matrix) and isinstance(a, numpy.matrix):
				b = python2mpf_matrix(b)
				a = python2mpf_matrix(a)
			else:
				raise ValueError('Cannot create a dTFmp object: expected mpmath.matrix or numpy.matrix arguments but instead got %s and %s' % (type(b), type(a)))

		#check if user gave transposed matrices
		if b.cols > 1 and b.rows == 1:
			b = b.transpose()
		if a.cols > 1 and a.rows == 1:
			a = a.transpose()

		if a.cols != 1 or  b.cols!= 1: # or b.rows != a.rows :
			raise ValueError('Cannot create a dTFmp pbject: incorrect sizes')


		n = a.rows
		if a[0,0] != mpmath.mp.one:
			for i in range(0, n):
				# division cannot be performed exactly but we do it with doubled precision
				a[i,0] = mpmath.fdiv(a[i,0], a[0,0], prec = a[i,0]._mpf_[3] * 2)
				b[i, 0] = mpmath.fdiv(b[i, 0], b[0, 0], prec = b[i,0]._mpf_[3] * 2)

		self._order = n - 1
		self._num = b
		self._den = a

		# cached sollya numerator and denominator
		self._sollya = None


	@property
	def num(self):
		return self._num

	@property
	def den(self):
		return self._den

	@property
	def order(self):
		return self._order

	def to_dTF(self):
		from fixif.LTI import dTF
		return dTF(mpf_to_numpy(self._num.transpose()), mpf_to_numpy(self._den.transpose()))

	def to_dSSmp(self):

		"""
		This function constructs a discrete state-space matrices in canonical controllable form[1].
		Returns a dSSmp object.

		All operations are performed *exactly*


		Algorithm:

		1. Extract a delay-free path D = h(0) = b_0
		This is done by one stage of long division:

		H(z) = b_0 + { (beta_1 * z^-1 + ... + beta_N * z^-N} / {1 + a_1 * z^-1 + ... + a_N * z^-N},

		where
			N = max(Na, Nb)
			a_i = 0                     for i > Na
			b_i = 0                     for i > Nb
			beta_i = b_i - b_0 * a_i    for i=1...N

		2. Controller canonical form is as follows:
			-a_1    -a_2    ... -a_N-1    -a_N          1
			1       0                        0          0
		A = 0       1                        0      B=  0
							....                        ...
			0       0              1         0		    0


		C = [beta_1     beta_2  ... beta_N]         D = b_0


		[1] https://ccrma.stanford.edu/~jos/fp/Converting_State_Space_Form_Hand.html

		Returns
		-------
		S  - dSSmp object
		"""

		from fixif.LTI import dSSmp

		N = self.order + 1

		A = mpmath.mp.zeros(N - 1, N - 1)
		A[0, :] = -self.den.transpose()[0, 1:N]
		for i in range(1, N - 1):
			A[i, i - 1] = mpmath.mp.one
		B = mpmath.mp.zeros(N - 1, 1)
		B[0, 0] = mpmath.mp.one

		# We compute matrix C exactly
		C = mpmath.mp.zeros(1, N - 1)
		for i in range(0, N - 1):
			tmp = mpmath.fmul(self.num[0, 0], self.den[i + 1, 0], exact=True)
			C[0, i] = mpmath.fsub(self.num[i + 1, 0], tmp, exact=True)

		D = mpmath.matrix([self.num[0, 0]])

		return dSSmp(A,B,C,D)


	def to_Sollya(self):
		"""
		Convert transfer function into two Sollya polynomials (numerator and denomitator)
		The result is cached in self._sollya
		Returns
		- num, den: (sollya object) numerator and denominator of the transfer function
		"""
		if not self._sollya:
			tf_num_sollya, len_num, _ = mpf_matrix_to_sollya(self._num)
			tf_den_sollya, len_den, _ = mpf_matrix_to_sollya(self._den)
			num = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(tf_num_sollya)))
			den = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(tf_den_sollya)))
			self._sollya = (num, den)

		return self._sollya




def iter_random_dTFmp(number, order=(5, 10)):
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
		yield random_dTFmp(order)

def random_dTFmp(order=(5, 10)):
	"""
		Generate a n-th order random transfer function (not necessary stable)
		Parameters:
			- order: tuple (mini,maxi) order of the filter (default:  random between 5 and 10)
	"""
	if order[0] == order[1]:
		n = order[0]
	else:
		n = randint(*order)
	num = numpy.matrix(rand(1, n))
	den = numpy.matrix(rand(1, n))
	return dTFmp(num, den)








