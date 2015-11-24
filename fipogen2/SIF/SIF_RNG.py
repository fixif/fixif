#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply, all, diag, trace
from numpy import transpose
from numpy.linalg import norm, inv, eig

__all__ = ['RNG']

def RNG(R, tol=1.e-8):
	
	def computeWeight(X, tol):
		
		W = ones(X.shape)
		
		rows, cols = where(abs(X) < tol | abs(X-1) < tol | abs(X+1) < tol)
		
		for row, col in zip(rows, cols):
		    W[row, col] = 0
		    
		rows, cols = where(abs(W) > tol)
		
		#WORK_MARKER
		for row, col in zip(rows, cols):
			if :
		
		
		
		return W
	
	invJ = inv(R.J)
	
	M1 = c_[R.K*invJ, eye(R.n), zeros((R.n, R.m))]
	M2 = c_[R.L*invJ, zeros((R.p, R.n)), eye(R.p)]
	
	W01Z = computeWeight(R.Z, tol)
	dZ = diag( W01Z*ones(R.l+R.n+R.m, 1) )
	
	G = trace( dZ * ( M2.transpose()*M2 + M1.transpose()*R.Wo*M1 ) )
	
	return G, dZ
	
	