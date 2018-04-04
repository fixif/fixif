import mpmath
from mpmath import *
def mpc_get_real(p):
	"""
	This function takes a complex MPmath matrix and
	throws away the imaginary part returning the real
	part matrix.

	Parameters
	----------
	p - mpc matrix

	Returns
	-------
	q = matrix representing the real part of p
	"""

	q = mp.zeros(p.rows, p.cols)
	for i in range(0, p.cols):
		for j in range(0, p.rows):
			q[j,i] = p[j,i].real

	return q
