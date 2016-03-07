#coding=utf8
#!usr/bin/env python

from SIF.SIF_tilde_error import *

from oSoP.Constant import Constant
from oSoP.oSoP_Generator import best_oSoP_gen_from_dict
from oSoP.FPF import FPF
from oSoP.Variable import Variable
from oSoP.Constant import Constant

from copy import copy

from scipy.io import loadmat
import matplotlib.pyplot as plt
from math import log


from sys import path
path.append('../../construct/fipogen-v1/Examples/These')
from ex_gen import *


wl_var = 8
wl_cst = wl_var
wl_op = 2*wl_var
formatting = False
u_max = 1.

Et={}
Es={}
Ett={}

D=loadmat("ARITH23_BLTH_ex.mat")
listSIF = ["SIF_SS", "SIF_rho", "SIF_LWDF"]
#listSIF = ["SIF_LWDF"]
for sifName in listSIF:
	print "\n\n---------------- Structure "+sifName+" ----------------\n"
	Et[sifName] = []
	Es[sifName] = []
	Ett[sifName] = []
	Z=[]
	for i in range(4,13):
		if D[sifName][0][0][i].dtype == np.dtype('uint8'):
			D[sifName][0][0][i].dtype = np.dtype('int8')
		Z.append(D[sifName][0][0][i])

	S = SIF(Z)
	nt = S.l
	nx = S.n
	nu = S.q
	ny = S.p

	for wl_var in range(4,33):
		print "LARGEUR : ",wl_var
		wl_cst = wl_var
		wl_op = 2*wl_var

		V_m = []
		wcpg_txy = WCPG_txy(S)
		for i in range(nt + nx):
			V_m.append(u_max * wcpg_txy[i])
		V_m.append(u_max)
		y_max = u_max * wcpg_txy[-1]
		var_y = Variable(value_inf= -y_max, value_sup= y_max, wl=wl_var, name='y[k]')

		L_dico=[]
		for i in range(nt + nx + ny):
			# Création de la liste des constantes
			L_cst = [S.Z[i,j] for j in range(nt+nx+nu)]
			# cas particulier de la matrice J
			if (nt != 0) and (i < nt):
				L_cst[i]=0
				for j in range(i):
					L_cst[j] = -L_cst[j]

			# Création de la liste des variables
			list_name_var=['t%d[k+1]'%(j) for j in range(1,nt+1)]+['x%d[k]'%(j) for j in range(1,nx+1)]+['u%d[k]'%(j) for j in range(1,nu+1)]
			L_var = [Variable(value_inf= -V_m[j], value_sup= V_m[j], wl=wl_var, name=list_name_var[j]) for j in range(nt + nx + nu)]
			# nettoyage des 0
			list_cst=[]
			list_var=[]
			for j in range(len(L_cst)):
				if L_cst[j] != 0:
					list_cst.append(L_cst[j])
					list_var.append(L_var[j])
			D_out={}
			D_out["list_cst"] = list_cst
			D_out["list_var"] = list_var
			D_out["wl_cst"] = wl_cst
			D_out["wl_var"] = wl_var
			D_out["wl_mult"] = wl_op
			D_out["wl_add"] = wl_op
			D_out["formatting"] = formatting
			if i < nt+nx:
				D_out["fpf_final"] = copy(L_var[i].FPF)
			else:
				D_out["fpf_final"] = copy(var_y.FPF)
			
			# On ajoute le dico a la liste des dico
			L_dico.append(D_out)
		OSOP =best_oSoP_gen_from_dict(L_dico)
		eps=[]
		for osop in OSOP:
			eps.append(osop._Top._total_error.inter)

		Eps = np.matrix([u_max]+[abs(eps[i][0]) for i in range(len(eps))])
		

		# print "\n### Z erreur ###\n"
		# print "WCPG erreur : "
		# print(Serror.dSS.WCPG())


		Stilde, Serror = SIFH_to_SIFHstar(S, wl_var)
		Etilde = Serror.dSS.WCPG()[0,0]*u_max
		Estar = Serror.dSS.WCPG()[0,1:]*Eps.transpose()[1:,0]
		print Etilde,Estar[0,0], Estar[0,0]/Etilde
		print Serror.dSS.WCPG()*Eps.transpose()
		Et[sifName].append(Etilde)
		Es[sifName].append(Estar[0,0])
		Ett[sifName].append(Etilde+Estar[0,0])

plt.plot(range(4,33),Ett["SIF_SS"], "b*-")
plt.plot(range(4,33),Ett["SIF_rho"], "r*-")
plt.plot(range(4,33),Ett["SIF_LWDF"],"g*-")

plt.show()
