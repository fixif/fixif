#coding=utf8
#!usr/bin/env python

from SIF.SIF_tilde_error import *

from oSoP.Constant import Constant
from oSoP.oSoP_Generator import best_oSoP_gen_from_dict

from scipy.io import loadmat


from sys import path
path.append('/Users/benoitlopez/Documents/Thèse/fipogen/construct/fipogen-v1/Examples/These')
from ex_gen import *

	

options_DFI = {'wl_var':8, 'wl_cst':8, 'wl_op':16, 'formatting':False}

D=loadmat("ARITH23_BLTH_ex.mat")
for sifName in ["SIF_LWDF", "SIF_SS", "SIF_rho"]:
	print "\n\n---------------- Structure "+sifName+" ----------------\n"
	Z=[]
	for i in range(4,13):
		if D[sifName][0][0][i].dtype == np.dtype('uint8'):
			D[sifName][0][0][i].dtype = np.dtype('int8')
		Z.append(D[sifName][0][0][i])

	S = SIF(Z)
	Stilde, Serror = SIFH_to_SIFHstar(S, 8)

	print "\n### Z erreur ###\n"
	print "WCPG erreur : "
	print(Serror.dSS.WCPG())





