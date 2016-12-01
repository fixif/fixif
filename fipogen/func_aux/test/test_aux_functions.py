import unittest
import numpy
import mpmath
from mpmath import *

from fipogen.func_aux import *
from fipogen.LTI import dSS, random_dSS

def my_assert_allclose_mp(A, AA, abs_tol):

	if AA.cols != A.cols or A.rows != AA.rows:
		raise ValueError('Trying to assert_close two matrices of different size! ')

	#if matrices are complex, then we need to check real and imaginary parts separately
	#we hope that if A[0,0] is complex, then all the elements are complex
	#this is to avoid the chek inside for for loops

	if abs_tol:
		if isinstance(A[0, 0], mpmath.mpc):
			for i in range(0, A.rows):
				for j in range(0, A.cols):
					if not mpmath.almosteq(A[i,j].real, AA[i,j].real, abs_eps=abs_tol) or not mpmath.almosteq(A[i,j].imag, AA[i,j.imag], abs_eps=abs_tol):
						assert False
		else:
			for i in range(0, A.rows):
				for j in range(0, A.cols):
					if not mpmath.almosteq(A[i, j], AA[i, j], abs_eps=abs_tol) :
						assert False

	else:
		assert False

	assert True

class MyTestCase(unittest.TestCase):
	def test_python2mpf_matrix(self):
		A = numpy.matrix([[1, 2, 3], [4, 5, 6]])
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

	def test_mp_poly_product(self):
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

	def test_mpf_get_representation1(self):
		a = mpf('2')
		(y,n) = mpf_get_representation(a)

		self.assertTrue(isinstance(y, long))
		self.assertEqual(y, 1L)
		self.assertEqual(n, 1)

		a = mpf('-0.125')
		(y, n) = mpf_get_representation(a)

		self.assertTrue(isinstance(y, long))
		self.assertEqual(y, -1L)
		self.assertEqual(n, -3)

		a = mpf('inf')
		try:
			(y, n) = mpf_get_representation(a)
		except ValueError:
			assert True
		else:
			assert False

		a = mpf('-inf')
		try:
			(y, n) = mpf_get_representation(a)
		except ValueError:
			assert True
		else:
			assert False

		a = mpf('nan')
		try:
			(y, n) = mpf_get_representation(a)
		except ValueError:
			assert True
		else:
			assert False


	def test_mpf_matrix_mul_exact(self):
		S = random_dSS(5, 2, 3)
		C = mpf_matrix_fmul(S.A, S.B)
		C2 = mpf_matrix_fmul(python2mpf_matrix(S.A), python2mpf_matrix(S.B))

		#TODO: add unit tests to verify exception catching

		self.assertEqual(C, C2)

	def test_mpf_matrix_fsub(self):
		A = numpy.matrix(numpy.random.rand(5, 5))

		AA = mpf_matrix_fsub(A, A)
		Z = mpmath.zeros(5,5)
		self.assertEqual(AA, Z)

		AA = mpf_matrix_fadd(AA, A)
		self.assertEqual(AA, python2mpf_matrix(A))

	def test_inverse(self):
		J = mpmath.matrix([[1, 0, 0], [2, 1, 0], [3, 4, 1]])
		Jinv = mpmath.inverse(J)
		myInverse = mpf_matrix_lt_inverse(J)

		self.assertEqual(Jinv, myInverse)



if __name__ == '__main__':
	unittest.main()
