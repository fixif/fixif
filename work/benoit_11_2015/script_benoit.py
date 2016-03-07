#coding=utf8
#!usr/bin/env python

from SIF.SIF_tilde_error import *

from oSoP.Constant import Constant
from oSoP.oSoP_Generator import best_oSoP_gen_from_dict

from scipy.io import loadmat


D=loadmat("ARITH23_BLTH_ex.mat")
for sifName in ["SIF_LWDF", "SIF_SS", "SIF_rho", "SIF_DFI"]:
	print "\n\n---------------- Structure "+sifName+" ----------------\n"
	Z=[]
	for i in range(4,13):
		if D[sifName][0][0][i].dtype == np.dtype('uint8'):
			D[sifName][0][0][i].dtype = np.dtype('int8')
		Z.append(D[sifName][0][0][i])

	S = SIF(Z)
	Stilde, Serror = SIFH_to_SIFHstar(S, 8, True)


	print "\n### Z erreur ###\n"
	print "WCPG erreur : "
	print(Serror.dSS.WCPG())





