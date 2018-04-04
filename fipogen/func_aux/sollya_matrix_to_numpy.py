import sollya
from sollya import *
import numpy

def sollya_matrix_to_numpy(A, m, n):
	"""
	For a m x n matrix represented as a list A of Sollya objects
	this function converts the matrix A to the numpy format

	Parameters
	----------
	A - list of Sollya objects
	m - number of rows
	n = number of columns

	Returns
	-------
	B - numpy matrix
	"""

	B = numpy.matrix(numpy.zeros([m,n]))
	for i in range(0,m):
		for j in range(0,n):
			B[i,j] = float(sollya.round(A[i * n + j ], 53, sollya.RN))


	return B
