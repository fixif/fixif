#coding=utf8

"""
This file contains Direct Form I structure

"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures import Structure

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv



def makeDFI( filter, nbSum=1, transposed=True):
	"""
	Factory function to make a Direct Form I Realization

	Two options are available
	- nbSum: number of sums (1 or 2) used for the computation of the output
		nbSum=1 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in the same Sum-of-Products
		nbSum=2 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in two Sums-of-Products
	- transposed: (boolean) indicates if the realization is transposed (Direct Form I or Direct Form I transposed)

	Returns
	- a dictionary of necessary infos to build the Realization

	"""

	# convert everything to mat
	n = filter.dTF.order
	num = mat(filter.dTF.num)
	den = mat(filter.dTF.den)

	# Compute J to S matrices
	P = mat( r_[c_[ diagflat(ones((1, n-1)), -1), zeros((n, n))],c_[zeros((n, n)), diagflat(ones((1, n-1)), -1) ]] )
	Q = mat( r_[ atleast_2d(1), zeros((2*n-1, 1)) ] )
	R = mat( zeros( (1,2*n) ) )
	S = mat( atleast_2d(0) )

	if nbSum == 1:
		J = mat( atleast_2d(1) )
		K = mat( r_[ zeros( (n,1) ), atleast_2d(1), zeros( (n-1,1) ) ] )
		L = mat( atleast_2d(1) )
		M = mat( c_[ num[0,1:], -den[0,1:] ] )
		N = atleast_2d(num[0,0])

	else:
		J = mat( [[1,0],[-1,1]])
		K = c_[ zeros((2*n,1)), r_[ zeros((n,1)), atleast_2d(1), zeros((n-1, 1)) ]]
		L = mat( [[0,1]])
		M = r_[  c_[ num[0,1:], zeros((1,n))], c_[ zeros((1,n)), -den[0,1:]]  ]
		N = mat( [ [num[0,0]], [0] ])


	# transposed form
	if transposed:

		K, M = M.transpose(), K.transpose()
		P = P.transpose()
		R, Q = Q.transpose(), R.transpose()
		L, N = N.transpose(),L.transpose()
		J = J.transpose()
		S = S.transpose()       # no need to really do this, since S in scalar

		if nbSum==2:
			# we should do something to keep J lower triangular
			T = mat(rot90(eye(2)))		#l=2
			invT=inv(T)
			J = invT * J * T
			K = K * T
			L = L * T
			M = invT * M
			N = invT * N
	else:
		# transformation to 'optimize' the code, ie to make P upper triangular, so that there is no need to keep x(k+1) and x(k) in the same time in memory
		T = mat(rot90(eye(2*n)))
		invT = inv(T)

		K = invT*K
		M = M*T
		P = invT*P*T
		Q = invT*Q



	# name of the intermediate variables and states
	var_T = ('t',) if nbSum==1 else ('t_1', 't_2')
	if transposed:
		var_X = tuple( 'x_%d(k)'%i for i in range(1,n+1) )
	else:
		var_X = [ 'u(k-%d)'%i for i in range(n,0,-1) ]
		var_X.extend( 'y(k-%d)'%i for i in range(n,0,-1) )
		var_X = tuple(var_X)


	# return useful infos to build the Realization
	return { "JtoS": (J, K, L, M, N, P, Q, R, S), "varNameTX":( var_T, var_X) }



def acceptDFI(filter, **options):
	"""
	return True only if the filter is SISO
	"""
	return filter.isSISO()


# build the Direct Form I
# as an instance of the class structure
DFI = Structure( shortName='DirectForm', fullName="Direct Form I", options={ "nbSum" : (1,2), "transposed" : (False,True) }, make=makeDFI, accept=acceptDFI)