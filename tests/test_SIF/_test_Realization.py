# coding: utf8

"""
This file contains tests for the Realization class
"""

_author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


import pytest
from colorama import Fore
from fixif.SIF import Realization
from numpy import zeros, eye

from fixif.Structures import iterAllRealizationsRandomFilter
from fixif.LTI import Filter, iter_random_Filter, iter_random_dSS
from fixif.Structures import State_Space

from latex import build_pdf, LatexBuildError


from numpy.random import rand, randint
from numpy.testing import assert_allclose




@pytest.mark.parametrize("S", iter_random_dSS(5, n=(5, 15), p=(1, 5), q=(1, 5)))
def test_construction_from_dSS(S):
	# random SIF from dSS (J=identity, K=zero, L=zero, M=random, N=random)
	l = randint(0, 10)
	JtoS = (eye(l), zeros((S.n, l)), zeros((S.p, l)), rand(l, S.n), rand(l, S.q), S.A, S.B, S.C, S.D)
	R = Realization(Filter(ss=S), JtoS)

	assert len(R._varNameT) == l
	assert len(R._varNameX) == S.n
	assert len(R._varNameY) == S.p
	assert len(R._varNameU) == S.q



