#coding=utf8
#!usr/bin/env python

__author__ = "Benoit Lopez, Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Benoit Lopez", "Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.LTI import dSS
from fixif.SIF import SIF

from fixif.FxP.Constant import Constant
import numpy as np

def convertToFix(M,w):
	if 0 in M.shape:
		return np.zeros(M.shape)
	M_tmp = [[M[i,j] for j in range(M.shape[1])]for i in range(M.shape[0])]
	M_cst = convertToFixAux(M_tmp,w)
	M_tilde=np.matrix([[M_cst[i][j] for j in range(len(M_tmp[0]))] for i in range(len(M_tmp))])
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

def WCPG_txy(S):
	N1 = np.bmat(np.r_[S.invJ*S.M,S.AZ,S.CZ])
	N2 = np.bmat(np.r_[S.invJ*S.N,S.BZ,S.DZ])
	SS = dSS(S.AZ,S.BZ,N1,N2)
	return SS.WCPG()


def SIFH_to_SIFHstar(S,w, prints = False):
	# Construit S_tilde et S_tilde_eps à partir de S
	# Nouveau J
	J_tilde = convertToFix(S.J,w)
	J = np.bmat([[S.J,np.zeros(S.J.shape)],[J_tilde-S.J,J_tilde]])
	# Nouveau K
	K_tilde = convertToFix(S.K,w)
	K = np.bmat([[S.K,np.zeros(S.K.shape)],[K_tilde-S.K,K_tilde]])
	# Nouveau L
	L_tilde = convertToFix(S.L,w)
	L = np.bmat([[L_tilde-S.L,L_tilde]])
	# Nouveau M
	M_tilde = convertToFix(S.M,w)
	M = np.bmat([[S.M,np.zeros(S.M.shape)],[M_tilde-S.M,M_tilde]])
	# Nouveau N
	IdenT=np.identity(S.l)
	N_tilde = convertToFix(S.N,w) 
	N = np.bmat([[S.N, np.zeros((S.l,S.l+S.n+S.p))],[N_tilde-S.N, IdenT,np.zeros((S.l,S.n+S.p))]])
	# Nouveau P
	P_tilde = convertToFix(S.P,w)
	P = np.bmat([[S.P,np.zeros(S.P.shape)],[P_tilde-S.P,P_tilde]])
	# Nouveau Q
	IdenX=np.identity(S.n)
	Q_tilde = convertToFix(S.Q,w)
	Q = np.bmat([[S.Q, np.zeros((S.n,S.l+S.n+S.p))],[Q_tilde-S.Q, np.zeros((S.n,S.l)), IdenX,np.zeros((S.n,S.p))]])
	# Nouveau R
	R_tilde = convertToFix(S.R,w)
	R = np.bmat([[R_tilde-S.R,R_tilde]])
	# Nouveau S
	IdenY=np.identity(S.p)
	S_tilde = convertToFix(S.S,w)
	S_t = np.bmat([[S_tilde-S.S, np.zeros((S.p, S.l+S.n)), IdenY]])
	
	if prints:
		print("\n### Z exact ###")
		print("\nWCPG : \n - Wy :")
		print ( S.dSS.WCPG() )
		print("\n - Wtxy :")
		print(WCPG_txy(S))
		print("\n### Z degrade ###\n\nWCPG : \n - Wy :")
	SIF_tilde = SIF((J_tilde,K_tilde,L_tilde,M_tilde,N_tilde,P_tilde,Q_tilde,R_tilde,S_tilde))
	if prints:
		print(SIF_tilde.dSS.WCPG())
		print("\n - Wtxy :")
		print(WCPG_txy(SIF_tilde))
	SIF_err = SIF((J,K,L,M,N,P,Q,R,S_t))
	return SIF_tilde, SIF_err


