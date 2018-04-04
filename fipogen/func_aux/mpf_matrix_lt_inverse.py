import mpmath
from mpmath import mp
import numpy
from fipogen.func_aux import python2mpf_matrix

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



def mpf_matrix_lt_inverse(L):
	"""
	For a lower-triangular n x n real matrix L with 1s on the main diagonal
	this function computes its inverse X exactly such that
				    L * X = I
	Matrix L must be in the numpy.matrix of mpmath.matrix formats.
	The function returns X as n x n real a mpmath.matrix


	Parameters
	----------
	L - n x n lower-triangular matrix

	Returns
	-------
	X - n x n matrix

	"""

	if isinstance(L, numpy.matrix):
		try:
			L = python2mpf_matrix(L)
		except ValueError as e:
			raise ValueError('Cannot compute exact difference of two matrices. %s') % e
	else:
		if not isinstance(L, mpmath.matrix):
			raise ValueError('Cannot compute exact difference of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(L)


	#checking the size
	if L.rows != L.cols:
		raise ValueError('Cannot compute inverse: matrix must be square but istead is %s x %s') % L.rows, L.cols
	else:
		n = L.rows

	#checking if the matrix is indeed lower-triangular with 1s on the main diagonal
	for i in range(0,n):
		if L[i,i] != mpmath.mp.one:
			raise ValueError('Cannot compute inverse: matrix must have 1s on the main diagonal.')
		for j in range(i+1, n):
			if L[i,j] != mpmath.mp.zero:
				raise ValueError('Cannot compute inverse: matrix must be lower triangular.')


	X = mp.zeros(n, n)
	for i in range(0,n):
		X[:, i] = my_forward_subst(L, i)


	return X
