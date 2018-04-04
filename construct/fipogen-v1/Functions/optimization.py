# -*- coding: utf-8 -*-

from Functions.matlab_files_reader import coef2msb
from numpy import matrix
import numpy
from FxP.Constant import Constant
from math import log, ceil, floor
from scipy.io import loadmat

def contraintes_AMPL(fichier, bound=0):
	"""A partir d'un fichier .mat, génère le code AMPL pour l'ensemble des contraintes"""
	D = loadmat(fichier)
	nt = int(D["l"])
	nx = int(D["n"])
	nu = int(D["m"])
	ny = int(D["p"])
	Z = D["Z"]
	u_m = D["um"][0][0]
	u_r = D["ur"][0][0]
	dcu = [D["dcHu"][i][0] for i in range(len(D["dcHu"]))]
	wcpgu = D["wcpgHu"][0]
	dce = D["dcHe"][0]
	wcpge = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]

	mZ = coef2msb(Z)

	# Calcul des MSB des variables de sorties (m_var_out) et d'entrées (m_var_in)
	if nu == 1:
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
	else:
		m_var_out = []
		for i in range(nt+nx+ny):
			p = 1
			for j in range(nu):
				if abs(u_m[j][0]*dcu[i][j] - u_r[j][0]*wcpgu[i][j]) > abs(u_m[j][0]*dcu[i][j] + u_r[j][0]*wcpgu[i][j]):
					diff_out = u_m[j][0]*dcu[i][j] - u_r[j][0]*wcpgu[i][j]
				else:
					diff_out = u_m[j][0]*dcu[i][j] + u_r[j][0]*wcpgu[i][j]
			p *= diff_out
			m_var_out.append(coef2msb(p))
		m_var_in = m_var_out[: (nt+nx)] + [coef2msb(u_m[j][0] - u_r[j][0]) for j in range(nu)]


	# je construit mon vecteur de bornes sup (seulement SISO ou même borne sur chaque sortie)
	b=[2**bound]*ny


	if ny == 1 :
		A = [[abs(dce[i] + wcpge[i]) for i in range(nt+nx+ny)]]
		D = [[abs(dce[i] - wcpge[i]) for i in range(nt+nx+ny)]]
	else:
		A = [[abs(dce[i][j] + wcpge[i][j]) for j in range(nt+nx+ny)] for i in range(ny)]
		D = [[abs(dce[i][j] - wcpge[i][j]) for j in range(nt+nx+ny)] for i in range(ny)]
	
	delta=[]
	for i in range(ny):
		for j in range(nt+nx+ny):
			s=0
			l=0
			for k in range(nt+nx+nu):
				if Z[j][k] != 0 and (j >= nt or j != k):
					s += Z[j][k]
					l += 1
			if l >= 2:
				delta.append(int(floor(log(l-1,2))+1))
			else:
				delta.append(0)

			if l == 2 and abs(s) == 0: # utile pour la LGS mais on peut mieux faire
				A[i][j] = 0
				D[i][j] = 0
			else:
				# A[i][j] = float(A[i][j])*2**(m_var_out[j]+1) / b[i]
				# D[i][j] = float(D[i][j])*2**(m_var_out[j]+1) / b[i]
				# test nouvelle version plus fine
				#print float(A[i][j])*2**(m_var_out[j]+1) / b[i], float(A[i][j])*2**(m_var_out[j])*(1+(l-1)*2**(-delta[j])) / b[i]
				A[i][j] = float(A[i][j])*2**(m_var_out[j])*(1+(l-1)*2**(-delta[j])) / b[i]
				D[i][j] = float(D[i][j])*2**(m_var_out[j])*(1+(l-1)*2**(-delta[j])) / b[i]

	# sA = 0
	# sD = 0
	# for j in range(nt+nx+ny):
	# 	sA += A[0][j]
	# 	sD += D[0][j]
	# w_p = floor(log(max(sA,sD),2))+1
	# print w_p
	
	txt_i = "param N := %d;\n"%(nt+nx)
	txt_i += "param M := %d;\n"%(ny)
	txt_i += "param Q := %d;\n\n"%(2*ny)
	txt_i += "#--- Objective function\n\n"
	txt_i += "param c := \n"
	for j in range(nt+nx):
		txt_i += "\t%d 1\n"%(j+1)
	txt_i += ";\n\nparam d := \n"
	for j in range(ny):
		txt_i += "\t%d 1\n"%(j+1)

	k=97
	txt_i += ";\n\n#--- Constraint %d\nparam coefx :"%(k-96)
	for j in range(nt+nx):
		txt_i += " %d"%(j+1)
	txt_i += " :="
	for i in range(ny):
		txt_i += "\n\t%d"%(i*2+1)
		for j in range(nt+nx):
			txt_i += " %lf"%(A[i][j])
		txt_i += "\n\t%d"%(i*2+2)
		for j in range(nt+nx):
			txt_i += " %lf"%(D[i][j])
	txt_i += ";\n\n"

	txt_i += "param coefy :"
	for j in range(ny):
		txt_i += " %d"%(j+1)
	txt_i += " :="
	for i in range(ny):
		txt_i += "\n\t%d"%(i*2+1)
		for j in range(ny):
			txt_i += " %lf"%(A[i][j+(nt+nx)])
		txt_i += "\n\t%d"%(i*2+2)
		for j in range(ny):
			txt_i += " %lf"%(D[i][j+(nt+nx)])
	txt_i += ";\n\n"

	return txt_i


def wordlengths_cst_var_post_optim(fichier, W_var, rounding_mode="truncature", iso_wl=False):
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
			if not iso_wl:
				if len(d.keys()) > 1:
					if rounding_mode == "truncature":
						delta[i] = int(floor(log(len(d.keys())-1,2)))+1
					else:
						delta[i] = int(floor(log(len(d.keys()),2)))+1
				else:
					delta[i] = 0

	if not iso_wl:
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
				if not iso_wl:
					Lc[j] = W_var[i] + M_cst[i,j]+m_var_in[j]-m_var_out[i]+delta[i]+1
				else:
					Lc[j] = W_var[0]
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
