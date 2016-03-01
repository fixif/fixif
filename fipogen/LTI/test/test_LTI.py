# coding=utf8

"""
This file contains tests for the dSS functions & class
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

from numpy import array, zeros, absolute, eye, isnan, logical_and
from numpy import matrix as mat
from numpy.linalg import norm, eigvals
from numpy.testing import assert_allclose
from numpy.random import seed, randint
from sys import exc_info  # to keep trace of trace stack

from fipogen.LTI import dSS, random_dSS, get_random_dSS

import pytest

# from __builtin__ import None

#TODO: move it to func_aux
def my_assert_relativeclose ( actual, desired, rtol, strActual, strDesired, strMethod ):
	"""
	"""
	try:
		assert_allclose(actual, desired, rtol=rtol)
	except AssertionError as e:
		print("""-------------------------------------------
Test with %s
%s = %s
%s = %s
diff = %s
-------------------------------------------""" % (strMethod, strActual, repr(actual), strDesired, repr(desired), repr(actual-desired)))
		raise e


def test_construction( ):
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		dSS( [[1, 2], [3, 4], [5, 6]], 1, 2, 3 )
	with pytest.raises(ValueError):
		dSS( [[1, 2], [3, 4]], 1, 2, 3 )
	with pytest.raises(ValueError):
		dSS( [[1, 2], [3, 4]], [[1], [2]], 2, 3)
	with pytest.raises(ValueError):
		dSS( [[1, 2], [3, 4]], [[1], [2]], [[1, 2], [1, 2]], 3)

	for i in range(50):
		n=randint(2,20)
		p=randint(2,15)
		q=randint(2,15)
		S = get_random_dSS(n,p,q)

		# test for correct sizes of random dSS
		assert (S.n, S.p, S.q) == (n, p, q)
		assert S.A.shape == (n, n)
		assert S.B.shape == (n, q)
		assert S.C.shape == (p, n)
		assert S.D.shape == (p, q)

		# test for spectral radius lower than 1
		assert max(abs(eigvals(S.A))) < 1



@pytest.mark.parametrize( "S", random_dSS( 130, True, n=(2, 40), p=(2,15), q=(2,15)) )
def test_Gramians ( S ):
	"""
	Test calculation of :math:`W_o` and :math:`W_c` with different methods, namely

	- python intrinsic ``linalg``
	- ``slycot`` method from xxx

	"""

	relative_tolerance_linalg = 1e-3
	relative_tolerance_slycot1 = 1e-5


	# test with 'linalg' method
	dSS._W_method = 'linalg'
	assert_allclose( array(S.A * S.Wc * S.A.transpose() + S.B * S.B.transpose()), array(S.Wc), rtol=relative_tolerance_linalg)
	assert_allclose( array(S.A.transpose() * S.Wo * S.A + S.C.transpose() * S.C), array(S.Wo), rtol=relative_tolerance_linalg)

	# We have to explicitely remove Wo and Wc from S so that those are calculated again
	S._Wo = None
	S._Wc = None

	# test for 'slycot1' method (with slycot we expect a 8-digit accuracy)
	dSS._W_method = 'slycot1'
	assert_allclose( array(S.A * S.Wc * S.A.transpose() + S.B * S.B.transpose()), array(S.Wc), rtol=relative_tolerance_slycot1)
	assert_allclose( array(S.A.transpose() * S.Wo * S.A + S.C.transpose() * S.C), array(S.Wo), rtol=relative_tolerance_slycot1)

	# test with non-existing method
	dSS._W_method = 'toto'
	S._Wc = None
	S._Wo = None
	with pytest.raises(ValueError):
		t = S.Wc
	with pytest.raises(ValueError):
		t = S.Wo



@pytest.mark.parametrize( "S", random_dSS( 30, True, (5,10), (1,5), (1,5)) )
def test_wcpg ( S ):

	"""
	Test Worst Case Peak Gain calculation
	"""

	def calc_wcpg_approx ( S, nit ):
		"""Very bad WCPG approximation (we hope to get the first digits....)
		Only used to compare with true, reliable Anastasia's WCPG"""

		res = mat(zeros((S.p, S.q)))
		powerA = mat(eye(S.n, S.n))

		for i in range(0, nit):
			res += absolute(S.C * powerA * S.B)
			powerA = powerA * S.A

		return res + absolute(S.D)


	nit = 5000
	rel_tol_wcpg = 1e-2

	wcpg = calc_wcpg_approx(S, nit)
	W = S.WCPG()

	assert_allclose( array(W), array(wcpg), rtol=rel_tol_wcpg)


#TODO: il reste à tester:
# H2norm
# DC-gain
# addition
# multiplication
# sous-système
# str et repr