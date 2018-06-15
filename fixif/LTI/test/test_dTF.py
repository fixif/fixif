# coding=utf8

"""
This file contains tests for the dTF class and its methods
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fixif.LTI import dTF, iter_random_dTF

import mpmath
import pytest


def my_assert_allclose_mp(A, AA, abs_tol):

	if AA.cols != A.cols or A.rows != AA.rows:
		raise ValueError('Trying to assert_close two matrices of different size! ')

	# if matrices are complex, then we need to check real and imaginary parts separately
	# we hope that if A[0,0] is complex, then all the elements are complex
	# this is to avoid the chek inside for for loops

	if abs_tol:
		if isinstance(A[0, 0], mpmath.mpc):
			for i in range(0, A.rows):
				for j in range(0, A.cols):
					if not mpmath.almosteq(A[i, j].real, AA[i, j].real, abs_eps=abs_tol) or not mpmath.almosteq(A[i, j].imag, AA[i, j].imag, abs_eps=abs_tol):
						assert False
		else:
			for i in range(0, A.rows):
				for j in range(0, A.cols):
					if not mpmath.almosteq(A[i, j], AA[i, j], abs_eps=abs_tol):
						assert False

	else:
		assert False

	assert True


def test_construction():
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		dTF([1, 2, 3], [0, 6, 7])		# den[0] cannot be zero
	# with pytest.raises(ValueError):
	# 	dTF( [1, 2, 3], [1, 2] )		# num should not be longer than den


@pytest.mark.parametrize("H", iter_random_dTF(20))
def test_str(H):
	print(str(H))


@pytest.mark.parametrize("H", iter_random_dTF(20))
def test_to_dSS(H):
	S = H.to_dSS()
	HH = S.to_dTF()

	H.assert_close(HH)



