from sys import path
path.append('../../../../fipogen2/')
path.append('../../oSoP')

import numpy as np
import LTI
import Structures
import SIF
from oSoP.Constant import Constant

from scipy.io import loadmat


def convertToFix(M,w):
	M_cst = convertToFixAux(M,w)
	M_tilde=[[M_cst[i][j] for j in range(len(M[0]))] for i in range(len(M))]
	return np.matrix(M_tilde)


def convertToFixAux(M,w):
	mM=[]
	if not isinstance(M,list) and not isinstance(M,np.matrix):
	#Si M n'est ni une liste ni un tableau numpy
		if M in [-1,0,1]:
			return M
		else:
			return Constant(M,w).approx
	else:
		for i in range(len(M)):
			mM.append(convertToFixAux(M[i],w))
	return mM


def SIFH_to_SIFHstar(z,w):
	S = SIF.SIF(z)

	# Nouveau J
	if S._l !=0:
		J_tmp = [[S.J[i,j] for j in range(S.J.shape[1])]for i in range(S.J.shape[0])]
		J_tilde = convertToFix(J_tmp,w)
		J = np.bmat([[S.J,np.zeros(S.J.shape)],[J_tilde-S.J,J_tilde]])
		# Nouveau K
		K_tmp = [[S.K[i,j] for j in range(S.K.shape[1])]for i in range(S.K.shape[0])]
		K_tilde = convertToFix(K_tmp,w)
		K = np.bmat([[S.K,np.zeros(S.K.shape)],[K_tilde-S.K,K_tilde]])
		# Nouveau L
		L_tmp = [[S.L[i,j] for j in range(S.L.shape[1])]for i in range(S.L.shape[0])]
		L_tilde = convertToFix(L_tmp,w)
		L = np.bmat([[L_tilde-S.L,L_tilde]])
		# Nouveau M
		M_tmp = [[S.M[i,j] for j in range(S.M.shape[1])]for i in range(S.M.shape[0])]
		M_tilde = convertToFix(M_tmp,w)
		M = np.bmat([[S.M,np.zeros(S.M.shape)],[M_tilde-S.M,M_tilde]])
		# Nouveau N
		IdenT=np.identity(S._l)
		N_tmp = [[S.N[i,j] for j in range(S.N.shape[1])]for i in range(S.N.shape[0])]
		N_tilde = convertToFix(N_tmp,w)
		N = np.bmat([[S.N, np.zeros((S._l,S._l+S._n+S._p))],[N_tilde-S.N, IdenT,np.zeros((S._l,S._n+S._p))]])
	else:
		J_tilde = S.J
		J = S.J
		K_tilde = S.K
		K = np.bmat([[S.K],[S.K]])
		L_tilde = S.L
		L = S.L
		M_tilde = S.M
		M = np.bmat([[S.M,S.M]])
		N_tilde = S.N
		N = np.bmat([np.zeros((0,S._m+S._n+S._p))])

	# Nouveau P
	P_tmp = [[S.P[i,j] for j in range(S.P.shape[1])]for i in range(S.P.shape[0])]
	P_tilde = convertToFix(P_tmp,w)
	P = np.bmat([[S.P,np.zeros(S.P.shape)],[P_tilde-S.P,P_tilde]])
	# Nouveau Q
	IdenX=np.identity(S._n)
	Q_tmp = [[S.Q[i,j] for j in range(S.Q.shape[1])]for i in range(S.Q.shape[0])]
	Q_tilde = convertToFix(Q_tmp,w)
	if S._l !=0:
		Q = np.bmat([[S.Q, np.zeros((S._n,S._l+S._n+S._p))],[Q_tilde-S.Q, np.zeros((S._n,S._l)), IdenX,np.zeros((S._n,S._p))]])
	else:
		Q = np.bmat([[S.Q, np.zeros((S._n,S._l+S._n+S._p))],[Q_tilde-S.Q, IdenX,np.zeros((S._n,S._p))]])
	# Nouveau R
	R_tmp = [[S.R[i,j] for j in range(S.R.shape[1])]for i in range(S.R.shape[0])]
	R_tilde = convertToFix(R_tmp,w)
	R = np.bmat([[R_tilde-S.R,R_tilde]])
	# Nouveau S
	IdenY=np.identity(S._p)
	S_tmp = [[S.S[i,j] for j in range(S.S.shape[1])]for i in range(S.S.shape[0])]
	S_tilde = convertToFix(S_tmp,w)
	S_t = np.bmat([[S_tilde-S.S, np.zeros((S._p, S._l+S._n)), IdenY]])
	
	print "\n### Z exact ###\n"
	print "WCPG exact : "
	print(LTI.dSS(S._AZ,S._BZ,S._CZ,S._DZ).WCPG)
	#print S.J,S.K,S.L,S.M,S.N,S.P,S.Q,S.R,S.S
	print "\n### Z degrade ###\n"
	if S._l != 0:
		SIF_tilde =SIF.SIF((J_tilde,K_tilde,L_tilde,M_tilde,N_tilde,P_tilde,Q_tilde,R_tilde,S_tilde))
		print "WCPG arrondi : "
		print(LTI.dSS(SIF_tilde._AZ,SIF_tilde._BZ,SIF_tilde._CZ,SIF_tilde._DZ).WCPG)
		return SIF.SIF((J,K,L,M,N,P,Q,R,S_t))
	else:
		SIF_tilde =SIF.SIF((J_tilde,K_tilde,L_tilde,M_tilde,N_tilde,P_tilde,Q_tilde,R_tilde,S_tilde))
		print "WCPG arrondi : "
		print(LTI.dSS(SIF_tilde._AZ,SIF_tilde._BZ,SIF_tilde._CZ,SIF_tilde._DZ).WCPG)
		return SIF.SIF((J,K,L,M,N,P,Q,R,S_t))
	



D=loadmat("Examples_Florent")
for sifName in ["SIF_DFI", "SIF_LWDF", "SIF_SS", "SIF_rho"]:
	print "\n\n---------------- Structure "+sifName+" ----------------\n\n"
	Z_DFI=[D[sifName][0][0][i] for i in range(4,13)]
	newSIF = SIFH_to_SIFHstar(Z_DFI, 8)
	print "\n### Z erreur ###\n"
	print "WCPG erreur : "
	print(LTI.dSS(newSIF._AZ,newSIF._BZ,newSIF._CZ,newSIF._DZ).WCPG)
	#print newdss
	#print newdss.WCPG
