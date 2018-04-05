#coding: UTF8

"""
This file contains rho Direct Form II structure

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
from fixif.LTI import dSS
from numpy import mat, array_equal
from numpy import zeros,  poly, sqrt, prod, transpose, diagflat, r_, c_, ones, atleast_2d, eye
from numpy import matrix as mat
from numpy.linalg import inv
from math import floor, log


def floor2( x):
	"""
	Compute the power of two just below x
	"""
	return 2**floor(log(x,2))



def makerhoDFII(filt, gamma=None, Delta=None, transposed=True, scaling=None, equiv_dSS=False):
	"""
	Factory function to make a rho Direct Form II Realisation

		- gamma and Delta are free parameters of the rho Direct Form II (Delta can be computed if None, see 'scaling' option, Gamma is set to 1 if None)
	Options:
		- transposed: (boolean, True as default) transpose (or not) the realization: rhoDirect Form II transposed (True) or rho Direct Form II (False)
		- scaling: tell how the Delta parameters should be chosen, WHEN the Deltas are not given (equal to None)
			- None: Deltas are all equal to 1 (no scaling)
			- 'l2': a l2-scaling is applied to deduce the Deltas
			- 'l2-relaxed': a l2-relaxed scaling is applied to deduce the Deltas
		- equiv_dSS: if True returns the equivalent State-Space (instead of the Direct Form II itself)
	Returns
	- a dictionary of necessary infos to build the Realization
	"""

	# see LI04b and Hila11b for reference

	n = filt.order
	if gamma is None:
		gamma = ones( (1,n) )
	gamma = mat(gamma)


	# =====================================
	#  Step 1: build Valapha_bar, Vbeta_bar
	# by considering Delta_k = 1 for all k
	# =====================================

	# Va and Vb
	Va = transpose(filt.dTF.den)
	Vb = transpose(filt.dTF.num)

	# Build Tbar
	Tbar = mat(zeros( (n+1,n+1) ))
	Tbar[n, n] = 1
	for i in range(n-1, -1, -1):
		Tbar[i, i:n+1] = poly( gamma[0,i:n].A1 )

	# Valpha_bar, Vbeta_bar
	Valpha_bar = transpose(inv(Tbar)) * Va
	Vbeta_bar = transpose(inv(Tbar)) * Vb

	# Equivalent state space (Abar, Bbar, Cbar, Dbar)
	A0 = diagflat(mat(ones( (n-1, 1) )), 1)
	A0[:, 0] = - Valpha_bar[1:, 0]
	Abar = diagflat(gamma) + A0
	Bbar = Vbeta_bar[1:, 0] - Vbeta_bar[0, 0] * Valpha_bar[1:, 0]
	Cbar = mat(zeros((1, n)))
	Cbar[0, 0] = 1
	Dbar = Vbeta_bar[0, 0]


	# ============================================
	# Step 2: Compute Delta according to scaling
	#	(when Delta is not given)
	# ============================================

	if Delta is None:
		#We need to compute the Deltas, according to the option 'scaling'

		if scaling is None:
			Delta = ones( (1,n) )

		else:
			Wc = dSS(Abar, Bbar, Cbar, Dbar).Wc
			Delta = zeros( (1,n) )
			if scaling == 'l2':
				# compute the Deltas that perform a l2-scaling (see Li04b)
				Delta[0, 0] = sqrt( Wc[0, 0])
				for i in range(1, n):
					Delta[0, i] = sqrt(Wc[i, i] / Wc[i-1, i-1])

			elif scaling == 'l2-relaxed':
				# compute the Deltas that perform a l2-scaling (see Hila09b)
				Delta[0, 0] = floor2( sqrt (Wc[0, 0]) )
				for i in range(1, n):
					Delta[0, i] = floor2( sqrt(Wc[i, i] / Wc[i-1, i-1]) )

			else:
				raise ValueError( "rhoDFII: the `scaling` parameter should be None, 'l2' or 'l2-relaxed'")

	# ============================================
	# Step 3: Compute the coefficients (Valpha, Vbeta
	# ============================================


	# compute Valpha and Vbeta
	#  compute Tbar
	Tbar = mat(zeros( (n+1, n+1) ))
	Tbar[n, n] = 1

	for i in range( n-1, -1, -1):
		Tbar[i, i:n + 1] = poly( gamma[0, i:n].A1 ) / prod( Delta[0, i:n])

	Ka = prod(Delta[0,:])

	Valpha = transpose( inv( Ka*Tbar ) ) * Va
	Vbeta = transpose( inv( Ka*Tbar ) ) * Vb


	# ============================
	# Step 4 : build SIF
	# ============================

	if equiv_dSS:

		# Equivalent state space (A, B, C, D)
		A0 = diagflat(mat(ones( (n-1, 1) )), 1)
		A0[:, 0] = - Valpha[1:, 0]
		Arho = diagflat(gamma) + A0 * diagflat(Delta)
		Brho = Vbeta[1:, 0] - Vbeta[0, 0] * Valpha[1:, 0]
		Crho = mat(zeros((1, n)))
		Crho[0, 0] = Delta[0,0]
		Drho = mat(Vbeta[0, 0])

		J = eye((0))
		K = zeros((n, 0))
		L = zeros((1, 0))
		M = zeros((0, n))
		N = zeros((0, 1))
		P = Arho
		Q = Brho
		R = Crho
		S = Drho

		#TODO: build dJtodS matrix, according to gammaExact and DeltaExact options

	else:
		if array_equal(Delta, ones( (1,n) )):
			# specific SIF when the Delta are all equal to 1 (the temporary variables are not necessary, since t_i = x_i * Delta_i)
			J = mat(1)
			K = -Valpha[1:n+1, 0]
			L = mat(1)
			M = c_[ atleast_2d(1), zeros((1, n-1)) ]
			N = mat(Vbeta[0,0])
			P = mat(diagflat(Delta)) + mat(diagflat(ones( (1, n-1) ), 1))
			Q = Vbeta[1:n+1, 0]
			R = zeros( (1,n) )
			S = mat(0)

		else:
			J = eye(n)
			K = mat(diagflat(ones( (1, n-1) ), 1))
			K[:,0] = -Valpha[1:n+1, 0]
			L = c_[ atleast_2d(1), zeros((1, n-1)) ]
			M = mat(diagflat(Delta))
			N = r_[ atleast_2d(Vbeta[0, 0]), zeros((n-1, 1)) ]
			P = mat(diagflat(gamma))
			Q = Vbeta[1:n+1, 0]
			R = zeros( (1,n) )
			S = mat(0)

	if not transposed:
		# matrices J, K, L, M, N, P, Q, R and S were for transposed form
			K, M = M.transpose(), K.transpose()
			P = P.transpose()
			R, Q = Q.transpose(), R.transpose()
			L, N = N.transpose(), L.transpose()
			J = J.transpose()
			S = S.transpose()  # no need to really do this, since S is a scalar

	#TODO: store gamma !!
	return {"JtoS": (J,K,L,M,N,P,Q,R,S) }



def acceptrhoDFII(filter, **options):
	"""
	return True only if the filter is SISO
	"""
	return filter.isSISO() and filter.isStable()





rhoDFII = Structure( shortName="rhoDFII", fullName="rho Direct Form II", options={ 'transposed': (True, False), 'equiv_dSS':(False, True), 'scaling':(None,'l2','l2-relaxed') }, make=makerhoDFII, accept=acceptrhoDFII)