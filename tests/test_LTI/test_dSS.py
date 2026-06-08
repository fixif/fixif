"""
This file contains tests for the dSS class and its methods
"""

from importlib.util import find_spec

import pytest
from numpy import absolute, all, array, eye, zeros
from numpy import matrix as mat
from numpy.linalg import eigvals, norm
from numpy.random import randint
from numpy.testing import assert_allclose

from fixif.LTI import dSS, iter_random_dSS


# FIXME: move this test somewhere else...
def test_construct_sollya_slycot(capsys):
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


# def my_assert_allclose_TFmp(H, b, a, tol):
#
# 	if max(H.num.shape) != b.rows or max(H.den.shape) != a.rows:
# 		raise ValueError('MP Transfer function is not the same size as the scipy transfer function!')
#
# 	for i in range(0, b.rows):
# 		if mpmath.fabs(b[i, 0] - H.num[0, i]) < tol:
# 			assert True
# 		else:
# 			raise ValueError("MP transfer function is not close to the dTF")
#
# 	for i in range(0, a.rows):
# 		if mpmath.fabs(a[i, 0] - H.den[0, i]) < tol:
# 			assert True
# 		else:
# 			raise ValueError("MP transfer function is not close to the dTF")


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
	# test for correct sizes of random dSS
	assert S.A.shape == (S.n, S.n)
	assert S.B.shape == (S.n, S.q)
	assert S.C.shape == (S.p, S.n)
	assert S.D.shape == (S.p, S.q)

	# test for spectral radius lower than 1
	assert max(abs(eigvals(S.A))) < 1



@pytest.mark.parametrize("S", iter_random_dSS(20, stable=True, n=(2, 40), p=(2, 15), q=(2, 15)))
def test_Gramians(S):
	"""
	Test calculation of :math:`W_o` and :math:`W_c` with the two different methods
	(``linalg`` from scipy and ``slycot``from Slycot), and compare them
	"""

	for method, tolerance in [('linalg', 1e-3), ('slycot', 1e-5)]:
		dSS._W_method = method
		assert_allclose(array(S.A * S.Wc * S.A.transpose() + S.B * S.B.transpose()), array(S.Wc), rtol=tolerance)
		assert_allclose(array(S.A.transpose() * S.Wo * S.A + S.C.transpose() * S.C), array(S.Wo), rtol=tolerance)

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

	res = mat(zeros((S.p, S.q)))
	powerA = mat(eye(S.n, S.n))

	for i in range(0, nit):
		res += absolute(S.C * powerA * S.B)
		powerA = powerA * S.A

	return res + absolute(S.D)


@pytest.mark.parametrize("S", iter_random_dSS(20, True, (5, 10), (1, 5), (1, 5), pBCmask=0.1))
def test_wcpg(S):

	"""
	Test Worst Case Peak Gain calculation
	"""
	nit = 5000

	W = S.WCPG()
	wcpg = calc_wcpg_approx(S, nit)

	assert norm(array(W) - array(wcpg)) < 1e-2


@pytest.mark.parametrize("S", iter_random_dSS(50, True, (5, 10), (1, 5), (1, 5)))
def test_subsystems(S):

	# random slices
	beg_i = randint(0, S.p)
	end_i = randint(beg_i, S.p)
	step_i = randint(1, 3)
	i = slice(beg_i, end_i, step_i)

	beg_j = randint(0, S.q)
	end_j = randint(beg_j, S.q)
	step_j = randint(1, 3)
	j = slice(beg_j, end_j, step_j)

	Sub = S[i, j]
	assert all(Sub.A == S.A)
	assert all(Sub.B == S.B[:, j])
	assert all(Sub.C == S.C[i, :])
	assert all(Sub.D == S.D[i, j])


@pytest.mark.parametrize("S", iter_random_dSS(20))
def test_str(S):
	str(S)

@pytest.mark.parametrize("S", iter_random_dSS(20))
def test_repr(S):
	repr(S)

@pytest.mark.parametrize("S", iter_random_dSS(20, False, n=(5, 15), p=(1, 2), q=(1, 2)))
def test_to_dTF(S):
	if S.p > 1 or S.q > 1:
		print(f"Case of {S.p} and {S.q}")
		assert True
	else:
		H = S.to_dTF()
		SS = H.to_dSS()
		S.assert_close(SS, 1e-4)


@pytest.mark.parametrize("S", iter_random_dSS(5, stable=True, n=(2, 15), p=(1, 5), q=(1, 5)))
def test_balanced(S):
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


# TODO: still need to test:
# H2norm
# DC-gain
# add, mul, sub
# simplify

# TODO: filter `RandomFilter-12/1/1-833056621` cannot be converted in rhoDFIIt without NaN... to be investigated
