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

from random import randint
from numpy import array, zeros, absolute, eye, isnan, logical_and
from numpy import matrix as mat
from numpy.linalg import norm, eigvals
from numpy.testing import assert_allclose
from numpy.random import seed
from sys import exc_info  # to keep trace of trace stack

from LTI import dSS
from LTI import random_dSS

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
		dSS( [[1, 2], [3, 4]], 1, 2, 3 )
		dSS( [[1, 2], [3, 4]], [1, 2], 2, 3)
		dSS( [[1, 2], [3, 4]], [1, 2], [[1, 2], [1, 2]], 3)

	for i in range(50):
		n = randint(2, 20)
		p = randint(2, 15)
		q = randint(2, 15)
		S = random_dSS(n, p, q)

		# test for correct sizes of random dSS
		assert (S.n, S.p, S.q) == (n, p, q)
		assert S.A.shape == (n, n)
		assert S.B.shape == (n, q)
		assert S.C.shape == (p, n)
		assert S.D.shape == (p, q)

		# test for spectral radius lower than 1
		assert max(abs(eigvals(S.A))) < 1




def test_Gramians ( ):
	"""
	Test calculation of :math:`W_o` and :math:`W_c` with different methods, namely

	- python intrinsic ``linalg``
	- ``slycot`` method from xxx

	"""

	relative_tolerance_linalg = 1e-3
	relative_tolerance_slycot1 = 1e-5

	# test number
	nloc = 0

	for i in range(50):

		nloc += 1
		n = randint(2, 40)
		p = randint(2, 15)
		q = randint(2, 15)
		S = random_dSS(n, p, q)

		# test with 'linalg' method
		dSS._W_method = 'linalg'
		my_assert_relativeclose( array(S.A * S.Wc * S.A.transpose() + S.B * S.B.transpose()),
								array(S.Wc),
								rtol=relative_tolerance_linalg,
								strActual="A*Wc*A' + B*B'",
								strDesired='Wc',
								strMethod='linalg (test #%d)' % nloc)
		my_assert_relativeclose( array(S.A.transpose() * S.Wo * S.A + S.C.transpose() * S.C),
								array(S.Wo),
								rtol=relative_tolerance_linalg,
								strActual="A'*Wo*A + C'*C",
								strDesired='Wo',
								strMethod='linalg (test #%d)' % nloc)

		# We have to explicitely remove Wo and Wc from S so that those are calculated again
		S._Wo = None
		S._Wc = None

		# test for 'slycot1' method
		# with slycot we expect a 8-digit accuracy

		dSS._W_method = 'slycot1'
		my_assert_relativeclose( array(S.A * S.Wc * S.A.transpose() + S.B * S.B.transpose()),
								array(S.Wc),
								rtol=relative_tolerance_slycot1,
								strActual="A*Wc*A' + B*B'",
								strDesired='Wc',
								strMethod='slycot1 (test #%d)' % nloc)

		my_assert_relativeclose( array(S.A.transpose() * S.Wo * S.A + S.C.transpose() * S.C),
								array(S.Wo),
								rtol=relative_tolerance_slycot1,
								strActual="A'*Wo*A + C'*C",
								strDesired='Wo',
								strMethod='slycot1 (test #%d)' % nloc)

def test_wcpg ( ):

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
	rel_tol_wcpg = 1e-3
	nloc = 0

	for i in range(20):

		nloc += 1
		n = randint(5, 10)
		p = randint(1, 5)
		q = randint(1, 5)
		S = random_dSS(n, p, q)

		wcpg = calc_wcpg_approx(S, nit)
		W = S.WCPG()
		my_assert_relativeclose(array(W),
								array(wcpg),
								rtol=rel_tol_wcpg,
								strActual="WCPG dprec",
								strDesired="WCPG approx",
								strMethod="compare methods")


