import numpy as np
import mpmath



def my_forward_subst(L, i):
	"""
	This function performs the forward substitution for solution of the system
				Lx = e_i
	where
		L   - is a lower triangular matrix with 1s on the main diagonal
		e_i - i-th identity vector

	All the computations are done exactly with MPMATH

	Parameters
	----------
	L - n x n lower-triangular matrix with ones on the diagonal
	i - index for the canonical vector

	Returns
	-------
	x - n x 1 vector of the solution
	"""

	n = L.rows
	x = mpmath.zeros(n, 1)

	e = mpmath.zeros(n, 1)
	e[i, 0] = mpmath.mp.one

	x[0,0] = e[0,0]

	for i in range(1, n):
		x[i,0] = e[i]
		for j in range(0, i):
			tmp = mpmath.fmul(L[i,j], x[j,0], exact=True)
			x[i,0] = mpmath.fsub(x[i,0], tmp, exact=True)

	return x








class mpf_matrix(object):
	"""
	A mpf_matrix is a m * n matrix with mpf numbers

	"""

	def __init__(self, M):
		"""
		Build a mpf_matrix from a numpy matrix
		contains a np.matrix filled with mpf objects
		"""
		# check type
		if not isinstance(M, np.matrix):
			raise ValueError('Expected a numpy matrix, instead have %s' % type(M))

		self._n, self._m = M.shape
		self._M = mpmath.zeros(self._n, self._m)
		for i in range(0, self._n):
			for j in range(0, self._m):
				self._M[i, j] = mpmath.mpf(M[i, j])
		#TODO: use np.vectorize !

	@property
	def n(self):
		return self._n
	@property
	def m(self):
		return self._m
	@property
	def shape(self):
		return self._n, self._m

	def __getitem__(self, item):
		return self._M[item]

	def __add__(self, other):
		"""
		This function computes the sum C = self + other exactly
		other should be a numpy.matrix or a mpf_matrix
		The output matrix C is a mpf_matrix.

		Parameters:
		- self: (mpf_matrxi) - m x n matrix
		- other: mpf_matrix or numpy.matrix) m x n matrix

		Returns:
		- C: (mpf_matrix) m x n matrix
		"""
		# check input type
		if isinstance(other, np.matrix):
			other = mpf_matrix(other)
		elif not isinstance(other, mpmath.matrix):
				raise ValueError('Cannot compute exact sum of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(other)

		#test sizes
		if self.shape != other.shape:
			raise ValueError('Cannot compute exact sum of two matrices: incorrect sizes.')

		# compute the sum
		m = self._m
		n = self._n
		C = mpmath.zeros(m, n)
		for i in range(0, m):
			for j in range(0, n):
				C[i,j] = mpmath.fadd(self[i,j], other[i,j], exact=True)
				if mpmath.isnan(C[i,j]) or mpmath.isinf(C[i,j]):
					print('WARNING: in matrix sum an abnormal number (NaN/Inf) occured: %f') % C[i,j]
		# TODO: use np.vectorize !

		return mpf_matrix(C)

	def __mul__(self,other):
		"""
		This function computes the matrix multiplication C = self * other exactly
		other should be a numpy.matrix or a mpf_matrix
		The output matrix C is a mpf_matrix.

		Parameters:
		- self: (mpf_matrxi) - m x n matrix
		- other: mpf_matrix or numpy.matrix) n x p matrix

		Returns:
		- C: (mpf_matrix) m x p matrix
			"""

		# check input type
		if isinstance(other, np.matrix):
			other = mpf_matrix(other)
		elif not isinstance(other, mpmath.matrix):
				raise ValueError('Cannot compute exact multiplication of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(other)


		# test sizes
		if self.m != other.n:
			raise ValueError('Cannot compute exact product of two matrices: incorrect sizes.')

		m = self.m
		n = self.n
		p = other.m

		C = mpmath.zeros(m, p)
		for i in range(0, m):
			for j in range(0, p):
				for k in range(0, n):
					tmp = mpmath.fmul(self[i, k], other[k, j], exact=True)
					C[i, j] = mpmath.fadd(C[i, j], tmp, exact=True)
					if mpmath.isnan(C[i, j]) or mpmath.isinf(C[i, j]):
						print('WARNING: in matrix multiplication an abnormal number (NaN/Inf) occured: %f') % C[
							i, j]

		return mpf_matrix(C)


	def inv(self):
		"""
		For a lower-triangular n x n real matrix L with 1s on the main diagonal
		this function computes its inverse X exactly such that
					    L * X = I
		The function returns X as n x n real mpf_matrix

		Parameters
		----------
		L - n x n lower-triangular matrix

		Returns
		-------
		X - n x n matrix
		"""

		# checking the size
		if self.n != self.m:
			raise ValueError('Cannot compute inverse: matrix must be square but istead is %s x %s') % self.m, self.n
		else:
			n = self.n

		# checking if the matrix is indeed lower-triangular with 1s on the main diagonal
		for i in range(0, n):
			if self[i, i] != mpmath.mp.one:
				raise ValueError('Cannot compute inverse: matrix must have 1s on the main diagonal.')
			for j in range(i + 1, n):
				if self[i, j] != mpmath.mp.zero:
					raise ValueError('Cannot compute inverse: matrix must be lower triangular.')

		# compute the inverse using forward substitution
		X = mpmath.zeros(n, n)
		for i in range(0, n):
			X[:, i] = my_forward_subst(self, i)

		return mpf_matrix(X)