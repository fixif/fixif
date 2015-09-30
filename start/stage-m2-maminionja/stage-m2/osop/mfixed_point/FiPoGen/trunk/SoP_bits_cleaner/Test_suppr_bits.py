#-*- coding:utf-8 -*-

from oSoP.FPR import FPR
from oSoP.Variable import Variable
from random import randint
from math import floor,ceil,log

from operator import attrgetter

# Constants
Nb = 16
beta_cst = Nb
beta_mult = 2 * Nb
beta_add = 2 * Nb
beta_final = Nb

def useless_bits_cleaner(L, beta_final):
	"""Cut down the useless bits of each FPR of the list L, according to the final wordlenght beta_final"""
	# Final FPR computation
	amax = max(L,key=attrgetter('_FPR.alpha'))
	fpr_final = FPR(beta = beta_final, alpha = amax+1)
	#print "Final "+repr(fpr_final)

	# We put elements with a gamma greater than final gamma into an empty list
	X=[]
	for x in L :
		if x.gamma > fpr_final.gamma :
			X.append(x)
	N = len(X)

	# delta_max computation
	delta_max = int(floor(log(N-1,2))) + 1
	i = 0
	while i < N:
		# Si un nombre est totalement tronqué (ou qu'il reste juste le bit de signe)
		if fpr_final.gamma + delta_max - 1 > -X[i].alpha:
			if fpr_final.gamma + delta_max <= X[i].gamma:
				X[i].gamma = fpr_final.gamma + delta_max
			i += 1
		else :
			X.remove(X[i])
			N -=1 
			print N
			delta_max = int(floor(log(N-1,2))) + 1
			i=0

def useless_bits_cleaner_for_interval(L, beta_final):
	"""Cut down the useless bits of FPR of each interval of the list L, according to the final wordlenght beta_final"""
	# Final FPR computation
	amax = max(L,key=attrgetter('_FPR.alpha'))
	fpr_final = FPR(beta = beta_final, alpha = amax+1)

	N = len(L)

	# delta_max computation
	delta_max = int(ceil(log(N,2))) + 1
	i = 0
	while i < N:
		# Si un nombre est totalement tronqué (ou qu'il reste juste le bit de signe)
		if fpr_final.gamma + delta_max - 1 > -L[i].FPR.alpha:
			if fpr_final.gamma + delta_max <= L[i].FPR.gamma:
				L[i] >> L[i].FPR.gamma - fpr_final.gamma - delta_max
			i += 1
		else :
			L.remove(L[i])
			N -=1 
			print N
			delta_max = int(ceil(log(N,2))) + 1
			i=0
	return delta_max


def simple_cleaned_SoP(list_cst, list_var,beta_final):
	l = len(list_cst)
	list_var_name = ["X_%d"%(i) for i in range(l)]
	list_fpr_cst = [FPR(beta = list_beta_cst[i], alpha=int(floor(log(abs(list_cst[i]),2)))+2) for i in range(l)]
	#type_var = type(list_var[0]) == FPR and "FPR" or "Interval"

	#if type_var == "FPR":
	#	list_mult = [Multiplier(list_cst[i],list_beta_cst[i],list_var[i],"",list_beta_mult[i],i) for i in range(l)]
	#	L = list_var
	#else:
	#	list_mult = [Multiplier2(list_cst[i],list_beta_cst[i],list_var[i],"",list_beta_mult[i],i) for i in range(l)]
	#	L = [i.fpr() for i in list_var]

	#On suppose tout d'abord qu'on a uniquement des intervalles et pas de FPR
	Products = []
	for i in range(l):
		Products.append( list_var[i].mult( int(list_cst[i] ,list_var[i].FPR.beta + list_cst[i].FPR.beta )))

	#On nettoie les bits
	delta_max = useless_bits_cleaner_for_interval(Products, beta_final)

	#On trie les intervalles suivant leurs gammas
	k=1
	for i in range(1,len(Products)):
		k=i
		while Products[k]<Products[k-1]:
			if k==0:
				break
			k-=1
		if k != i:
			p = Products.pop(i) 
			c = list_cst.pop(i)
			x = list_var_name.pop(i)
			Products.insert(k,p)
			list_cst.insert(k,c)
			list_var_name.insert(k,x)
	#Products.sort(key=lambda x: x.fpr().gamma,reverse = True)
	st = "("*(len(Products)+1)
	for i in range(len(Products)):
		st += "%d * %s)"%(list_cst[i].integer,list_var_name[i]) + (Products[i].FPR.gamma>Products[i].FPR.gamma)* ( (">> %d ") %(Products[i].FPR.gamma-Products[i].FPR.gamma) )
	st += (delta_max>0)* ">> %d )"%(delta_max)
	return st



	
	










