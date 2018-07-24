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

from fixif.Structures import iterAllRealizationsRandomFilter
from fixif.LTI import iter_random_Filter
from fixif.Structures import State_Space

from numpy.random import rand
from numpy.testing import assert_allclose



@pytest.mark.parametrize("F", iter_random_Filter(5, ftype='SISO'), ids=lambda x: x.name)
# @pytest.mark.parametrize("F", [random_Filter(name='RandomFilter-8/4/3-396548150')], ids=lambda x: x.name)
def test_implementCdouble(F):

	N = 10
	u = 3000 * rand(F.q, N)  # random input of N samples

	from numpy.linalg import norm

	for R in F.iterAllRealizations():
		print('\n'+Fore.RED + str(R.name) + Fore.RESET+'\n\t')

		# y = R.simulateMP(u)
		yb = R.simulate(u)
		yC = R.runCdouble(u)

		assert norm(yb-yC) < 1e-5



@pytest.mark.parametrize("F", iter_random_Filter(5, ftype='SISO'), ids=lambda x: x.name)
def test_makeModule(F):
	R = State_Space(F)
	R.makeModule()


@pytest.mark.parametrize("R", iterAllRealizationsRandomFilter(1), ids=lambda x: x.name)
def test_rea2(R):
	u = 30 * rand(R.filter.q, 1)  # random input of N samples

	print(str(R.name) + "\t")

	y = R.simulate(u)
	yC = R.runCdouble(u)
	assert_allclose(y, yC, atol=1e-5)

	R.filter.dSS.assert_close(R.dSS)
	if R.filter.isSISO():
		R.filter.dTF.assert_close(R.dSS.to_dTF())

