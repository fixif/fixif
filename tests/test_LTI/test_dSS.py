"""
This file contains tests for the dSS class and its methods
"""

from importlib.util import find_spec

import numpy as np
import pytest
from numpy.random import default_rng
from numpy.testing import assert_allclose

from fixif.func_aux.matrix import matrix
from fixif.LTI import dSS, iter_random_dSS, random_dSS

rng = default_rng()

# FIXME: move this test somewhere else...
def test_construct_sollya_slycot(capsys):
	"""simple test to check if sollya and slycot are installed"""
	# tell if sollya or slycot are disabled
	with capsys.disabled():
		print("")
		if find_spec('sollya') is not None:
			print("PythonSollya is installed")
		else:
			print("PythonSollya is not installed")
		if find_spec('slycot') is not None:
			print("Slycot is installed")
		else:
			print("Slycot is not installed")



def my_assert_allclose(A, strA: str, B, strB: str, atol=None, rtol=None):
	"""compare A and B with absolue or relative error using assert_allclose"""
	D = {}
	if atol:
		D['atol'] = atol
	if rtol:
		D['rtol'] = rtol
	try:
		assert_allclose(A, B, **D)
	except Exception as e:
		print(strA+"="+str(A))
		print(strB+"="+str(B))
		raise e


def test_construction():
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		dSS([[1, 2], [3, 4], [5, 6]], 1, 2, 3)
	with pytest.raises(ValueError):
		dSS([[1, 2], [3, 4]], 1, 2, 3)
	with pytest.raises(ValueError):
		dSS([[1, 2], [3, 4]], [[1], [2]], 2, 3)
	with pytest.raises(ValueError):
		dSS([[1, 2], [3, 4]], [[1], [2]], [[1, 2], [1, 2]], 3)


@pytest.mark.parametrize("S", iter_random_dSS(30, True, n=(2, 40), p=(2, 15), q=(2, 15)))
def test_random_dSS(S):
	"""Test random_dSS generator"""
	# test for correct sizes of random dSS
	assert S.A.nrows(),S.A.ncols() == (S.n, S.n)
	assert S.B.nrows(),S.B.ncols() == (S.n, S.q)
	assert S.C.nrows(),S.C.ncols() == (S.p, S.n)
	assert S.D.nrows(),S.D.ncols() == (S.p, S.q)

	# test for spectral radius lower than 1
	assert max(e.abs_upper() for e in S.A.eig(multiple=True)) < 1



@pytest.mark.parametrize("S", iter_random_dSS(20, stable=True, n=(2, 40), p=(2, 15), q=(2, 15)))
def test_Gramians(S):
	"""
	Test calculation of :math:`W_o` and :math:`W_c` with the two different methods
	(``linalg`` from scipy and ``slycot``from Slycot), and compare them
	"""

	for method, tolerance in [('linalg', 1e-3), ('slycot', 1e-5)]:
		dSS._W_method = method
		assert_allclose(S.A.tonumpy() @ S.Wc @ S.A.transpose().tonumpy() + (S.B * S.B.transpose()).tonumpy(), S.Wc, rtol=tolerance)
		assert_allclose(S.A.transpose().tonumpy() @ S.Wo @ S.A.tonumpy() + (S.C.transpose() * S.C).tonumpy(), S.Wo, rtol=tolerance)

		# We have to explicitely remove Wo and Wc from S so that those are calculated again
		S._Wo = None
		S._Wc = None


	# now test with non-existing method
	dSS._W_method = 'toto'
	S._Wc = None
	S._Wo = None
	with pytest.raises(ValueError):
		_ = S.Wc
	with pytest.raises(ValueError):
		_ = S.Wo

	dSS._W_method = 'slycot'


# @pytest.mark.parametrize("S", iter_random_dSS(1, True, (5, 10), (1, 5), (1, 5), pBCmask=0.1))
# def test_wcpgMP(S):
#
# 	# TODO: code WCPGmp and test it !
# 	# W = S.WCPGmp()
#
# 	# print(W)
#
# 	assert True


def calc_wcpg_approx(S, nit):
	"""Very bad WCPG approximation (we hope to get the first digits....)
	Only used to compare with true, reliable Anastasia's WCPG"""

	res = np.zeros((S.p, S.q))
	powerA = np.eye(S.n,S.n)

	for i in range(0, nit):
		res += np.absolute(S.C.tonumpy() @ powerA @ S.B.tonumpy())
		powerA = powerA @ S.A.tonumpy()

	return res + np.absolute(S.D.tonumpy())


@pytest.mark.parametrize("S", iter_random_dSS(20, True, (5, 10), (1, 5), (1, 5), pBCmask=0.1))
def test_DC_gain_and_H2_norm(S):
	"""Test DC gain calculation"""
	S.DC_gain()
	S.H2norm()
	#TODO: test if the computed value is coherent for certain simple dSS

@pytest.mark.parametrize("S", iter_random_dSS(20, True, (5, 10), (1, 5), (1, 5), pBCmask=0.1))
def test_wcpg(S):
	"""
	Test Worst Case Peak Gain calculation
	"""
	nit = 5000

	W = S.WCPG()
	wcpg = calc_wcpg_approx(S, nit)

	assert (W - matrix(wcpg)).frobenius() < 1e-5


def random_slice(p: int) -> slice:
	"""Return a random row slice with random start, stop and step.
	Args:
		p:   Number of rows in the matrix.
	Returns:
		A slice with random start, stop and step, guaranteed to select
		at least one row.
	"""
	step  = int(rng.integers(1, max(2, p)))   # step in [1, p-1]
	start = int(rng.integers(0, p))
	# stop must be strictly greater than start to select at least one element
	stop  = int(rng.integers(start + 1, p + 1))
	return slice(start, stop, step)


@pytest.mark.parametrize("S", iter_random_dSS(50, True, (5, 10), (1, 5), (1, 5)))
def test_subsystems(S):
	"""Test subsystems calculation"""
	# random slices
	i = random_slice(S.p)
	j = random_slice(S.q)

	Sub = S[i, j]
	assert Sub.A == S.A
	assert Sub.B == S.B[:, j]
	assert Sub.C == S.C[i, :]
	assert Sub.D == S.D[i, j]


@pytest.mark.parametrize("S", iter_random_dSS(20))
def test_str(S):
	"""Test string representation"""
	str(S)

@pytest.mark.parametrize("S", iter_random_dSS(20))
def test_repr(S):
	"""Test representation"""
	repr(S)

@pytest.mark.parametrize("S", iter_random_dSS(20, False, n=(5, 15), p=(1, 2), q=(1, 2)))
def test_to_dTF(S):
	"""Test transformation from dSS to dTF and dTF to dSS"""
	if S.p > 1 or S.q > 1:
		print(f"Case of {S.p} and {S.q}")
		assert True
	else:
		H = S.to_dTF()
		SS = H.to_dSS()
		S.assert_close(SS, 1e-4)


@pytest.mark.parametrize("S", iter_random_dSS(5, stable=True, n=(2, 15), p=(1, 5), q=(1, 5)))
def test_balanced(S):
	"""Test balanced realization calculation"""
	# should raise an exception if slycot is not installed
	if find_spec('slycot') is  None:
		with pytest.raises(ImportError):
			S.balanced()
	# otherwise we can compute the balanced state-space
	else:
		Sb = S.balanced()
		# check if S and Sb represent the same systems
		S.assert_close(Sb)
		# check if Sb is really balanced
		my_assert_allclose(Sb.Wo, 'Wo', Sb.Wc, 'Wc', atol=1e-3)


@pytest.mark.parametrize("S", iter_random_dSS(5, stable=True, n=(2, 15), p=(1, 5), q=(1, 5)))
def test_operations(S):
	"""Test the add, sub and mul operations"""
	# check types
	with pytest.raises(TypeError):
		S += 1
	with pytest.raises(TypeError):
		S -= 1

	T= random_dSS(n=17, p=6, q=6)
	with pytest.raises(ValueError):
		S + T
	with pytest.raises(ValueError):
		S - T


	# assert (S*2-(S+S)).H2norm() < 1e-5

	S + S
	S + random_dSS(n=rng.integers(5, 11), p=S.p, q=S.q, pRepeat=0.01, pReal=0.5, pBCmask=0.90, pDmask=0.8, pDzero=0.5)
	S - S
	random_dSS(n=rng.integers(5, 11), p=S.p, q=S.q, pRepeat=0.01, pReal=0.5, pBCmask=0.90, pDmask=0.8, pDzero=0.5) - S
	S - random_dSS(n=rng.integers(5, 11), p=S.p, q=S.q, pRepeat=0.01, pReal=0.5, pBCmask=0.90, pDmask=0.8, pDzero=0.5)
	S * random_dSS(n=rng.integers(5, 11), q=S.p, p=rng.integers(1, 6), pRepeat=0.01, pReal=0.5, pBCmask=0.90,
					pDmask=0.8, pDzero=0.5)

# TODO: add unit test for H2norm
# TODO: add unit test for DC-gain
# TODO add unit test for add, mul, sub
# TODO: add unit test for simplify

# TODO: filter `RandomFilter-12/1/1-833056621` cannot be converted in rhoDFIIt without NaN... to be investigated
