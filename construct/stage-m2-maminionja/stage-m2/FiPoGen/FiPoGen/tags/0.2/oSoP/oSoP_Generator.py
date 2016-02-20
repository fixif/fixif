# -*- coding: utf-8 -*-
from copy import deepcopy
from copy import copy
from Adder import Adder
from Multiplier import Multiplier
from oSoP_class import oSoP
from Variable import Variable
from FPF import FPF

from math import ceil, log

def oSoP_Generator(list_name_var, list_inter_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, alfix = None,plus = None, RndOff = None):

	# Un generateur (avec yield) copier-coller depuis tree_thibault.py
	# qd j'ai un resultat (une liste de liste), je la passe a list2oSoP qui construit l'oSoP (en appelant recursivement l2oSoP pour chacun des operandes)


	# args
	N=len(list_cst)
	if not isinstance(list_inter_var,list):
		list_inter_var = [list_inter_var]*N
	if not isinstance(list_wl_cst,list):
		list_wl_cst = [list_wl_cst]*N
	if not isinstance(list_wl_mult,list):
		list_wl_mult = [list_wl_mult]*N
	if RndOff and (not isinstance(RndOff,list)):
		RndOff = [RndOff]*N
	if not isinstance(list_name_var,list):
		list_name_var = [list_name_var+repr(i) for i in range(N)]	
	Adder.wl_add = wl_add
	var_final = Variable(fpf = fpf_final)

	# list of results : a result is a couple of couples of couples...
	# example : [[1,2],[3,4]] or [[[1,2],3],[4,5]]
	results = []


	# stack of possibilities to examin : a possibility is list of 
	# - a partial result (a list of lists of couples of indexes  )
	# - a list of non-yet-used indexes
	# example : [ [1,2], 3, 4 ]
	stack = [ range(1,N+1)  ]

	if RndOff:
		stack = [ [ Multiplier(list_cst[i], list_wl_cst[i], list_inter_var[i], list_name_var[i], list_wl_mult[i],i,RndOff[i]) for i in range(N) ] ]
	else:
		stack = [ [ Multiplier(list_cst[i], list_wl_cst[i], list_inter_var[i], list_name_var[i], list_wl_mult[i],i) for i in range(N) ] ]

	stack[0].sort(Multiplier.cmp_lsb)
	max_lsb=0
	for i in range(N-1):
		max_lsb = max(max_lsb,abs(stack[0][i+1].result.lsb-stack[0][i].result.lsb))

	delta = int(ceil(log(N,2)))
	fpf_add = FPF(wl=fpf_final.wl+delta, msb=fpf_final.msb, lsb=fpf_final.lsb-delta, signed=fpf_final._signed)


	m = len(stack)
	while stack:

		# get first possibility
		osops = stack.pop()

		# examin all the possibilities to take two of these osops that satisfies the constraint
		# i,j are the two examined osops (with i<j)
		for j in range(1,len(osops)):
			for i in range(j):
				# check if the constraint is ok
				#if (osops[i] >= osops[0]) and (abs(osops[j].cmp_lsb(osops[i])) <= max_lsb):
				if (osops[i]>=osops[0]):
					# re-copy the list
					result = osops[:]
					# then we can add element i with element j
					op_j = result.pop(j)
					op_i = result.pop(i)
					result.insert( 0, op_i.add(op_j,(alfix,plus,fpf_add)) )
					#print len(result)
					
					# result is a final result or a partial result according to its length
					if len(result)==1:
						# add it to the list of possibilities
						#we have an oSop
						osop = oSoP(result[0], var_final)
						osop.Calc_var_result((alfix,plus,fpf_add))
						yield osop
					else:
						# or add this partial result to the stack (some of the osops are not yet used)
						stack.append( result)
						if len(stack)> m :
							m = len(stack)
	
	
def oSoP_Generator2(multipliers, max_lsb, fpf_add, var_final, alfix = None, plus = None):
	# args
	N=len(multipliers)

	results = []
	stack = [ multipliers  ]

	m = len(stack)
	while stack:

		# get first possibility
		osops = stack.pop()

		# examin all the possibilities to take two of these osops that satisfies the constraint
		# i,j are the two examined osops (with i<j)
		for j in range(1,len(osops)):
			for i in range(j):
				# check if the constraint is ok
				if (osops[i] >= osops[0]) and (abs(osops[j].cmp_lsb(osops[i])) <= max_lsb+1):
				#if (osops[i]>=osops[0]):
					# re-copy the list
					result = osops[:]
					# then we can add element i with element j
					op_j = result.pop(j)
					op_i = result.pop(i)
					result.insert( 0, op_i.add(op_j,(alfix,plus,fpf_add)) )
					#print len(result)
					
					# result is a final result or a partial result according to its length
					if len(result)==1:
						# add it to the list of possibilities
						#we have an oSop
						osop = oSoP(result[0], var_final)
						
						#test (ligne de dessous en commentaire)
						osop.Calc_var_result((alfix,plus,fpf_add))
						yield osop
					else:
						# or add this partial result to the stack (some of the osops are not yet used)
						stack.append( result)
						if len(stack)> m :
							m = len(stack)
	
	
def best_oSoP_gen(variables_name, variables, constants, constants_wordlength, multipliers_wordlength,\
                  adders_wordlength, fpf_final, alfix = False,plus = False, RndOff = "RAM", formatting = True):
	
	# args
	N=len(constants)
	delta=0
	
	if formatting:
		Variable.formatting = True
		Adder.formatting = True
		Multiplier.formatting = True
		
		delta = int(ceil(log(N,2)))
		Adder.wl = adders_wordlength + delta
		multipliers_wordlength += delta
		lsb_final = fpf_final.lsb - delta
	else:
		Variable.formatting = False
		Adder.formatting = False
		Multiplier.formatting = False		
		lsb_final = 0
	
	if not isinstance(constants_wordlength,list):
		constants_wordlength = [constants_wordlength]*N
	if not isinstance(multipliers_wordlength,list):
		multipliers_wordlength = [multipliers_wordlength]*N
	if RndOff and (not isinstance(RndOff,list)):
		RndOff = [RndOff]*N
	if not isinstance(variables_name,list):
		variables_name = [variables_name+repr(i) for i in range(N)]	
	Adder.wl_add = adders_wordlength
	var_final = Variable(fpf = fpf_final)
	
	# Multipliers creation from args
	multipliers = [Multiplier(constants[i], constants_wordlength[i], variables[i], variables_name[i],\
	                          multipliers_wordlength[i], i, RndOff=RndOff[i], lsb_final=lsb_final) for i in range(N)]
	multipliers.sort(Multiplier.cmp_lsb)
	
	# Heuristic for non-exhaustive generation
	# Computation of max_lsb, the maximum difference of lsb between two consecutive multipliers (in the sorted list)
	max_lsb=0
	for i in range(N-1):
		max_lsb = max(max_lsb , abs(multipliers[i+1].result.lsb - multipliers[i].result.lsb))	
	
	best_osop = None
	h=N
	
	# formatting is the bits cleaning option
	if formatting:
		# Computation of fpf_add, ie fpf_final 'plus' delta bits considered for additions
		fpf_add = FPF(wl=fpf_final.wl+delta, msb=fpf_final.msb, lsb=fpf_final.lsb-delta, signed=fpf_final._signed)
		for L in oSoP_Generator2(multipliers, max_lsb, fpf_add, var_final, alfix = False,plus = False):
			if L.height() ==ceil(log(N,2)):
				h=L.height()
				best_osop = L
				break
		
	# if formatting == False we use default parameters
	else:
		fpf_add = FPF(wl=adders_wordlength, msb=fpf_final.msb)
		
		nb=0
		LT=[]
		best_mean = 10000
		for L in oSoP_Generator2(multipliers, max_lsb, fpf_add, var_final, alfix = False,plus = False):
			nb+=1
			if nb%10000 == 0:
				print nb
				#LT.append(L)
				#break
			if L._Top._total_error.mean <= best_mean:
				if L._Top._total_error.mean < best_mean:
					LT=[]
				LT.append(L)
				best_mean = L._Top._total_error.mean
				best_osop = L
		
		
		h = LT[0].height()
		for L in LT:
			if L.height() <=h:
				h=L.height()
				best_osop = L
		
	return best_osop