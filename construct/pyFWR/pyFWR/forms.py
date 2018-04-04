from pyFWR import *		
import numpy as np
import dSS
from scipy.signal.filter_design import butter

def DirectFormII( num, den):
	"""create a direct form II realization"""
	
	# ceofficients' normalization
	a0 = float(den[0])
	num = [ c/a0 for c in num ]
	den = [ c/a0 for c in den ]
	n = max(len(num),len(den))
	
	J = mat([1])
	K =  np.r_[ np.mat([1]), np.zeros((n-2,1)) ]
	L = mat([num[0]])
	M = mat([ -c for c in den[1:] ])
	N = mat([1])
	P = np.diag( [1]*(n-2), -1 )
	Q = np.zeros((n-1,1))
	R = mat(num[1:])
	S = mat([0])
	
	return pyFWR( (J, K, L, M, N, P, Q, R, S), name='Direct Form II')



def directFormI(num,den):
	
	# coefficients' normalization
	a0 = float(den[0])
	num = [ c/a0 for c in num ]
	den = [ c/a0 for c in den ]
	n = max(len(num),len(den))-1
	
	#
	J = mat([1])
	K = np.r_[ np.zeros((n-1,1)), mat([1]), np.zeros((n,1)) ]
	L = mat( [1])
	M = np.c_[ mat([-c for c in den[-1:0:-1]]), mat(num[-1:0:-1]) ]
	N = mat(num[0])
	P = np.diag( [1]*(2*n-1), 1 )
	P[n-1,n] = 0
	Q = np.r_[ np.zeros((2*n-1,1)), mat([1]) ]
	R = np.zeros((1,2*n))
	S = mat([0])
	return pyFWR( (J, K, L, M, N, P, Q, R, S), name='Direct Form I')