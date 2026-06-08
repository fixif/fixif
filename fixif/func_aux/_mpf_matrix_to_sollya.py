import mpmath
#import sollya
#from sollya import *
from fixif.func_aux import mpf_matrix_get_representation

def mpf_matrix_to_sollya(A):
	"""
	For a real m x n matrix A in mpmath.matrix format
	this function converts it to the sollya representation S.
	S is a list of sollya numbers such that

	A[i,j] =: S[i + j * n] for i=1..m and j=1..n


	Parameters
	----------
	A - m x n mpmath matrix

	Returns
	-------
	S - list of n * m  sollya objects
	m - number of rows
	n - number of columns
	"""

	if not isinstance(A,mpmath.matrix):
		raise ValueError('Cannot convert matrix to sollya: expected mpmath.matrix but instead got %s') % type(A)

	if not isinstance(A[0,0], mpmath.mpf):
		raise ValueError('Cannot convert matrix to sollya: expected a real matrix but instead got %s') % type(A[0,0])

	#First, we need to get the (long, long) representation of the matrix A
	#We compute matrices Y and N such that A[i,j] = Y[i,j] * 2 ** N[i,j]

	(Y, N) = mpf_matrix_get_representation(A)

	m = A.rows
	n = A.cols
	S = list()
	for i in range(0, m):
		for j in range(0,n):
			s = sollya.SollyaObject(Y[i,j]) * 2**sollya.SollyaObject(N[i,j])
			S.append(s)


	return S, m, n


