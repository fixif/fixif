# coding: utf8

"""
This file contains Direct Form I structure

"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from fixif.Structures.Structure import Structure
from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv


def makeDFI(filt, nbSum=1, transposed=True):
	"""
	Factory function to make a Direct Form I Realization

	Two options are available
	- nbSum: number of sums (1 or 2) used for the computation of the output
		nbSum==1 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in the same Sum-of-Products
		nbSum==2 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in two Sums-of-Products
	- transposed: (boolean) indicates if the realization is transposed (Direct Form I or Direct Form I transposed)

	Returns
	- a dictionary of necessary infos to build the Realization

	"""
	if nbSum != 1 and nbSum != 2:
		raise ValueError("DFI: nbSum should be equal to 1 or 2")

	# convert everything to mat
	n = filt.dTF.order
	num = mat(filt.dTF.num)
	den = mat(filt.dTF.den)

	# Compute J to S matrices
	P = mat(r_[c_[diagflat(ones((1, n - 1)), -1), zeros((n, n))], c_[zeros((n, n)), diagflat(ones((1, n - 1)), -1)]])
	Q = mat(r_[atleast_2d(1), zeros((2 * n - 1, 1))])
	R = mat(zeros((1, 2 * n)))
	S = mat(atleast_2d(0))

	if nbSum == 1:
		J = mat(atleast_2d(1))
		K = mat(r_[zeros((n, 1)), atleast_2d(1), zeros((n - 1, 1))])
		L = mat(atleast_2d(1))
		M = mat(c_[num[0, 1:], -den[0, 1:]])
		N = atleast_2d(num[0, 0])

	else:
		J = mat([[1, 0], [-1, 1]])
		K = c_[zeros((2 * n, 1)), r_[zeros((n, 1)), atleast_2d(1), zeros((n - 1, 1))]]
		L = mat([[0, 1]])
		M = r_[c_[num[0, 1:], zeros((1, n))], c_[zeros((1, n)), -den[0, 1:]]]
		N = mat([[num[0, 0]], [0]])

	# transposed form
	if transposed:

		K, M = M.transpose(), K.transpose()
		P = P.transpose()
		R, Q = Q.transpose(), R.transpose()
		L, N = N.transpose(), L.transpose()
		J = J.transpose()
		S = S.transpose()  # no need to really do this, since S in scalar

		if nbSum == 2:
			# we should do something to keep J lower triangular
			T = mat(rot90(eye(2)))  # l=2
			invT = inv(T)
			J = invT * J * T
			K = K * T
			L = L * T
			M = invT * M
			N = invT * N
	else:
		# transformation to 'optimize' the code, ie to make P upper triangular, so that there is no need to keep x(k+1) and x(k) in the same time in memory
		T = mat(rot90(eye(2 * n)))
		invT = inv(T)

		K = invT * K
		M = M * T
		P = invT * P * T
		Q = invT * Q

	# name of the intermediate variables and states (when non transposed form)
	var_X = [('y', None, -i) for i in range(n, 0, -1)]		# x_i(k) := y(k-i)
	var_X.extend([('u', None, -i) for i in range(n, 0, -1)])		# x_{i+n}(k) := u(k-i)

	# return useful infos to build the Realization
	return {"JtoS": (J, K, L, M, N, P, Q, R, S), "surnameVarX": None if transposed else var_X}


def acceptDFI(filt, **options):
	"""
	return True only if the filter is SISO
	"""
	return filt.isSISO()


# build the Direct Form I
# as an instance of the class structure
DFI = Structure(shortName='DFI', fullName="Direct Form I", options={"nbSum": (1, 2), "transposed": (False, True)}, make=makeDFI, accept=acceptDFI)

# TODO: nbSum=3 and transposed=True is the same as nbSum=1 and transposed=True (just an extra useless temporary variable (t_2=t_1))

