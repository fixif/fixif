import mpmath
import numpy

def mpf_to_numpy(A):
	"""
	Given an mpf matrix, this function rounds its elements to double precision
	and returns a numpy matrix with the result. Rounding is done with
	the python built-in command float().

	Parameters
	----------
	A - mpf matrix

	Returns
	-------
	M - numpy matrix

	"""

	if isinstance(A, mpmath.mpf):
		return float(A)

	if not isinstance(A, mpmath.matrix):
		raise ValueError('Expected a scalar or matrix MPF input')

	m = A.rows
	n = A.cols
	M = numpy.zeros([m,n])
	for i in range(0,m):
		for j in range(0, n):
			M[i,j] = float(A[i,j])

	return M