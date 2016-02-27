#coding=utf8
#!usr/bin/env python


from LTI import dSS
from SIF import SIF

from oSoP.Constant import Constant

from scipy.io import loadmat
import numpy as np
from numpy.linalg import inv

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

def WCPG_txy(S):
	#O_JM=np.bmat(np.c_[np.zeros((S.l,S.l)),S.invJ*S.M])
	#O_KJMP=np.bmat(np.c_[np.zeros((S.n,S.l)),S.K*S.invJ*S.M+S.P])
	#Ab = S.K*S.invJ*S.M+S.P
	#Bb = S.K*S.invJ*S.N+S.Q
	print S.AZ
	print S.BZ
	Cb = np.bmat(np.r_[S.invJ*S.M,S.AZ,S.CZ])
	Db = np.bmat(np.r_[S.invJ*S.N,S.BZ,S.DZ])
	print Cb
	print Db
	#print Cb
	#print Db
	#Cb = np.bmat([np.zeros((S.p,S.l)),S.L*S.invJ*S.M+S.R])
	#Db = np.bmat([S.L*S.invJ*S.N+S.S])
	SS = dSS(S.AZ,S.BZ,Cb,Db)
	return SS.WCPG()


def SIFH_to_SIFHstar(z,w):
	#SS=SIF.SIF(z)
	#print SS.CZ
	#z[2]=np.bmat(np.r_[np.identity(z[0].shape[0]),np.zeros(z[1].shape),z[2]])
	#z[7]=np.bmat(np.r_[np.zeros(z[3].shape),np.identity(z[5].shape[0]),z[7]])
	#z[8]=np.bmat(np.r_[np.zeros(z[4].shape),np.zeros(z[6].shape),z[8]])
	S = SIF(z)
	#print S.CZ
	
	if S.l !=0:
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
		IdenT=np.identity(S.l)
		N_tmp = [[S.N[i,j] for j in range(S.N.shape[1])]for i in range(S.N.shape[0])]
		N_tilde = convertToFix(N_tmp,w)
		N = np.bmat([[S.N, np.zeros((S.l,S.l+S.n+S.p))],[N_tilde-S.N, IdenT,np.zeros((S.l,S.n+S.p))]])
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
		N = np.bmat([np.zeros((0,S.q+S.n+S.p))])

	# Nouveau P
	P_tmp = [[S.P[i,j] for j in range(S.P.shape[1])]for i in range(S.P.shape[0])]
	P_tilde = convertToFix(P_tmp,w)
	P = np.bmat([[S.P,np.zeros(S.P.shape)],[P_tilde-S.P,P_tilde]])
	# Nouveau Q
	IdenX=np.identity(S.n)
	Q_tmp = [[S.Q[i,j] for j in range(S.Q.shape[1])]for i in range(S.Q.shape[0])]
	Q_tilde = convertToFix(Q_tmp,w)
	if S.l !=0:
		Q = np.bmat([[S.Q, np.zeros((S.n,S.l+S.n+S.p))],[Q_tilde-S.Q, np.zeros((S.n,S.l)), IdenX,np.zeros((S.n,S.p))]])
	else:
		Q = np.bmat([[S.Q, np.zeros((S.n,S.l+S.n+S.p))],[Q_tilde-S.Q, IdenX,np.zeros((S.n,S.p))]])
	# Nouveau R
	R_tmp = [[S.R[i,j] for j in range(S.R.shape[1])]for i in range(S.R.shape[0])]
	R_tilde = convertToFix(R_tmp,w)
	R = np.bmat([[R_tilde-S.R,R_tilde]])
	# Nouveau S
	IdenY=np.identity(S.p)
	S_tmp = [[S.S[i,j] for j in range(S.S.shape[1])]for i in range(S.S.shape[0])]
	S_tilde = convertToFix(S_tmp,w)
	S_t = np.bmat([[S_tilde-S.S, np.zeros((S.p, S.l+S.n)), IdenY]])
	
	print "\n### Z exact ###\n"
	print "Rayon spectral:"
	print max(abs(np.linalg.eig(S.AZ)[0]))
	print "\nWCPG exact : "
	print ( S.dSS.WCPG() )
	print WCPG_txy(S)
	#print S.J,S.K,S.L,S.M,S.N,S.P,S.Q,S.R,S.S
	print "\n### Z degrade ###\n"
	if S.l != 0:
		SIF_tilde = SIF((J_tilde,K_tilde,L_tilde,M_tilde,N_tilde,P_tilde,Q_tilde,R_tilde,S_tilde))
		print "Rayon spectral:"
		print max(abs(np.linalg.eig(SIF_tilde.AZ)[0]))
		print "\nWCPG arrondi : "
		print(SIF_tilde.dSS.WCPG())
		return SIF((J,K,L,M,N,P,Q,R,S_t))
	else:
		SIF_tilde = SIF((J_tilde,K_tilde,L_tilde,M_tilde,N_tilde,P_tilde,Q_tilde,R_tilde,S_tilde))
		print "Rayon spectral:"
		print max(abs(np.linalg.eig(SIF_tilde.AZ)[0]))
		print "\nWCPG arrondi : "
		print( SIF_tilde.dSS.WCPG() )
		return SIF((J,K,L,M,N,P,Q,R,S_t))
	



D=loadmat("ARITH23_BLTH_ex.mat")
for sifName in ["SIF_LWDF", "SIF_SS", "SIF_rho"]:
	print "\n\n---------------- Structure "+sifName+" ----------------\n"
	Z=[]
	for i in range(4,13):
		if D[sifName][0][0][i].dtype == np.dtype('uint8'):
			D[sifName][0][0][i].dtype = np.dtype('int8')
		Z.append(D[sifName][0][0][i])
	newSIF = SIFH_to_SIFHstar(Z, 8)
	print "\n### Z erreur ###\n"
	print "WCPG erreur : "
	print(newSIF.dSS.WCPG())
	#print newdss
	#print newdss.WCPG
