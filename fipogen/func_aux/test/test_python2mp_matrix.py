import unittest
import numpy as np
from fipogen.func_aux import python2mpf_matrix, mpf_poly_mult, mp_poly_product
from mpmath import *

class MyTestCase(unittest.TestCase):
	def test_python2mpf_matrix(self):
		A = np.matrix([[1, 2, 3], [4, 5, 6]])
		B = python2mpf_matrix(A)
		self.assertEqual(B.rows, 2)
		self.assertEqual(B.cols, 3)
		self.assertEqual((A[0,:] - B[0,:]).all(), mpf('0.0'))
		self.assertEqual((A[1, :] - B[1, :]).all(), mpf('0.0'))

	def test_mpf_poly_mult1(self):
		with self.assertRaises(ValueError) as context:
			p = 0
			q = 0
			mpf_poly_mult(p,q)
		self.assertTrue(context.exception)

	def test_mpf_poly_mult2(self):
		p = matrix([1, 1])
		q = matrix([1, -1])
		c = mpf_poly_mult(p, q)
		res = matrix([1, 0, -1])
		self.assertEqual(c, res)

	def test_mp_poly_product1(self):
		p = [-1, -2, -3]
		c = mp_poly_product(p)
		res = matrix([1,-6,11,-6])
		self.assertEqual(c, res)

	def test_mp_poly_product1(self):
		p = [-1, -2, -3]
		c = mp_poly_product(p, 0)
		res = matrix([1, -5, 6])
		self.assertEqual(c, res)

	def test_mp_poly_product2(self):
		p = [-1, -2, -3]
		c = mp_poly_product(p, 1)
		res = matrix([1, -4, 3])
		self.assertEqual(c, res)







	def test_mp_poly_product3(self):
		p = [-1, -2, -3]
		c = mp_poly_product(p, 2)
		res = matrix([1, -3, 2])
		self.assertEqual(c, res)




if __name__ == '__main__':
	unittest.main()
