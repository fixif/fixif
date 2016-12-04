
_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2016, FIPOgen Project, LIP6"
__credits__ = ["Anastasia Volkova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Anastasia Volkova"
__email__ = "Anastasia.Volkova@lip6.fr"
__status__ = "Beta"

import mpmath
import numpy

from fipogen.func_aux import python2mpf_matrix, mpf_to_numpy, mpf_poly_mult, mp_poly_product
from fipogen.LTI import dSS, dTF

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
			if isinstance(A.numpy.matrix):
				A = python2mpf_matrix(A)
			else:
				raise ValueError('Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix but instead got %s') % type(A)
		if not isinstance(B, mpmath.matrix):
			if isinstance(B.numpy.matrix):
				B = python2mpf_matrix(B)
			else:
				raise ValueError(
					'Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix but instead got %s') % type(B)
		if not isinstance(C, mpmath.matrix):
			if isinstance(C.numpy.matrix):
				C = python2mpf_matrix(C)
			else:
				raise ValueError(
					'Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix but instead got %s') % type(C)
		if not isinstance(C, mpmath.matrix):
			if isinstance(C.numpy.matrix):
				C = python2mpf_matrix(C)
			else:
				raise ValueError(
					'Cannot create dSSmp object: expected mpmath.matrix of numpy.matrix but instead got %s') % type(D)


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


	def sub(self, S, add=False):
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

		if add:
			for i in range(0,self.p):
				for j in range(0,self.q):
					D[i, j] = mpmath.fadd(self.D[i, j], S.D[i, j], exact=True)

			for i in range(0,self.p):
				for j in range(0, S.n):
					C[i, j + self.n] = S.C[i, j]
		else:
			for i in range(0, self.p):
				for j in range(0,self.q):
					D[i, j] = mpmath.fsub(self.D[i, j], S.D[i, j], exact=True)
			for i in range(0,self.p):
				for j in range(0, S.n):
					C[i, j + self.n] = -S.C[i, j]

		return dSSmp(A, B, C, D)


	def get_dSS(self):
		return dSS(mpf_to_numpy(self._A), mpf_to_numpy(self._B), mpf_to_numpy(self._C), mpf_to_numpy(self._C))


	def get_dTFmp(self, prec):
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



		if self.p != 1 or self.q != 1:
			raise ValueError('dSS: cannot convert a dSSmp to dTFmp for not a SISO system')


		with mpmath.extraprec(prec * 6):
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
		for i in range(0, Q.rows):
			a[i, 0] = Q[i, 0].real

		mpmath.mp.prec = oldprec
		return dTFmp(b, a)


