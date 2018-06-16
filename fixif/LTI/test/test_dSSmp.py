_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2016, FiXiF Project, LIP6"
__credits__ = ["Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Anastasia Volkova"
__email__ = "Anastasia.Volkova@lip6.fr"
__status__ = "Beta"

import pytest
import numpy
import mpmath
# from numpy.testing import assert_allclose
# from fixif.func_aux import *

from fixif.LTI import dSSmp, iter_random_dSSmp, Filter, iter_random_dSS
# from fixif.SIF import SIF
# from fixif.Structures import State_Space


def my_assertEqual_matrix(A, B):
	if not isinstance(A, mpmath.matrix) and not isinstance(B, mpmath.matrix):
		raise ValueError('Cannot assert matrices: expected mpmath.matrix.')

	if A.rows != B.rows or A.cols != B.cols:
		raise ValueError('Cannot assert matrices: matrices must be of the same size!')

	for i in range(0, A.rows):
		for j in range(0, A.cols):
			if not A[i, j] - B[i, j] == mpmath.mp.zero:
				raise ValueError('Matrices are not equal.')

	assert True


def my_assertAlmostEqual_matrix(A, B, rel_eps=None, abs_eps=None):
	if not isinstance(A, mpmath.matrix) and not isinstance(B, mpmath.matrix):
		raise ValueError('Cannot assert matrices: expected mpmath.matrix.')

	if A.rows != B.rows or A.cols != B.cols:
		raise ValueError('Cannot assert matrices: matrices must be of the same size!')

	for i in range(0, A.rows):
		for j in range(0, A.cols):
			if not mpmath.almosteq(A[i, j], B[i, j], rel_eps, abs_eps):
				raise ValueError('Matrices are not almost equal.')

	assert True



def test_construction():
	with pytest.raises(ValueError):
		dSSmp(numpy.matrix([[1.0, 2], [3, 4], [5, 6]]), 1, 2, 3)
	with pytest.raises(ValueError):
		dSSmp([[1, 2], [3, 4]], 1, 2, 3)
	with pytest.raises(ValueError):
		dSSmp([[1, 2], [3, 4]], [[1], [2]], 2, 3)
	with pytest.raises(ValueError):
		dSSmp([[1, 2], [3, 4]], [[1], [2]], [[1, 2], [1, 2]], 3)


# @pytest.mark.parametrize("S", iter_random_dSSmp(20, False, n=(3, 10), p=(1,5), q=(1,5)))
@pytest.mark.parametrize("S", iter_random_dSSmp(20, True, (5, 10), (1, 5), (1, 5), pBCmask=0.1))
def test_to_dSS(S):

	Sd = S.to_dSS()
	Sdd = Sd.to_dSSmp()

	my_assertAlmostEqual_matrix(S.A, Sdd.A)
	my_assertAlmostEqual_matrix(S.B, Sdd.B)
	my_assertAlmostEqual_matrix(S.C, Sdd.C)
	my_assertAlmostEqual_matrix(S.D, Sdd.D)


# @pytest.mark.parametrize("S", iter_random_dSSmp(1, False, n=(3, 4), p=(1, 2), q=(3, 4)))
# def test_simulate( S ):
# 	u = numpy.matrix([[-1, -1, -1], [1, 1, 1], [-1, 1, -1], [1, -1, 1]])
# 	y = S.simulate(u.transpose(), exact=False)
#
# 	Sd = S.to_dSS()

@pytest.mark.parametrize("S", iter_random_dSS(25, True, (5, 10), (1, 2), (1, 2), pBCmask=0.1))
def test_WCPGmp(S):

	from fixif.Structures import State_Space
	F = Filter(A=S.A, B=S.B, C=S.C, D=S.D)
	R = State_Space(F)
	Rq = R.quantize(16)
	Sq = Rq.to_dSSexact()
	l = list()

	for prec in range(50, 1000, 100):
		H_hat = Sq.to_dTFmp(prec)
		S_H = H_hat.to_dSSmp()
		S_delta = Sq - S_H
		W = S_delta.WCPGmp(prec)
		print('WCPG = %s' % W[0])
		l.append(W[0])
		if str(W[0]) == '0':
			break

	print(l)
	for i in range(0, len(l)-1):
		if l[i] > l[i+1]:
			print('l[%d] > l[%d]' % (i, i+1))
		elif l[i] == l[i + 1]:
			print('l[%d] > l[%d]' % (i, i + 1))
		else:
			print('l[%d] < l[%d]' % (i, i + 1))




@pytest.mark.parametrize("S", iter_random_dSSmp(20, False, n=(3, 6), p=(1, 2), q=(1, 2)))
def test_sub(S):

	Sadd = S + S
	Ssub = Sadd - S

	u = numpy.matrix(numpy.random.rand(1, 100))
	my_assertAlmostEqual_matrix(S.simulate(u, exact=True), Ssub.simulate(u, exact=True))


