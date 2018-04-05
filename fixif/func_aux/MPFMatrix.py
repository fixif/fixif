import numpy
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





class MPFMatrix(object):
	"""
	A MPFMatrix is a m * n matrix with mpf numbers

	"""

	def __init__(self, M):
		"""

		"""

		if isinstance(M, numpy.ndarray):
			self._M = mpmath.matrix(M)
		elif isinstance(M, mpmath.matrix):
			self._M = M.copy()
		elif isinstance(M, numpy.matrix):
			n, m = M.shape
			self._M = mpmath.zeros(n, m)
			for i in range(0, n):
				for j in range(0, m):
					self._M[i, j] = mpmath.mpf(M[i, j])
		else:
			raise ValueError('Cannot create a MPFmatrix: unknown object type %s' % type(M))



	@property
	def matrix(self):
		return self._M

	@property
	def rows(self):
		return self._M.rows

	@property
	def cols(self):
		return self._M.cols

	@property
	def shape(self):
		return self.rows, self.cols

	def __str__(self):
		return self._M.__str__()

	def __getitem__(self, item):
		return self._M[item]

	def __add__(self, other):
		if isinstance(other, numpy.matrix) or isinstance(other, numpy.ndarray):
			other = MPFMatrix(other)
			return MPFMatrix(self._M + other._M)
		elif isinstance(other, MPFMatrix):
			return MPFMatrix(self._M + other._M)
		elif isinstance(other, mpmath.matrix):
			return MPFMatrix(self._M + other)
		else:
			raise ValueError ('Cannot add two MPFMatrix objects: unknown operand type')

	def __sub__(self, other):
		if isinstance(other, numpy.matrix) or isinstance(other, numpy.ndarray):
			other = MPFMatrix(other)
			return MPFMatrix(self._M - other._M)
		elif isinstance(other, MPFMatrix):
			return MPFMatrix(self._M - other._M)
		elif isinstance(other, mpmath.matrix):
			return MPFMatrix(self._M - other)
		else:
			raise ValueError('Cannot add two MPFMatrix objects: unknown operand type')

	def __mul__(self, other):
		if isinstance(other, numpy.matrix) or isinstance(other, numpy.ndarray):
			other = MPFMatrix(other)
			return MPFMatrix(self._M * other._M)
		elif isinstance(other, MPFMatrix):
			return MPFMatrix(self._M * other._M)
		elif isinstance(other, mpmath.matrix):
			return MPFMatrix(self._M * other)
		else:
			raise ValueError('Cannot multiply two MPFMatrix objects: unknown operand type')



	def add_exact(self, other):
		"""
		This function computes the sum C = self + other exactly
		other should be a numpy.matrix or a MPFMatrix
		The output matrix C is a MPFMatrix.

		Parameters:
		- self: (mpf_matrix) - m x n matrix
		- other: MPFMatrix m x n matrix

		Returns:
		- C: (MPFMatrix) m x n matrix
		"""
		# check input type

		if not isinstance(other, MPFMatrix):
				raise ValueError('Cannot compute exact sum of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(other)

		#test sizes
		if self.shape != other.shape:
			raise ValueError('Cannot compute exact sum of two matrices: incorrect sizes.')

		# compute the sum
		m = self._M.rows
		n = self._M.cols
		C = mpmath.zeros(m, n)
		for i in range(0, m):
			for j in range(0, n):
				C[i,j] = mpmath.fadd(self[i,j], other[i,j], exact=True)
				if mpmath.isnan(C[i,j]) or mpmath.isinf(C[i,j]):
					print('WARNING: in matrix sum an abnormal number (NaN/Inf) occured: %f') % C[i,j]
		# TODO: use np.vectorize !

		return MPFMatrix(C)

	def sub_exact(self, other):
		"""
		This function computes the sum C = self - other exactly
		other should be a numpy.matrix or a MPFMatrix
		The output matrix C is a MPFMatrix.

		Parameters:
		- self: (mpf_matrix) - m x n matrix
		- other: MPFMatrix m x n matrix

		Returns:
		- C: (MPFMatrix) m x n matrix
		"""
		# check input type

		if not isinstance(other, MPFMatrix):
			raise ValueError('Cannot compute exact sum of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(other)

		# test sizes
		if self.shape != other.shape:
			raise ValueError('Cannot compute exact sum of two matrices: incorrect sizes.')

		# compute the sum
		m = self._M.rows
		n = self._M.cols
		C = mpmath.zeros(m, n)
		for i in range(0, m):
			for j in range(0, n):
				C[i, j] = mpmath.fsub(self[i, j], other[i, j], exact=True)
				if mpmath.isnan(C[i, j]) or mpmath.isinf(C[i, j]):
					print('WARNING: in matrix sum an abnormal number (NaN/Inf) occured: %f') % C[i, j]
		# TODO: use np.vectorize !

		return MPFMatrix(C)



	def mul_exact(self, other):
		"""
		This function computes the matrix multiplication C = self * other exactly
		other should be a numpy.matrix or a MPFMatrix
		The output matrix C is a MPFMatrix.

		Parameters:
		- self: (mpf_matrxi) - m x n matrix
		- other: MPFMatrix or numpy.matrix or mpmath.mp n x p matrix

		Returns:
		- C: (MPFMatrix) m x p matrix
			"""

		# check input type
		if not isinstance(other, MPFMatrix):
			raise ValueError('Cannot compute exact product of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(other)

		# test sizes


		if self.rows != other.cols:
			raise ValueError('Cannot compute exact product of two matrices: incorrect sizes.')

		m = self.rows
		n = self.rows
		p = other.cols

		C = mpmath.zeros(m, p)
		for i in range(0, m):
			for j in range(0, p):
				for k in range(0, n):
					tmp = mpmath.fmul(self[i, k], other[k, j], exact=True)
					C[i, j] = mpmath.fadd(C[i, j], tmp, exact=True)
					if mpmath.isnan(C[i, j]) or mpmath.isinf(C[i, j]):
						print('WARNING: in matrix multiplication an abnormal number (NaN/Inf) occured: %f') % C[i, j]

		return MPFMatrix(C)


	def inv_lowtr(self):
		"""
		For a lower-triangular n x n real matrix L with 1s on the main diagonal
		this function computes its inverse X exactly such that
					    L * X = I
		The function returns X as n x n real MPFMatrix

		Parameters
		----------
		L - n x n lower-triangular matrix

		Returns
		-------
		X - n x n matrix
		"""

		# checking the size
		if self.rows != self.cols:
			raise ValueError('Cannot compute inverse: matrix must be square but istead is %s x %s' % self.rows, self.cols)
		else:
			n = self.rows

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
			X[:, i] = my_forward_subst(self._M, i)

		return MPFMatrix(X)

	def to_numpy(self):
		"""
			This function rounds the elements of mpmath matrix self to double precision
			and returns a numpy matrix with the result. Rounding is done with
			the python built-in command float().

			Parameters
			----------
			self - mpf matrix

			Returns
			-------
			M - numpy matrix

			"""

		m = self.rows
		n = self.cols
		M = numpy.matrix(numpy.zeros([m, n]))
		for i in range(0, m):
			for j in range(0, n):
				M[i, j] = float(self[i, j])

		return M

	def get_int_representation(self):
		"""
		Given a mpmath matrix self the function
		returns a tuple (Y, N), where Y_ij and N_ij are such that
				self_ij = Y_ij * 2 ** N_ij
		Where Y is a matrix of long integers and N is a matrix of either integers either long integers.

		Returns
		-------
		Y - p x q matrix of type long
		N - p x q matrix of type int or long
		"""

		from fixif.func_aux import mpf_get_representation
		Y = numpy.zeros([self.rows, self.cols], dtype=object)
		N = numpy.zeros([self.rows, self.cols], dtype=object)

		for i in range(0, self.rows):
			for j in range(0, self.cols):
				try:
					Y[i, j], N[i, j] = mpf_get_representation(self[i, j])
				except ValueError as e:
					raise ValueError('Cannot get representation of MPF matrix. %s ' % e)

		return Y, N

	def to_sollya(self):
		"""
			This function converts self to its sollya representation S.
			S is a list of sollya numbers such that

			self[i,j] =: S[i + j * n] for i=1..m and j=1..n


			Parameters
			----------
			self - m x n mpmath matrix

			Returns
			-------
			S - list of n + m  sollya objects
			m - number of rows
			n - number of columns
			"""


		# First, we need to get the (long, long) representation of the matrix A
		# We compute matrices Y and N such that A[i,j] = Y[i,j] * 2 ** N[i,j]

		(Y, N) = self.get_int_representation()

		import sollya
		m = self.rows
		n = self.cols
		S = list()
		for i in range(0, m):
			for j in range(0, n):
				s = sollya.SollyaObject(Y[i, j]) * 2 ** sollya.SollyaObject(N[i, j])
				S.append(s)

		return S, m, n

	def almost_close(self, other, abs_eps = 0):
		"""
		Compare if self is almost close to the object other, which can be either a MPFmatrix or a mpmath.matrix.
		Uses the almost-eq function from MPMATH with absolute bound on the difference element-by-element.

		Parameters
		----------
		other   - a MPFmatrix of mpmath.matrix of the sam size as self
		abs_eps - absolute bound on the elenemt-by-element relative difference between self and other

		Returns
		-------
		boolean - True if for all element matrices are close, False otherwise
		"""
		if not isinstance(other, MPFMatrix):
			other = MPFMatrix(other)

		if self.shape != other.shape:
			raise ValueError('Cannot compare matrices of different sizes')

		for i in range(0, self.rows):
			for j in range(0, self.cols):
				if not mpmath.almosteq(self[i, j], other[i, j], abs_eps=abs_eps):
					return False

		return True

	def equal(self, other):
		"""
		Compare if self is equal to the object other, which can be either a MPFmatrix or a mpmath.matrix.
		Uses the almost-eq function from MPMATH with absolute bound on the difference element-by-element.

		Parameters
		----------
		self - MPFMatrix
		other - MPFMatrix or something convertable to it

		Returns
		-------
		boolean - True if for all element matrices are close, False otherwise
		"""
		if not isinstance(other, MPFMatrix):
			other = MPFMatrix(other)

		if self.shape != other.shape:
			raise ValueError('Cannot compare matrices of different sizes')

		for i in range(0, self.rows):
			for j in range(0, self.cols):
				if not self[i, j] == other[i, j]:
					return False

		return True

