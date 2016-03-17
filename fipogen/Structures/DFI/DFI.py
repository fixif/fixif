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


from fipogen.SIF import SIF
from fipogen.Structures import Structure

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv

class DFI(Structure):

	_name = "Direct Form I"              # name of the structure
	_possibleOptions = { "nbSum" : (1,2), "transposed" : (False,True) }       # the only option is nbSum, that can be 1 or 2
	_acceptMIMO = False

	def __init__(self, filter, nbSum=1, transposed=True):
		"""
		Two options are available

		nbSum=1 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in the same Sum-of-Products
		nbSum=2 - compute \sum b_i u(k-i) and \sum a_i y(k-i) in two Sums-of-Products

		"""

		# check the args
		self.manageOptions(nbSum=nbSum, transposed=transposed)

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
			L = mat( [[0, 1]])
			M = r_[  c_[ num[0,1:], zeros((1,n))], c_[ zeros((1,n)), -den[0,1:]]  ]
			N = mat( [ [num[0,0]], [0] ])


		# transposed form
		if transposed:
			K, M = M.transpose(), K.transpose()
			P = P.transpose()
			R, Q = Q.transpose(), R.transpose()
			L, N = N.transpose(),L.transpose()
			J = J.transpose()       # no need to really do this, since J in scalar
			S = S.transpose()       # no need to really do this, since S in scalar

		else:
			# transformation to 'optimize' the code, ie to make P upper triangular, so that there is no need to keep x(k+1) and x(k) in the same time in memory
			T = mat(rot90(eye(2*n)))
			invT = inv(T)

			K = invT*K
			M = M*T
			P = invT*P*T
			Q = invT*Q

		# name of the intermediate variables
		var_name = [ 't' ] if nbSum==1 else [ 't_1', 't_2' ]
		# states
		if transposed:
			var_name.extend( 'x_%d(k)'%i for i in range(1,n+1) )
		else:
			var_name.extend( 'u(k-%d)'%i for i in range(n,0,-1) )
			var_name.extend( 'y(k-%d)'%i for i in range(n,0,-1) )
		# output
		var_name.append( 'y(k)')

		# build SIF
		self.SIF = SIF( (J, K, L, M, N, P, Q, R, S) )
		#TODO: do something with the var_name !! (ie add it in the Structure class)

