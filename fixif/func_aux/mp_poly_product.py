import mpmath
from mpmath import *

from fipogen.func_aux import mpf_poly_mult


#polynomials are sto

def mp_poly_product(p, j=-1):
	"""
	Given a list of n coefficients p_i the function computes coefficients of the polynomial

		P(z) = product_i=1^n ( z + p_i )

	If the second argument j is specified, then it computes the product for all indices i != j

		P(z) = product_i=1^n, i!=j ( z + p_i )

	Parameters
	----------
	p - a list of coefficients p_i
	j - index

	Returns
	-------
	 c - coefficients of the polynomial P(z) as a MPMath matrix (possibly complex) of size degP x 1

	"""
	degP = len(p)
	if degP < 2:
		raise ValueError('error in polynomial product: empty polynomial')
	if j == -1:
		c = mp.matrix([1, p[0]])
		for i in range(1, degP):
			c = mpf_poly_mult(c, mp.matrix([mpmath.mpf(1), p[i]]))
	else:
		if j == 0:
			c = mp.matrix([1, p[1]])
			for i in range(2, degP):
				c = mpf_poly_mult(c, mp.matrix([mpmath.mpf(1), p[i]]))
		else:
			c = mp.matrix([1, p[0]])
			for i in range(1, j):
				c = mpf_poly_mult(c, mp.matrix([mpmath.mpf(1), p[i]]))

			for i in range(j + 1, degP):
				c = mpf_poly_mult(c, mp.matrix([mpmath.mpf(1), p[i]]))

	return c