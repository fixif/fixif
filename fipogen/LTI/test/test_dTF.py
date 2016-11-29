# coding=utf8

"""
This file contains tests for the dTF class and its methods
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fipogen.LTI import dTF, iter_random_dTF, TFmp_to_dSSmp, to_dTFmp
from fipogen.func_aux import python2mpf_matrix
import mpmath
import pytest


def my_assert_allclose_mp(A, AA, tol):

	if AA.cols != A.cols or A.rows != AA.rows:
		raise ValueError('Trying to assert_close two matrices of different size! ')

	#if matrices are complex, then we need to check real and imaginary parts separately
	#we hope that if A[0,0] is complex, then all the elements are complex
	#this is to avoid the chek inside for for loops
	if isinstance(A[0,0], mpmath.mpc):
		for i in range(0, A.rows):
			for j in range(0, A.cols):
				if mpmath.fabs(A[i, j].real - AA[i, j].real) > tol or mpmath.fabs(A[i, j].imag - AA[i, j].imag) > tol:
					#raise ValueError("Two complex MP matrices are not close.")
					assert(False)
	else:
		for i in range(0, A.rows):
			for j in range(0, A.cols):
				if mpmath.fabs(A[i, j] - AA[i, j]) > tol:
					#raise ValueError("Two MP matrices are not close.")
					assert (False)

	assert(True)


def test_construction( ):
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		dTF( [1, 2, 3], [0, 6 ,7] )		# den[0] cannot be zero
	with pytest.raises(ValueError):
		dTF( [1, 2, 3], [1, 2] )		# num should not be longer than den


@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_str( H ):
	str(H)


@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_to_dSS( H ):
	S = H.to_dSS()
	HH = S.to_dTF()

	H.assert_close( HH )


@pytest.mark.parametrize("H", iter_random_dTF(20, order=(3,10)))
def test_TFmp_to_dSSmp( H ):

	prec = 100
	b = python2mpf_matrix(H.num)
	a = python2mpf_matrix(H.den)
	b = b.transpose()
	a = a.transpose()

	A,B,C,D = TFmp_to_dSSmp(b, a, mpmatrices=True,prec=prec)
	#Ad, Bd, Cd, Dd = TFmp_to_dSSmp(b, a, mpmatrices=False,prec=prec)
	bb, aa = to_dTFmp(A, B, C, D, prec)
	my_assert_allclose_mp(bb, b, 1e-16)
	my_assert_allclose_mp(aa, a, 1e-16)

