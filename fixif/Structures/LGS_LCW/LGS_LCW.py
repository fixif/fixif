#coding=utf8

"""
This file contains LGS and LCW structures

"""

__author__ = "Benoit Lopez, Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Benoit Lopez", "Thibault Hilaire" ]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures import Structure
from fixif.LTI import Filter

import numpy as np
import scipy as sp
import random as rd
from numpy import linalg as la
from numpy.linalg import inv  # Calcule l'inverse d'une matrice
from numpy import eye
from math import sqrt  # Racine carrée
from scipy import signal
from scipy.io import savemat, loadmat

np.set_printoptions(suppress=True)


def PhiKLD(s):
	"""Returns the (Phi,K,L,D) matrices from a dSS
	"""
	I = eye(s.A.shape[0])
	IAinv = inv(s.A + I)
	Phi = IAinv * (s.A - I)
	K = sqrt(2) * IAinv * s.B
	L = sqrt(2) * s.C * IAinv
	D = s.D - s.C * IAinv * s.B
	return (Phi, K, L, D)


def PhiKLD_in(alpha, Phi, K, L, D):
	"""Construit Phi_in et K_in à partir des alphas en utilisant la formule
	et L_in en utilisant la transformation pour passer de (Phi,K,L,D)
	à (Phi_in,K_in,L_in,D)"""
	n = Phi.shape[0]
	I = np.eye(n)
	# On construit la matrice Phi_in
	Phi_in = np.zeros([n, n])
	for i in range(1, n - 1):
		Phi_in[i][i + 1] = alpha[i]
		Phi_in[i][i - 1] = -alpha[i - 1]
	Phi_in[0][1] = alpha[0]
	Phi_in[n - 1][n - 2] = -alpha[n - 2]
	Phi_in[n - 1][n - 1] = -alpha[n - 1]
	Phi_in = np.matrix(Phi_in)

	# Le vecteur K_in
	K_in = np.zeros([n, 1])
	K_in[n - 1] = sqrt(2 * alpha[n - 1])
	K_in = np.matrix(K_in)
	(uu, V_in) = la.eig(Phi_in)
	S = []
	for i in range(0, n):
		c = complex(rd.uniform(0., 1.), rd.uniform(0., 1.))
		while (c in S) or (c in uu):
			c = complex(rd.uniform(0., 1.), rd.uniform(0., 1.))
		S.append(c)
		if i == 0:
			B = np.matrix(inv(c * I - Phi_in) * K_in)
			A = np.matrix(L * inv(c * I - Phi) * K)
		else:
			b = np.matrix(inv(c * I - Phi_in) * K_in)
			B = np.c_[B, b]
			a = np.matrix(L * inv(c * I - Phi) * K)
			A = np.c_[A, a]
	LL = A * inv(B)
	L_in = []
	for i in range(LL.size):
		L_in.append(LL.item(i).real)
	L_in = np.matrix(L_in)
	return (Phi_in, K_in, L_in, D)


def ABCd_in(Phi, K, L, D):
	"""On applique la bonne formule pour passer de (Phi_in,K_in,L_in,D)
	à (A_in,B_in,C_in,d)"""
	I = np.eye(Phi.shape[0])
	A = (I + Phi) * inv(I - Phi)
	B = sqrt(2) / 2 * (I + A) * K
	C = sqrt(2) / 2 * L * (I + A)
	d = D + C * inv(I + A) * B
	return (A, B, C, d)


def ABCd_star(A, B, C, d, Phi, K):
	I = np.eye(Phi.shape[0])
	As = np.transpose(A)
	Bs = np.transpose(inv(I - Phi)) * np.transpose(C)
	Cs = sqrt(2) * np.transpose(K)
	return (As, Bs, Cs, d)


def A_decomposition_LGS(alpha, Phi_in):
	"""Retourne la décomposition de A_in en produit de
	1+3*(n-1) matrices"""
	n = Phi_in.shape[0]
	Ad = []
	# On calcule d'abord tous les beta_i et gamma_i
	beta = [-alpha[0]]
	gamma = [1 / (1 + alpha[0] ** 2)]
	for i in range(1, n - 1):
		beta.append(-alpha[i] / (1 - alpha[i - 1] * beta[i - 1]))
		if (i < n - 2):
			gamma.append(1 / (1 - alpha[i] * beta[i]))
	beta.append(-alpha[n - 1] / (1 + alpha[n - 1] - alpha[n - 2] * beta[n - 2]))
	gamma.append(1 / (1 + alpha[n - 1] - alpha[n - 2] * beta[n - 2]))
	# Puis on ajoute dans la liste de la décomposition les matrices U selon la formule.
	for i in range(0, n - 1):
		Ad.append(U(i + 1, i, -alpha[i], n))
		Ad.append(U(i + 1, i + 1, gamma[i], n))
	for i in range(0, n - 1):
		Ad.append(U(n - 2 - i, n - 1 - i, -beta[n - 2 - i], n))
	# A la fin on rajoute  la matrice (I+Phi_in)
	Ad.append(np.eye(n) + Phi_in)
	return Ad


def A_decomposition_LCW(alpha, Phi_in):
	"""Retourne la décomposition de A_in en produit de
	3*(n-1) matrices"""
	n = Phi_in.shape[0]
	Ad = []
	# On calcule d'abord tous les beta_i et gamma_i
	beta = [-alpha[0]]
	gamma = [1 / (1 + alpha[0] ** 2)]
	for i in range(1, n - 1):
		beta.append(-alpha[i] / (1 - alpha[i - 1] * beta[i - 1]))
		if (i < n - 2):
			gamma.append(1 / (1 - alpha[i] * beta[i]))
	beta.append(-alpha[n - 1] / (1 + alpha[n - 1] - alpha[n - 2] * beta[n - 2]))
	gamma.append(1 / (1 + alpha[n - 1] - alpha[n - 2] * beta[n - 2]))
	# Puis on ajoute dans la liste de la décomposition les matrices U selon la formule.
	for i in range(0, n - 1):
		Ad.append(U(i + 1, i, alpha[i], n))
		Ad.append(U(i + 1, i + 1, gamma[i], n))
	for i in range(0, n - 1):
		Ad.append(U(n - 2 - i, n - 1 - i, beta[n - 2 - i], n))
	return Ad


def Matrice_JtoS_LGS(Ad, A_in, B_in, C_in, d):
	"""A partir de la décomposition de A_in et des matrices B_in,C_in,D,
	construit les éléments (J,K,L,M,N,P,Q,R,S) qui forment Z."""
	n = Ad[0].shape[0]
	nn = len(Ad)
	I = np.matrix(np.eye(n))
	Ze = np.matrix(np.zeros([n, n]))
	J = []
	C = []  # va stocker la colonne courante de J dans la boucle
	# la boucle suivante construit les colones N x n de la matrice J et les concatène.
	for i in range(1, nn + 1):
		if i == 1:
			C = np.r_[I, -Ad[i]]
			while len(C) < n * nn:
				C = np.r_[C, Ze]
			J = C
		else:
			C = Ze
			while len(C) < n * (i - 1):
				C = np.r_[C, Ze]
			C = np.r_[C, I]
			if i != nn:
				C = np.r_[C, -Ad[i]]
			while len(C) < n * nn:
				C = np.r_[C, Ze]
			J = np.c_[J, C]
	J = np.matrix(J)
	K = Ze
	for i in range(0, nn - 2):
		K = np.c_[K, Ze]
	K = np.c_[K, I]
	L = np.matrix(np.zeros([1, n * nn]))
	N = np.matrix(np.zeros([n * nn, 1]))
	M = Ad[0]
	for i in range(0, nn - 1):
		M = np.r_[M, Ze]
	P = Ze
	Q = B_in
	R = C_in
	S = d


	return J, K, L, M, N, P, Q, R, S


def Matrice_JtoS_LCW(Ad, As, Bs, Cs, d):
	"""A partir de la décomposition de A_in et des matrices B_in,C_in,D,
	construit les éléments (J,K,L,M,N,P,Q,R,S) qui forment Z."""
	n = Ad[0].shape[0]
	nn = len(Ad)
	I = np.matrix(np.eye(n))
	Ze = np.matrix(np.zeros([n, n]))
	J = []
	C = []
	# la boucle suivante construit les colones N x n de la matrice J et les concatène.
	for i in range(1, nn + 1):
		if i == 1:
			C = np.r_[I, -Ad[i]]
			while len(C) < n * nn:
				C = np.r_[C, Ze]
			J = C
		else:
			C = Ze
			while len(C) < n * (i - 1):
				C = np.r_[C, Ze]
			C = np.r_[C, I]
			if i != nn:
				C = np.r_[C, -Ad[i]]
			while len(C) < n * nn:
				C = np.r_[C, Ze]
			J = np.c_[J, C]
	J = np.matrix(J)
	K = Ze
	for i in range(0, nn - 2):
		K = np.c_[K, Ze]
	K = np.c_[K, I]
	L = np.matrix(np.zeros([1, n * nn]))
	N = np.matrix(np.zeros([n * nn, 1]))
	M = 2 * Ad[0]
	for i in range(0, nn - 1):
		M = np.r_[M, Ze]
	P = -I
	Q = Bs
	R = Cs
	S = d
	return (J, K, L, M, N, P, Q, R, S)


def U(i, j, x, n):
	"""Construit la matrice U(i,j,x) de taille n telle que
	U est la matric identité et
	le j-ème élément de la i-ème ligne vaut x."""
	U = np.eye(n)
	U[i][j] = x
	U = np.matrix(U)
	return U


def JSS_trans(D):
	"""Calcul la décomposition en fraction continue"""
	D=list(D.flat)#TODO:ugly!!
	n = len(D)
	Ol = []
	El = []
	for i in range(0, n):
		if i % 2 == 0:
			Ol.append(D[i])
			El.append(0.0)
		else:
			El.append(D[i])
			Ol.append(0.0)
	O = np.poly1d(Ol)  # Polynôme des monômes pair
	E = np.poly1d(El)  # Polynôme des monômes impair
	r = []
	j = len(D)
	while j > 1:
		if len(O) > len(E):
			LMo = []
			Ro = []
			for i in range(0, len(O) + 1):
				if i < len(O):
					Ro.append(O[i])
					LMo.append(0.0)
				else:
					LMo.append(O[i])
			LMo.reverse()
			LMo = np.poly1d(LMo)
			Ro.reverse()
			Ro = np.poly1d(Ro)
			(Q, R) = np.polydiv(LMo, E)
			r.append(Q[1])
			O = Ro + R
		else:
			LMe = []
			Re = []
			for i in range(0, len(E) + 1):
				if i < len(E):
					Re.append(E[i])
					LMe.append(0.0)
				else:
					LMe.append(E[i])
			LMe.reverse()
			LMe = np.poly1d(LMe)
			Re.reverse()
			Re = np.poly1d(Re)
			(Q, R) = np.polydiv(LMe, O)
			r.append(Q[1])
			E = Re + R
		j -= 1
	r.reverse()
	# On trouve les alpha à partir des r en utilisant la formule
	alpha = []
	for i in range(0, len(r) - 1):
		alpha.append(sqrt(1.0 / (r[i] * r[i + 1])))
	alpha.append(1.0 / (r[-1]))
	# On retourne les alpha qui serviront à construire Phi_in et K_in
	return alpha


def makeLGS(filt, transposed=False):
	"""
	Factory function to make a LGS Realization

	Option
	- transposed: (boolean) indicates if the realization is transposed

	Returns
	- a dictionary of necessary infos to build the Realization
	"""

	# We compute (Phi,K,L,D) from the initial state-space
	(Phi, K, L, D) = PhiKLD(filt.dSS)
	num, den = signal.ss2tf(Phi, K, L, D)

	# We compute alphas with JSS-transformation
	alpha = JSS_trans(den)

	# We compute the PhiKLD_in
	(Phi_in, K_in, L_in, D) = PhiKLD_in(alpha, Phi, K, L, D)

	# We can compute the (A_in, B_in, C_in, d) abd tge A_in decomposition
	(A_in, B_in, C_in, d) = ABCd_in(Phi_in, K_in, L_in, D)

	Ad = A_decomposition_LGS(alpha, Phi_in)

	# Then, we deduce J to S matrices
	JtoS = Matrice_JtoS_LGS(Ad, A_in, B_in, C_in, d)

	#TODO: use transposed ???

	# return useful infos to build the Realization
	return { "JtoS": JtoS }



def makeLCW(filt, transposed=False):
	"""Retourne la forme SIF de la structure LCW correspondant au filtre donné"""
	# Par la fonction de scipy.signal on obtient le state-space associé
	# On calcule ensuite (Phi,K,L,D) qu'on reconverti en fonction de transfert
	(Phi, K, L, D) = PhiKLD(filt.dSS)
	num, den = signal.ss2tf(Phi, K, L, D)
	# On calcule les alpha par la JSS-transformation
	alpha = JSS_trans(den)
	# On calcule les PhiKLD_in
	(Phi_in, K_in, L_in, D) = PhiKLD_in(alpha, Phi, K, L, D)
	# On peut calculer les (A,B,C,d)_in et la
	# décomposition de A_in en produit de matrice.
	(A_ib, B_ib, C_ib, d) = ABCd_in(Phi_in, K_in, L_in, D)
	(As, Bs, Cs, d) = ABCd_star(A_ib, B_ib, C_ib, d, Phi_in, K_in)
	Ad = A_decomposition_LCW(alpha, Phi_in)
	# On construit les matrices qui forment Z
	JtoS = Matrice_JtoS_LCW(Ad, As, Bs, Cs, d)
	#TODO: use transposed ???

	# return useful infos to build the Realization
	return { "JtoS": JtoS }



def acceptLGSLCW(filt, **options):
	"""
	return True only if the filter is SISO
	"""
	return filt.isSISO() and filt.isStable()


# build the Direct Form I
# as an instance of the class structure
LGS = Structure( shortName='LGS', fullName="Li-Gevers-Sun", options={ "transposed" : (False,True) }, make=makeLGS, accept=acceptLGSLCW)
LCW = Structure( shortName='LCW', fullName="Li-Chu-Wu", options={ "transposed" : (False,True) }, make=makeLCW, accept=acceptLGSLCW)

#TODO: relire, recommenter en anglais, virer les listes (et mettre du numpy matrix à la place), etc.
#TODO: et bien sûr, passer en multiprécision (et un jour savoir quelle précision est suffisante...)