import mpmath
from mpmath import mp
import numpy
from fipogen.func_aux import python2mpf_matrix

def mpf_matrix_fadd(A, B):
	"""
	Given a m x n matrix A and m x n matrix B either in numpy.matrix
	or mpmath.matrix format,
	this function computes the sum C = A + B exactly.
	The output matrix C is always given in the MPMATH format.


	Parameters
	----------
	A - m x n matrix
	B - m x n matrix

	Returns
	-------
	C - m x n matrix
	"""

	if isinstance(A, numpy.matrix):
		try:
			A = python2mpf_matrix(A)
		except ValueError as e:
			raise ValueError('Cannot compute exact sum of two matrices. %s') % e
	else:
		if not isinstance(A, mpmath.matrix):
			raise ValueError('Cannot compute exact sum of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') %type(A)

	if isinstance(B, numpy.matrix):
		try:
			B = python2mpf_matrix(B)
		except ValueError as e:
			raise ValueError('Cannot compute exact sum of two matrices. %s') % e
	else:
		if not isinstance(B, mpmath.matrix):
			raise ValueError('Cannot compute exact sum of two matrices: unexpected input type, excpected numpy.matrix or mpmath.matrix but got %s') % type(B)


	#here both A and B are mpmath matrices
	#we consider that A and B are MPF matrices if their first elements are of type mpf, let's test it

	if not isinstance(A[0,0], mpmath.mpf) or not isinstance(B[0,0], mpmath.mpf):
		raise ValueError('Cannot compute exact product of two matrices: cannot sum complex matrices.')

	#test sizes
	if A.rows != B.rows or A.cols != B.cols:
		raise ValueError('Cannot compute exact sum of two matrices: incorrect sizes.')

	m = A.rows
	n = A.cols
	C = mp.zeros(m, n)
	for i in range(0, m):
		for j in range(0, n):
			C[i,j] = mpmath.fadd(A[i,j], B[i,j], exact=True)
			if mpmath.isnan(C[i,j]) or mpmath.isinf(C[i,j]):
				print('WARNING: in matrix sum an abnormal number (NaN/Inf) occured: %f') % C[i,j]


	return C