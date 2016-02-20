# -*- coding: utf-8 -*-

from ex_gen import *
from oSoP.Constant import Constant
from math import floor, log

def coef2msb(M):
	"""Calcule le msb de l'argument M. 
	- si M est un scalaire non nul, retourne le msb de M
	- si M est 0, retourne 'NULL'
	- si M est une liste (ou matrice), retourne la liste (ou matrice) des msb des éléments de M"""
	mM=[]
	if not isinstance(M,list) and not isinstance(M,numpy.ndarray):
	#Si M n'est ni une liste ni un tableau numpy
		if M != 0:
			return Constant(M,16).FPF.msb
		else:
			return "NULL"
	else:
	#Si M est une liste ou un tableau numpy, appels récursifs sur les éléments de M
		for i in range(len(M)):
			mM.append(coef2msb(M[i]))
	return mM

def wordlengths_cst_var_post_optim(fichier, W_var, rounding_mode="truncature"):
	"""Étant donnés le fichier .mat contenant les spécifications d'un filtre et la liste W_var
	des largeurs obtenues par optimisation, retourne les largeurs finales des coefficients et 
	des variables pour les produits dont les constantes sont non triviales"""

	D = loadmat(fichier)
	Z=D["Z"]
	nt = int(D["l"])
	nx = int(D["n"])
	nu = int(D["m"])
	ny = int(D["p"])
	u_m = D["um"][0][0]
	u_r = D["ur"][0][0]
	dcu = [D["dcHu"][i][0] for i in range(len(D["dcHu"]))]
	wcpgu = D["wcpgHu"][0]


	M_cst={} # clés : indices (i,j) du coefficient non trivial, valeurs : msb correspondant
	delta={} # clés : indice du SoP, valeurs : delta correspondant

	for i in range(nt+nx+ny):
		d={}
		for j in range(nt+nx+nu):
			if (i<nt):
				if i != j:
					if (Z[i][j] !=0):
						C=Constant(Z[i][j],wl=20)
						d[j] = C
			else:
				if (Z[i][j] !=0):
					C=Constant(Z[i][j],wl=20)
					d[j] = C
		if len(d.keys()) > 1 or (len(d.keys()) == 1 and d[d.keys()[0]].value != 1 ):
			for j in range(nt+nx+nu):
				if j in d.keys():
					M_cst[i,j] = d[j].FPF.msb
			if len(d.keys()) > 1:
				if rounding_mode == "truncature":
					delta[i] = int(floor(log(len(d.keys())-1,2)))+1
				else:
					delta[i] = int(floor(log(len(d.keys()),2)))+1
			else:
				delta[i] = 0

	m_var_out = []
	for i in range(nt+nx+ny):
		# calcul de la plus grande valeur représentable dans l'intervalle
		if abs(u_m*dcu[i] - u_r*wcpgu[i]) > abs(u_m*dcu[i] + u_r*wcpgu[i]):
			diff_out = u_m*dcu[i] - u_r*wcpgu[i]
		else:
			diff_out = u_m*dcu[i] + u_r*wcpgu[i]
		# calcul du msb de cette plus grance valeur
		m_var_out.append(coef2msb(diff_out))
	m_var_in = m_var_out[: (nt+nx)] + [coef2msb(u_m - u_r)]


	WL_cst = {} # clés : indice du SoP, valeurs : liste des largeurs des constantes du SoP
	WL_var = {} # clés : indice du SoP, valeurs : liste des largeurs des variables du SoP

	for i in range(nt+nx+ny):
		Lc={}
		Lv={}
		for j in range(nt+nx+nu):
			if (i,j) in M_cst.keys():
				Lc[j] = W_var[i] + M_cst[i,j]+m_var_in[j]-m_var_out[i]+delta[i]+1
				Lv[j] = W_var[j]
		if len(Lc.keys()) > 0:
			WL_cst[i] = Lc
			WL_var[i] = Lv

	# Calcul de la somme de toutes les largeurs obtenues
	s=0
	for i in WL_cst.keys():
		for j in WL_cst[i].keys():
			s+= WL_cst[i][j]
	for wl in W_var:
		if wl!=5:
			s+= wl
	print "Somme totale des différentes largeurs (constantes + variables) : "+str(s)
	return WL_cst, WL_var




















