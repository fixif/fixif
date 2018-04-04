import mpmath
from mpmath import *

def mpf_poly_mult(p, q):
	if(not isinstance(p, mp.matrix) or not isinstance(q, mp.matrix)):
		raise ValueError('ERROR: cannot multiply two mpf polynomials: expected two mpf matrices of size degree x 1 ')

	# given two polynomials p and q of degree degP and degQ, the polynomial
	# c = p * q of degree degC=degP+degQ has coefficients
	#			c_k = sum_i=0^k {p_i * q_(k-i)}

	#polynomials are represented as mp.matrices with cols=1 and rows=degree

	degP = p.rows-1
	degQ = q.rows-1
	c = mp.zeros(degP + degQ+1, 1)
	#p = matrix([p[:,0], mp.zeros(c.rows - p.rows, 1)])
	#q = matrix([q[:,0], mp.zeros(c.rows - q.rows, 1)])

	pp = mp.zeros(c.rows, c.cols)
	qq = mp.zeros(c.rows, c.cols)
	for i in range(0, p.rows):
		pp[i,0] = p[i,0]
	for i in range(0, q.rows):
		qq[i, 0] = q[i, 0]

	for i in range (0, c.rows):
		c[i, 0] = nsum(lambda j: pp[j,0] * qq[i - j, 0], [0, i])

	return c





