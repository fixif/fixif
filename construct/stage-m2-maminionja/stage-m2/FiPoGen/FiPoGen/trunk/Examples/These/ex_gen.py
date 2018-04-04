# -*- coding: utf-8 -*-

from FxP.FPF import FPF
from FxP.Variable import Variable
from FxP.Constant import Constant
from copy import copy

from numpy import matrix
import numpy
from math import log, ceil
from scipy.io import loadmat

def coef2msb(M):
	"""Calcule le msb de l'argument M. 
	- si M est un scalaire non nul, retourne le msb de M
	- si M est 0, retourne 'NULL'
	- si M est une liste (ou matrice), retourne la liste (ou matrice) des msb des éléments de M"""
	mM=[]
	if not isinstance(M,list) and not isinstance(M,numpy.ndarray):
	#Si M n'est ni une liste ni un tableau numpy
		if M != 0:
			return Constant(M,32).FPF.msb
		else:
			return "NULL"
	else:
	#Si M est une liste ou un tableau numpy, appels récursifs sur les éléments de M
		for i in range(len(M)):
			mM.append(coef2msb(M[i]))
	return mM

def MatlabDict2FilterExample_DFI(fichier, options=None):
	#Largeur des constantes et variables
	if options:
		wl_var = options["wl_var"]
		wl_cst = options["wl_cst"]
		wl_op = options["wl_op"]
		formatting = options["formatting"]
	else:
		wl_par = 16
		wl_op = 16
		formatting = True

	# Chargement du fichier
	D = loadmat(fichier)

	# On stocke les éléments du dictionnaire dans des variables
	nt = int(D["l"])
	nx = int(D["n"])
	nu = int(D["m"])
	ny = int(D["p"])
	Z = D["Z"]
	u_m = D["um"][0]
	u_r = D["ur"][0]
	dcu = D["dcHu"]
	wcpgu = D["wcpgHu"]
	dce = D["dcHe"]
	wcpge = D["wcpgHe"]

	# Calcul de l'intervalle de sortie
	y_m = u_m * dcu[-1][0]
	y_r = u_r * wcpgu[-1][0]
	print y_m-y_r,y_m+y_r

	# Création de la liste des constantes
	list_cst = list(Z[0])[1:]
	list_cst.reverse()

	# Création de la liste des variables
	list_name_var=['u[k]']+['u[k-%d]'%(i) for i in range(1,nx/2+1)]+['y[k-%d]'%(i) for i in range(1,nx/2+1)]
	list_var = [Variable(value_inf= u_m - u_r, value_sup= u_m + u_r, wl=wl_var, name=list_name_var[i]) for i in range(nx/2+1)]\
	+[Variable(value_inf= y_m - y_r, value_sup= y_m + y_r, wl=wl_var, name=list_name_var[nx/2+1+i]) for i in range(nx/2)]

	D_out={}
	D_out["list_cst"] = list_cst
	D_out["list_var"] = list_var
	D_out["wl_cst"] = wl_cst
	D_out["wl_var"] = wl_var
	D_out["wl_mult"] = wl_op
	D_out["wl_add"] = wl_op
	D_out["fpf_final"] = copy(list_var[-1].FPF)
	D_out["formatting"] = formatting
	# if options:
	# 	for k in options.keys():
	# 		D_out[k] = options[k]

	return D_out

def MatlabDict2FilterExample_SIF(fichier, options=None, dicos = None):
	if options:
		wl_var = options["wl_var"]
		wl_cst = options["wl_cst"]
		wl_op = options["wl_op"]
		formatting = options["formatting"]
	elif dicos:
		WL_var = dicos["WL_var"]
		WL_cst = dicos["WL_cst"]
		W_var = dicos["W_var"]
		formatting = dicos["formatting"]
	else:
		wl_par = 16
		wl_op = 16
		formatting = True

	# Chargement du fichier
	D = loadmat(fichier)

	# On stocke les éléments du dictionnaire dans des variables
	nt = int(D["l"])
	nx = int(D["n"])
	nu = int(D["m"])
	ny = int(D["p"])
	Z = D["Z"]
	u_m = D["um"][0]
	u_r = D["ur"][0]
	dcu = D["dcHu"]
	wcpgu = D["wcpgHu"]
	dce = D["dcHe"]
	wcpge = D["wcpgHe"]

	# Calcul des variables de calcul (SISO pour le moment)
	V_m = []
	V_r = []
	for i in range(nt + nx):
		V_m.append(u_m * dcu[i][0])
		V_r.append(u_r * wcpgu[0][i])
	V_m.append(u_m)
	V_r.append(u_r)
	
	# Calcul de l'intervalle de sortie
	y_m = u_m * dcu[-1][0]
	y_r = u_r * wcpgu[0][-1]
	if options:
		var_y = Variable(value_inf= y_m - y_r, value_sup= y_m + y_r, wl=wl_var, name='y[k]')
	elif dicos:
		var_y = Variable(value_inf= y_m - y_r, value_sup= y_m + y_r, wl=W_var[-1], name='y[k]')
	print y_m-y_r,y_m+y_r

	L_dico=[]

	for i in range(nt + nx + ny):

		#optim
		#var_res = Variable(value_inf= V_m[i][0] - V_r[i][0], value_sup= V_m[i][0] + V_r[i][0], wl=W_var[i], name="osef")
		
		# Création de la liste des constantes
		L_cst = list(Z[i])
		# cas particulier de la matrice J
		if (nt != 0) and (i < nt):
			L_cst[i]=0
			for j in range(i):
				L_cst[j] = -L_cst[j]
		
		# Création de la liste des variables
		list_name_var=['t%d[k+1]'%(j) for j in range(1,nt+1)]+['x%d[k]'%(j) for j in range(1,nx+1)]+['u%d[k]'%(j) for j in range(1,nu+1)]
		if options:
			L_var = [Variable(value_inf= V_m[j][0] - V_r[j][0], value_sup= V_m[j][0] + V_r[j][0], wl=wl_var, name=list_name_var[j]) for j in range(nt + nx + nu)]
			# nettoyage des 0
			list_cst=[]
			list_var=[]
			for j in range(len(L_cst)):
				if L_cst[j] != 0:
					list_cst.append(L_cst[j])
					list_var.append(L_var[j])
		elif dicos:
			if i in WL_var.keys():
				L_var = [Variable(value_inf= V_m[j][0] - V_r[j][0], value_sup= V_m[j][0] + V_r[j][0], wl=WL_var[i][j], name=list_name_var[j]) for j in range(nt + nx + nu) if j in WL_var[i].keys()]
				list_cst=[L_cst[j] for j in WL_var[i].keys()]
				list_var=L_var

		


		# if len(list_cst)==3:
		# 	print i, list_cst
		if options:
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
		elif dicos and i in WL_cst.keys():
			D_out={}
			D_out["list_cst"] = list_cst
			D_out["list_var"] = list_var
			D_out["wl_cst"] = [WL_cst[i][j] for j in range(nt + nx + nu) if j in WL_var[i].keys()]
			D_out["wl_var"] = [WL_var[i][j] for j in range(nt + nx + nu) if j in WL_var[i].keys()]
			D_out["wl_mult"] = W_var[i]
			D_out["wl_add"] = W_var[i]
			D_out["formatting"] = formatting
			if i < nt+nx:
				D_out["fpf_final"] = copy(var_res.FPF)
			else:
				D_out["fpf_final"] = copy(var_y.FPF)
			
			# On ajoute le dico a la liste des dico
			L_dico.append(D_out)
	return L_dico

def Z2tex(fichier):
	tex = ""
	# Chargement du fichier
	D = loadmat(fichier)

	# On stocke les éléments du dictionnaire dans des variables
	nt = int(D["l"])
	nx = int(D["n"])
	nu = int(D["m"])
	ny = int(D["p"])
	Z = D["Z"]

	tex += "\\begin{pmat}({"
	if nt > 0:
		tex += "."*(nt-1)+"|"+"."*(nx-1)+"|"+"."*(nu-1)+"})\n\t"
	else:
		tex += "."*(nx-1)+"|"+"."*(nu-1)+"})\n\t"

	for i in range(nt+nx+ny):
		L_cst = list(Z[i])
		for j in range(nt+nx+nu):
			if j == nt+nx+nu-1:
				tex += " %.6g "%(L_cst[j])
			else:
				tex += " %.6g &"%(L_cst[j])
		tex += "\cr"
		if i == nt+nx+ny-1:
			tex += "\n"
		else:
			if (i == nt-1) or (i == nt+nx-1):
				tex += "\-"
			tex += "\n\t"
	tex += "\\end{pmat}"
	tex.replace("e-","\texttt{e-}")
	return tex

def M2tex(M):
	#pour les matrices numpy
	tex = "\\begin{pmatrix}"
	n=len(M)
	for i in range(n):
		#L_cst = list(M[i])
		for j in range(n):
			if j == n-1:
				tex += " %.6g "%(M[i,j])
			else:
				tex += " %.6g &"%(M[i,j])
		if i == n-1:
			tex += "\n"
		else:
			tex += "\\\\\n\t"
	tex += "\\end{pmatrix}"
	tex.replace("e-","\texttt{e-}")
	return tex










