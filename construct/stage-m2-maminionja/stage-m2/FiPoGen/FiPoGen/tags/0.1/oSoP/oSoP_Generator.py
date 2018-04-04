# -*- coding: utf-8 -*-
from copy import deepcopy
from copy import copy
from Adder import Adder
from Multiplier import Multiplier
from oSoP_class import oSoP
from Variable import Variable

def oSoP_Generator(list_name_var, list_inter_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, msb_final, alfix = None,plus = None, RndOff = None):

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

	m = len(stack)
	while stack:

		# get first possibility
		osops = stack.pop()

		# examin all the possibilities to take two of these osops that satisfies the constraint
		# i,j are the two examined osops (with i<j)
		for j in range(1,len(osops)):
			for i in range(j):
				# check if the constraint is ok
				if (osops[i] >= osops[0]) and (abs(osops[j].cmp_lsb(osops[i])) <= max_lsb):
				#if (osops[i]>=osops[0]):
					# re-copy the list
					result = osops[:]
					# then we can add element i with element j
					op_j = result.pop(j)
					op_i = result.pop(i)
					result.insert( 0, op_i.add(op_j,(alfix,plus,msb_final)) )
					#print len(result)
					
					# result is a final result or a partial result according to its length
					if len(result)==1:
						# add it to the list of possibilities
						#we have an oSop
						osop = oSoP(result[0], var_final)
						osop.Calc_var_result((alfix,plus,msb_final))
						yield osop
					else:
						# or add this partial result to the stack (some of the osops are not yet used)
						stack.append( result)
						if len(stack)> m :
							m = len(stack)
	print "au plus il y a %d elements dans la pile"%m