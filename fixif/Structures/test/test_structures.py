# coding: utf8

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from fixif.Structures import iterAllRealizations, LWDF
from fixif.LTI import Filter, iter_random_Filter, random_Filter
from fixif.LTI import iter_random_Butter
from fixif.LTI import iter_random_dTF
from fixif.Structures import DFI

import pytest
import numpy


@pytest.mark.parametrize("H", iter_random_dTF(20))
def test_buildAllPossibleSISORealizationsFromdTF(H):
    """
	Check all the SISO structures (including MIMO structures)
	check that the correspong transfer function is equal to the initial transfer function
	"""
    print('')

    for R in iterAllRealizations(Filter(tf=H, stable=False)):
        print(R.name + "\t")
        H.assert_close(R.dSS.to_dTF(), eps=1e-6)


@pytest.mark.parametrize("F", iter_random_Filter(20, n=(5, 15), p=(1, 5), q=(1, 5)))
def test_buildAllPossibleMIMORealizationsFromdSS(F):
    """
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
    print('')
    for R in iterAllRealizations(F):
        print(R.name + "\t")
        F.dSS.assert_close(R.dSS)


@pytest.mark.parametrize("F", iter_random_Filter(20, n=(5, 10), p=(1, 2), q=(1, 2)))
def test_buildAllPossibleStableSISORealizationsFromdSS(F):
    """
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
    print('')
    for R in iterAllRealizations(F):
        print(R.name + "\t")
        # F.dSS.assert_close( R.dSS )
        F.dTF.assert_close(R.to_dTF(), eps=1e-4)


# @pytest.mark.parametrize( "F", iter_random_Filter(20, n=(3, 15), p=(1, 2), q=(1, 2)))
def test_LWDF():
    """
	Check the LWDF structure
	check that the correspong transfer function is equal to the initial transfer function
	"""

    b = numpy.matrix([3.770838943200613e-04, - 2.024690051110791e-04, 3.407766155670199e-04, 3.407766155670199e-04, \
                      - 2.024690051110791e-04, 3.770838943200613e-04])
    a = numpy.matrix([1.000000000000000e+00, - 4.340164570232563e+00, 7.668918353331406e+00, - 6.884599315526233e+00, \
                      3.136630548401215e+00, - 5.797542329642728e-01])

    F = Filter(num=b, den=a)
    if F.dTF._order % 2 == 1:
        R = LWDF.makeRealization(F)
        F.dTF.assert_close(R.to_dTF(), eps=1e-8)
    else:
        assert False
