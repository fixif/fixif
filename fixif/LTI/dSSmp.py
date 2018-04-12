#import sollya

_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2016, FIPOgen Project, LIP6"
__credits__ = ["Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Anastasia Volkova"
__email__ = "Anastasia.Volkova@lip6.fr"
__status__ = "Beta"

import mpmath
import numpy

from numpy.random.mtrand import randint, rand
from fixif.func_aux import python2mpf_matrix, mpf_to_numpy, mp_poly_product, mpf_matrix_fadd, mpf_matrix_fmul, mpf_matrix_to_sollya
from fixif.LTI import random_dSS

class dSSmp(object):

	def __init__(self, A, B, C, D):
		"""
		The dSSmp class describes a discrete state space realization
		with coefficients in multiple precision

	A state space system :math:`(A,B,C,D)` is defined by

	.. math::

		\left\lbrace \begin{aligned}
		x(k+1) &= Ax(k) + Bu(k) \\
		y(k)   &= Cx(k) + Du(k)
		\end{aligned}\right.

	with :math:`A \in \mathbb{R}^{n \times n}, B \in \mathbb{R}^{n \times q}, C \in \mathbb{R}^{p \times n} \text{ and } D \in \mathbb{R}^{p \times q}`.

	**Dimensions of the state space :**

	.. math::
		:align: left
		n,p,q \in \mathbb{N}

	==  ==================
	n   number of states
	p   number of outputs
	q   number of inputs
	==  ==================

		Parameters
		----------
		A
		B
		C
		D

		Returns
		-------

		"""

		if not isinstance(A, mpmath.matrix):
			if isinstance(A, numpy.matrix):
				A = python2mpf_matrix(A)
			else:
				raise ValueError('Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix')
		if not isinstance(B, mpmath.matrix):
			if isinstance(B, numpy.matrix):
				B = python2mpf_matrix(B)
			else:
				raise ValueError('Cannot create dSSmp object: expected mpmath.matrix of numpy.matri')
		if not isinstance(C, mpmath.matrix):
			if isinstance(C, numpy.matrix):
				C = python2mpf_matrix(C)
			else:
				raise ValueError('Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix')
		if not isinstance(D, mpmath.matrix):
			if isinstance(D, numpy.matrix):
				D = python2mpf_matrix(D)
			else:
				raise ValueError('Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix')


		#checking sizes
		# n = A.rows


		if A.rows != A.cols:
			raise ValueError('Cannot create dSSmp object: incorrect sizes')
		else:
			self._n = A.rows

		if B.rows != self._n:
			raise ValueError('Cannot create dSSmp object: incorrect sizes')
		else:
			self._q = B.cols

		if C.cols != self._n:
			raise ValueError('Cannot create dSSmp object: incorrect sizes')
		else:
			self._p = C.rows

		if D.rows != self._p or D.cols != self._q:
			raise ValueError('Cannot create dSSmp object: incorrect sizes')

		self._A = A
		self._B = B
		self._C = C
		self._D = D



	@property
	def A(self):
		return self._A

	@property
	def B(self):
		return self._B

	@property
	def C(self):
		return self._C

	@property
	def D(self):
		return self._D

	@property
	def n(self):
		return self._n

	@property
	def p(self):
		return self._p

	@property
	def q(self):
		return self._q

	def __add__(self, S):
		"""
		Given a dSSmp system S the function returns a dSSmp system H,
		whcih corresponds to the difference H:=self - S in the meaning that
		y_H(k) = y_self(k) - y_S(k)

		Set add to True if you want to perfor addition of systems.

		Parameters
		----------
		S - a dSSmp system to substract
		add=False - set to True if you want addition
		Returns
		-------
		H - a filter which corresponds to the difference of systems self and S
		"""

		from fixif.LTI import dSS
		if not isinstance(S, dSSmp):
			if isinstance(S, dSS):
				S = dSSmp(S.A, S.B, S.C, S.D)
			else:
				raise ValueError('Cannot substract two dSSmp filters: expected a dSSmp but instead got %s') % type(S)

		if self.q != S.q:
			raise ValueError('Cannot substract two State-Space systems with different size of inputs')
		if self.p != S.p:
			raise ValueError('Cannot substract two State-Space systems with different size of outputs')

		A = mpmath.mp.zeros(self.n + S.n, self.n + S.n)
		B = mpmath.mp.zeros(self.n + S.n, self.q)
		C = mpmath.mp.zeros(self.p, self.n + S.n)
		D = mpmath.mp.zeros(self.p, self.q)

		for i in range(0, self.n):
			for j in range(0, self.n):
				A[i, j] = self.A[i, j]

		for i in range(0, S.n):
			for j in range(0, S.n):
				A[i + self.n, j + self.n] = S.A[i, j]

		for i in range(0, self.n):
			for j in range(0, self.q):
				B[i, j] = self.B[i, j]
		for i in range(0, S.n):
			for j in range(0, self.q):
				B[i + self.n, j] = S.B[i, j]

		for i in range(0, self.p):
			for j in range(0, self.n):
				C[i, j] = self.C[i, j]

		for i in range(0, self.p):
			for j in range(0, S.n):
				C[i, j + self.n] = S.C[i, j]

		for i in range(0, self.p):
			for j in range(0, self.q):
				D[i, j] = mpmath.fadd(self.D[i, j], S.D[i, j], exact=True)


		return dSSmp(A, B, C, D)


	def __sub__(self, S):
		"""
		Given a dSSmp system S the function returns a dSSmp system H,
		whcih corresponds to the difference H:=self - S in the meaning that
		y_H(k) = y_self(k) - y_S(k)

		Set add to True if you want to perfor addition of systems.

		Parameters
		----------
		S - a dSSmp system to substract
		add=False - set to True if you want addition
		Returns
		-------
		H - a filter which corresponds to the difference of systems self and S
		"""


		from fixif.LTI import dSS
		if not isinstance(S, dSSmp):
			if isinstance(S, dSS):
				S = dSSmp(S.A, S.B, S.C, S.D)
			else:
				raise ValueError('Cannot substract two dSSmp filters: expected a dSSmp but instead got %s') % type(S)


		if self.q != S.q:
			raise ValueError('Cannot substract two State-Space systems with different size of inputs')
		if self.p != S.p:
			raise ValueError('Cannot substract two State-Space systems with different size of outputs')


		A = mpmath.mp.zeros(self.n + S.n, self.n + S.n)
		B = mpmath.mp.zeros(self.n + S.n,self.q)
		C = mpmath.mp.zeros(self.p, self.n + S.n)
		D = mpmath.mp.zeros(self.p, self.q)

		for i in range(0, self.n):
			for j in range(0, self.n):
				A[i, j] = self.A[i, j]

		for i in range(0, S.n):
			for j in range(0, S.n):
				A[i + self.n, j + self.n] = S.A[i, j]

		for i in range(0, self.n):
			for j in range(0,self.q):
				B[i, j] = self.B[i, j]
		for i in range(0, S.n):
			for j in range(0,self.q):
				B[i + self.n, j] = S.B[i, j]

		for i in range(0,self.p):
			for j in range(0, self.n):
				C[i, j] = self.C[i, j]

		for i in range(0, self.p):
			for j in range(0, self.q):
				D[i, j] = mpmath.fsub(self.D[i, j], S.D[i, j], exact=True)
		for i in range(0, self.p):
			for j in range(0, S.n):
				C[i, j + self.n] = -S.C[i, j]

		return dSSmp(A, B, C, D)


	def to_dSS(self):
		from fixif.LTI import dSS
		return dSS(mpf_to_numpy(self._A), mpf_to_numpy(self._B), mpf_to_numpy(self._C), mpf_to_numpy(self._D))


	def to_dTFmp(self, prec=64):
		"""
		This function computes corresponding transfer function in multiple precision.
		All operations are performed with at leaste prec bits of precision for mantissas.
		Parameters
		----------
		prec - precision for the computations

		Returns
		-------
		TF - a dTFmp object

		"""
		# converting the dSS matrices to mp type

		oldprec = mpmath.mp.prec
		mpmath.mp.prec = prec

		from fixif.LTI import dTFmp

		if self.p != 1 or self.q != 1:
			raise ValueError('dSS: cannot convert a dSSmp to dTFmp for not a SISO system')

		E, V = mpmath.mp.eig(self.A)  # eig returns a list E and a matrix V
		Cmp = self.C * V
		Vinv = mpmath.mp.inverse(V)
		Bmp = Vinv * self.B

		Q = mp_poly_product([-e for e in E])
		PP = mpmath.mp.zeros(Q.rows - 1, 1)
		# tmp_polyproduct = mp.zeros([self.n, 1]) #temporary polynomial products
		for i in range(0, self.n):
			# P = sum_i=0^n c_i * b_i * product_j!=i p_j
			tmp_polyproduct = mp_poly_product([-e for e in E], i)
			PP = PP + Cmp[0, i] * Bmp[i, 0] * tmp_polyproduct


		if self.D[0, 0] != mpmath.mp.zero:
			P = self.D[0, 0] * Q
		else:
			P = mpmath.mp.zeros(Q.rows, 1)

		for i in range(1, P.rows):
			P[i, 0] = P[i, 0] + PP[i - 1, 0]

		b = mpmath.mp.zeros(P.rows, 1)
		a = mpmath.mp.zeros(Q.rows, 1)
		for i in range(0, P.rows):
			b[i, 0] = P[i, 0].real
			b[i, 0] = mpmath.fadd(b[i,0], mpmath.mp.zero, prec=prec)
		for i in range(0, Q.rows):
			a[i, 0] = Q[i, 0].real
			a[i, 0] = mpmath.fadd(a[i, 0], mpmath.mp.zero, prec=prec)

		mpmath.mp.prec = oldprec
		return dTFmp(b, a)

	def WCPGmp(self, delta=2**-53):
		"""
		This functions computes the WCPG of the state-space system
		with absolute error bounded by delta.

		The result is given as a list W of sollya objects, which represents a
		p x q WCPG matrix.


		Parameters
		----------
		delta - bound of the absolute

		Returns
		-------
		W - a list of sollya objects representing elemnts of the WCPG matrix
		"""

		import sollya
		import sys

		# load gabarit.sol
		#sollya.suppressmessage(57, 174, 130, 457)
		sollya.execute("fipogen/LTI/wcpg.sol")

		wcpg = sollya.parse("wcpg")


		#construct the inputs for the wcpg function in sollyaObject format
		A,_,_ = mpf_matrix_to_sollya(self._A)
		B,_,_ = mpf_matrix_to_sollya(self._B)
		C,_,_ = mpf_matrix_to_sollya(self._C)
		D,_,_ = mpf_matrix_to_sollya(self._D)

		#W = sollya.parse("wcpg")(A, B, C, D, self._n, self._p, self._q, eps)
		W = wcpg(A, B, C, D, self._n, self._p, self._q, delta)
		return W



	def simulate_rounded(self, u, prec=53):

		#suppose u is a mpmath matrix
		xk = mpmath.mp.zeros(self._n, 1)

		#xk = mpf_matrix_to_sollya(xk)[0]

		nSimulations = u.shape[1]
		yk = mpmath.mp.zeros(self._p, nSimulations)

		yk_sollya = mpf_matrix_to_sollya(yk)[0]
		for i in range(0, nSimulations):
			xkp1 = mpf_matrix_fmul(self._A, xk)
			xkp1 = mpf_matrix_fadd(xkp1, mpf_matrix_fmul(self._B, u[:, i]))

			yk[:, i] = mpf_matrix_fmul(self._C, xk)
			yk[:, i] = mpf_matrix_fadd(yk[:, i], mpf_matrix_fmul(self._D, u[:, i]))


			xk = mpmath.matrix([float(sollya.round(mpf_matrix_to_sollya(xkp1)[0][j], prec, sollya.RN)) for j in range(0, self._n)])
			yk_sollya[i] = sollya.round(mpf_matrix_to_sollya(yk[:,i])[0][0], prec, sollya.RN)

		return yk_sollya



	def simulate(self, u, exact=True, x0=None):
		"""
		Given a vector of inputs u this function simulates
		the output of the dSS system on these inputs.

		If the flag exact is set to True (default) then the simulation is performed
		exactly. Otherwise, on each iteration the SoPs are computed exactly and then the state variables
		are rounded to double precision.

		Parameters
		----------
		u - vector of inputs in the format numpy.matrix or mpmath.matrix of size q x T
		x0 - vector of inital states, if specified must be of size n x 1
		exact - a flag wether to perform simulations in exact (by default) or to perform

		Returns
		-------
		y -  p x T matrix of outputs

		"""

		if not isinstance(u, mpmath.matrix):
			if isinstance(u, numpy.matrix):
				u = python2mpf_matrix(u)
			else:
				raise ValueError('Cannot perform simulation: u must be either mpmath.matrix or numpy.matrix')

		if u.rows != self._q:
			raise ValueError('Cannot perform somulation: u is of incorrect size')

		xk = mpmath.mp.zeros(self._n, 1)
		if x0:
			if not isinstance(x0, mpmath.matrix):
				if isinstance(x0, numpy.matrix):
					xk = python2mpf_matrix(x0)
				else:
					raise ValueError('Cannot perform simulation: initial state specified in incorrect format')

		if xk.rows != self._n:
			raise ValueError('Cannot perform simulation: initial state is of incorrect size')

		T = u.cols
		yk = mpmath.mp.zeros(self._p, T)

		if exact:
			for i in range(0, T):
				xkp1 = mpf_matrix_fmul(self._A, xk)
				xkp1 = mpf_matrix_fadd(xkp1, mpf_matrix_fmul(self._B, u[:, i]))

				yk[:, i] = mpf_matrix_fmul(self._C, xk)
				yk[:, i] = mpf_matrix_fadd(yk[:, i], mpf_matrix_fmul(self._D, u[:, i]))

				xk = xkp1

		else:
			for i in range(0, T):
				xkp1 = mpf_matrix_fmul(self._A, xk)
				xkp1 = mpf_matrix_fadd(xkp1, mpf_matrix_fmul(self._B, u[:, i]))

				yk[:, i] = mpf_matrix_fmul(self._C, xk)
				yk[:, i] = mpf_matrix_fadd(yk[:, i], mpf_matrix_fmul(self._D, u[:, i]))

			for i in range(0, xk.rows):
				xk[i, 0] = mpmath.fadd(xkp1[i, 0], mpmath.mp.zero, prec=64, rounding='n')


		return yk







def random_dSSmp(n, p, q, pRepeat = 0.01, pReal = 0.5, pBCmask = 0.90, pDmask = 0.8, pDzero = 0.5):
	return random_dSS(n, p, q, pRepeat, pReal, pBCmask, pDmask, pDzero).to_dSSmp()



def iter_random_dSSmp(number, stable = True, n = (5, 10), p = (1, 5), q = (1, 5), pRepeat = 0.01, pReal = 0.5, pBCmask = 0.90, pDmask = 0.8, pDzero = 0.5):
	"""
	Generate some n-th order random (stable or not) state-spaces, with q inputs and p outputs
	copy/Adapted from control-python library (thanks guys): https://sourceforge.net/projects/python-control/
	possibly already adpated from Mathworks or Octave

	Parameters:
		- number: number of state-space to generate
		- stable: indicate if the state-spaces are stable or not
		- n: tuple (mini,maxi) number of states (default:  random between 5 and 10)
		- p: number of outputs (default: 1)
		- q: number of inputs (default: 1)

		- pRepeat: Probability of repeating a previous root (default: 0.01)
		- pReal: Probability of choosing a real root (default: 0.5). Note that when choosing a complex root, the conjugate gets chosen as well. So the expected proportion of real roots is pReal / (pReal + 2 * (1 - pReal))
		- pBCmask: Probability that an element in B or C will not be masked out (default: 0.9)
		- pDmask: Probability that an element in D will not be masked out (default: 0.8)
		- pDzero: Probability that D = 0 (default: 0.5)

	Returns:
		- returns a generator of dSS objects (to use in a for loop for example)

	"""
	for i in range(number):
		if stable:
			yield random_dSSmp(randint(*n), randint(*p), randint(*q), pRepeat, pReal, pBCmask, pDmask, pDzero)
		else:
			nn = randint(*n)
			pp = randint(*p)
			qq = randint(*q)
			A = numpy.matrix(rand(nn,nn))
			B = numpy.matrix(rand(nn,qq))
			C = numpy.matrix(rand(pp,nn))
			D = numpy.matrix(rand(pp,qq))

			yield dSSmp(A,B,C,D)




