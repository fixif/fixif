# coding: utf8

"""
This file contains tests for the SIF functions & class
"""

_author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import pytest
import numpy

from fixif.SIF import SIF
from numpy import matrix as mat
from fixif.LTI import Filter, iter_random_dTF, iter_random_dSS


#from func_aux.get_data import get_data
#from func_aux.MtlbHelper import MtlbHelper

from fixif.func_aux import mpf_to_numpy


from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose



@pytest.mark.parametrize("S", iter_random_dSS(25, n=(5, 15), p=(1, 5), q=(1, 5) ))
def test_dSSexact( S ):

	l = randint(1, 10)
	myJtoS = (numpy.eye(l), numpy.zeros((S.n, l)), numpy.zeros((S.p, l)), rand(l, S.n), rand(l, S.q), S.A, S.B, S.C, S.D)

	mySIF = SIF(myJtoS)
	SS = mySIF.dSS
	Sexact = mySIF.to_dSSexact()

	assert_allclose(SS.A, mpf_to_numpy(Sexact.A))
	assert_allclose(SS.B, mpf_to_numpy(Sexact.B))
	assert_allclose(SS.C, mpf_to_numpy(Sexact.C))
	assert_allclose(SS.D, mpf_to_numpy(Sexact.D))




def test_construction():

	for i in range(50):
		l = randint(0, 15)
		n = randint(5, 20)
		p = randint(1, 5)
		q = randint(1, 5)

		# (n,n)
		myP = mat(rand(n, n))
		# (l,l)
		myJ = mat(rand(l, l))
		# (n,l)
		myK = mat(rand(n, l))
		# (p,l)
		myL = mat(rand(p, l))
		# (l,n)
		myM = mat(rand(l, n))
		# (l,q)
		myN = mat(rand(l, q))
		# (n,q)
		myQ = mat(rand(n, q))
		# (p,n)
		myR = mat(rand(p, n))
		# (p,q)
		myS = mat(rand(p, q))

		myJtoS = [myJ, myK, myL, myM, myN, myP, myQ, myR, myS]

		# test correct obj creation
		mySIF = SIF(myJtoS)

		# testing getters/properties
		assert_allclose(mySIF.J, myJ)
		assert_allclose(mySIF.K, myK)
		assert_allclose(mySIF.L, myL)
		assert_allclose(mySIF.M, myM)
		assert_allclose(mySIF.N, myN)
		assert_allclose(mySIF.P, myP)
		assert_allclose(mySIF.Q, myQ)
		assert_allclose(mySIF.R, myR)
		assert_allclose(mySIF.S, myS)

		assert mySIF.n == n
		assert mySIF.l == l
		assert mySIF.p == p
		assert mySIF.q == q

		# test the construction with not consistent matrices
		# when the 4 sizes are all different
		if len({l, n, p, q}) == 4:
			shuffle(myJtoS)
			with pytest.raises(ValueError):
				_ = SIF(myJtoS)

