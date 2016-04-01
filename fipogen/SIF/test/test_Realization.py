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

from fipogen.Structures import iterAllRealizations
from fipogen.LTI import Filter, iter_random_Filter, iter_random_dSS
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





@pytest.mark.parametrize( "F", iter_random_Filter(5))
def test_implementCdouble(F):
	N = 10
	for R in iterAllRealizations( F ):
		print(str(R.name)+"\t")
		u = 300*rand( N, F.q)					# random input of N samples
		yC = zeros( (N, F.p), dtype=float64)	# empty output to be computed by the `implementCdouble` code
		y = R.simulate(u.transpose()).transpose()

		func = R.implementCdouble("myFunction")
		pu_str = '*pu' if R.q==1 else 'pu'
		if R.p==1:
			iteration  = "*py = myFunction( %s, xk);"%pu_str
		else:
			iteration = "myFunction( py, %s, xk);"%pu_str
		code = """
		double xk[%d];
		double *pu = &u[0,0];
		double *py = &yC[0,0];
		for( int i=0; i<N; i++)
		{
			%s
			pu += %d;
			py += %d;
		}
		"""%(R.n, iteration, R.q, R.p)

		inline(code, ['N', 'u', 'yC'], support_code=func)

		print(y-yC)


		assert_allclose(y, yC, atol=1e-5)




