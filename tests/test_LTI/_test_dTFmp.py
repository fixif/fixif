_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2016, FiXiF Project, LIP6"
__credits__ = ["Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Anastasia Volkova"
__email__ = "Anastasia.Volkova@lip6.fr"
__status__ = "Beta"


import mpmath
import pytest
from fixif.LTI import iter_random_dTFmp, dTF


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
		dTF([1, 2, 3], [0, 6, 7])		# den[0] cannot be zero
	# with pytest.raises(ValueError):
	# 	dTF( [1, 2, 3], [1, 2] )		# num should not be longer than den


@pytest.mark.parametrize("H", iter_random_dTFmp(15))
def test_to_dSSmp(H):
	S = H.to_dSSmp()
	H2 = S.to_dTFmp(prec=100)

	my_assertAlmostEqual_matrix(H.num, H2.num)
	my_assertAlmostEqual_matrix(H.den, H2.den)





