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
from numpy import matrix as mat, zeros,eye, empty, float64

from fipogen.Structures import iterAllRealizations, iterAllRealizationsRandomFilter
from fipogen.LTI import Filter, iter_random_Filter, iter_random_dSS, random_Filter
from scipy.weave import inline

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




seed(120)
N = 10
u = 300 * rand(N, 3)# random input of N samples

@pytest.mark.parametrize( "F", iter_random_Filter(10, q=(3,4), type='MIMO'), ids=lambda x: x.name)
#@pytest.mark.parametrize( "F", [ random_Filter(name='RandomFilter-8/4/3-396548150')], ids=lambda x: x.name)
def test_implementCdouble(F):





	for R in iterAllRealizations( F ):
	#for R in [DFI.makeRealization(F, transposed=False, nbSum=2)]:
		print(str(R.name)+"\t")

		y = R.simulate(u.transpose()).transpose()
		yC = zeros((N, F.p), dtype=float64)  # empty output to be computed by the `implementCdouble` code
		func,run_code = R.implementCdouble("myFunction")

		print( R )
		print( func)

		inline(run_code, ['N', 'u', 'yC'], support_code=func, verbose=0, force=1)

		print(u)
		print(y)
		print(yC)


		assert_allclose(y, yC, atol=1e-5)




@pytest.mark.parametrize( "R", iterAllRealizationsRandomFilter(1), ids=lambda x: x.name)
def test_rea2(R):
	N = 10
	u = 300 * rand(N, R.filter.q)  # random input of N samples
	yC = zeros((N, R.filter.p), dtype=float64)  # empty output to be computed by the `implementCdouble` code

	print(str(R.name) + "\t")

	y = R.simulate(u.transpose()).transpose()
	func, run_code = R.implementCdouble("myFunction")
	inline(run_code, ['N', 'u', 'yC'], support_code=func, verbose=0, force=1)
	assert_allclose(y, yC, atol=1e-5)

	R.filter.dSS.assert_close( R.dSS )
	if R.filter.isSISO():
		R.filter.dTF.assert_close( R.dSS.to_dTF() )



