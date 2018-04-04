import sollya
from sollya import *

def sollya_matrix_print(A, m, n):
	"""
	For a m x n matrix represented as a list A of Sollya objects
	this function prints the matrix A to the standard output.

	Parameters
	----------
	A - list of Sollya objects
	m - number of rows
	n = nimber of columns

	Returns
	-------

	"""

	for i in range(0,m):
		for j in range(0,n):
			print '%s\t' % A[i* n + j],
		print('\n')


