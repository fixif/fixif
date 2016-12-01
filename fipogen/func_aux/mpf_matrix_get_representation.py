import mpmath
import numpy
from fipogen.func_aux import mpf_get_representation

def mpf_matrix_get_representation(A):
	"""
	Given a floating-point multiple precision matrix A of size p x q the function
	returns a tuple (Y, N), where Y_ij and N_ij are such that
			A_ij = Y_ij * 2 ** N_ij
	Where Y is a matrix of long integers and N is a matrix of either integers either long integers.

	Returns
	-------
	Y - p x q matrix of type long
	N - p x q matrix of type int or long
	"""

	Y = numpy.zeros([A.rows, A.cols], dtype=object)
	N = numpy.zeros([A.rows, A.cols], dtype=object)

	for i in range(0, A.rows):
		for j in range(0, A.cols):
			try:
				Y[i,j], N[i,j] = mpf_get_representation(A[i,j])
			except ValueError as e:
				raise ValueError('Cannot get representation of MPF matrix. %s ' %e)


	return Y, N

