# coding: utf8

"""
This file contains tests for the Realization class
"""

_author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


import pytest

from fipogen.SIF import Realization
from numpy import matrix as mat, zeros,eye
from fipogen.Structures import iterAllRealizations
from fipogen.LTI import Filter, iter_random_dSS, iter_random_dTF


#from func_aux.get_data import get_data
#from func_aux.MtlbHelper import MtlbHelper


from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose


@pytest.mark.parametrize( "S", iter_random_dSS(5, n=(5,15), p=(1,5), q=(1,5) ))
def test_construction(S):
	# random SIF from dSS (J=identity, K=zero, L=zero, M=random, N=random)
	l = randint(0,10)
	JtoS = (eye((l)), zeros((S.n, l)), zeros((S.p, l)), rand(l, S.n), rand(l, S.q), S.A, S.B, S.C, S.D)
	R = Realization( Filter(ss=S), JtoS )

	assert len(R._varNameT) == l
	assert len(R._varNameX) == S.n
	assert len(R._varNameY) == S.p
	assert len(R._varNameU) == S.q





@pytest.mark.parametrize( "S", iter_random_dSS(4))
def test_algoMIMO(S):

	for R in iterAllRealizations(Filter(ss=S)):
		#R.algorithmLaTeX('testlegend')
		print( R.SIF.algorithmCdouble("myFunction") )

@pytest.mark.parametrize("H", iter_random_dTF(4))
def test_algoSISO(H):

	for R in iterAllRealizations(Filter(tf=H)):
		# R.algorithmLaTeX('testlegend')
		print(R.SIF.algorithmCdouble("myFunction"))





