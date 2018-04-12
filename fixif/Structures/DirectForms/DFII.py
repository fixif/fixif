#coding: utf8

"""
This file contains Direct Form II structure

"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures.Structure import Structure

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d, fliplr
from numpy.linalg import inv


def makeDFII(filt, transposed=True):
	"""
	Factory function to make a Direct Form II Realization

	One option:
	- transposed: (boolean) indicates if the realization is transposed (Direct Form II or Direct Form II transposed)

	Returns
	- a dictionary of necessary infos to build the Realization
	"""

	# convert everything to mat
	n = filt.dTF.order
	num = mat(filt.dTF.num)
	den = mat(filt.dTF.den)

	# Compute J to S matrices
	J = mat( atleast_2d(1) )
	K = mat( r_[ zeros( (n-1,1) ), atleast_2d(1) ] )
	L = mat( atleast_2d(num[0,0]) )
	M = mat( fliplr(-den[0,1:]) )
	N = mat( atleast_2d(1) )
	P = mat( diagflat(ones((1, n-1)), 1) )
	Q = mat( zeros( (n, 1) )  )
	R = mat( fliplr(num[0,1:]) )
	S = mat( atleast_2d(0) )


	# transposed form
	if transposed:
		K, M = M.transpose(), K.transpose()
		P = P.transpose()
		R, Q = Q.transpose(), R.transpose()
		L, N = N.transpose(),L.transpose()
		J = J.transpose()       # no need to really do this, since J in scalar
		S = S.transpose()       # no need to really do this, since S in scalar

		# transformation to 'optimize' the code, ie to make P upper triangular, so that there is no need to keep x(k+1) and x(k) in the same time in memory
		T = mat(rot90(eye(n)))
		invT = inv(T)

		K = invT*K
		M = M*T
		P = invT*P*T
		Q = invT*Q

	# name of the intermediate variables and states
	if transposed:
		varName = [ ('t',), tuple( 'x_%d(k)'%i for i in range(1,n+1) ) ]
	else:
		varName = [ ('t',), tuple( 'v(k-%d)'%i for i in range(n,0,-1) ) ]


	# return useful infos to build the Realization
	return { "JtoS": (J, K, L, M, N, P, Q, R, S), "varNameTX" : varName }



def acceptDFII(filter, **options):
	"""
	return True only if the filter is SISO
	"""
	return filter.isSISO()



# build the Direct Form II
# as an instance of the class structure
DFII = Structure( shortName='DFII', fullName="Direct Form II", options={"transposed": (False, True)}, make=makeDFII, accept=acceptDFII)
