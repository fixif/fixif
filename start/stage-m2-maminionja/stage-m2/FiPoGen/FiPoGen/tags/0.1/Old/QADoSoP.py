# Quick and Dirty oSOP Generator

from  Ordered_SoP import *




# gives the value of the first element of t
# t can be a list of list of list...
def first(t):
	# take the 1st element until it is not a list
	while type(t)==type([]):
		t=t[0]
	return t



def list2oSoP( L, list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, list_beta_add, fpr_final, RndOff):
	# facon Quick&Dirty, je transforme un "tree" sous forme de liste de liste en un oSoP...
	# de [ [1,2], [3,4] ] on cree un osop correspondant a (x0+x1) + (x2 + x3)
	N=len(list_cst)
	osop = oSoP()
	if RndOff:
		osop._Multipliers = [Multiplier(list_cst[i], list_beta_cst[i], list_fpr_var[i], list_name_var[i], list_beta_mult[i],RndOff[i]) for i in range(N)]
	else:
		osop._Multipliers = [Multiplier(list_cst[i], list_beta_cst[i], list_fpr_var[i], list_name_var[i], list_beta_mult[i]) for i in range(N)]	

	osop._Top = l2oSoP( L, osop, list_beta_add)
	osop._Top._fpr_res = fpr_final
	return osop



def l2oSoP( L, osop, list_beta_add):
	"""L : la liste a transformer
	osop : l'osop cible de la la liste
	"""
	n = len(osop._Adders)
	add = Adder("A"+str(n), list_beta_add[n])
	osop._Adders.append( add)
	
	for op in L:
		if isinstance(op,list):
			add._operands.append( l2oSoP(op, osop, list_beta_add) )
			for a in osop._Adders:
				if a == add._operands[-1]:
					a._result = add
					break
		else:
			add._operands.append( osop._Multipliers[op-1] )
			osop._Multipliers[op-1]._result = add
	
	return add


	
def QAD_oSop_Generator(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, list_beta_add, fpr_final, RndOff = None):
	
	# Un generateur (avec yield) copier-coller depuis tree_thibault.py
	# qd j'ai un resultat (une liste de liste), je la passe a list2oSoP qui construit l'oSoP (en appelant recursivement l2oSoP pour chacun des operandes)
	
	
	# args
	N=len(list_cst)
	if not isinstance(list_fpr_var,list):
		list_fpr_var = [list_fpr_var]*N
	if not isinstance(list_beta_cst,list):
		list_beta_cst = [list_beta_cst]*N
	if not isinstance(list_beta_mult,list):
		list_beta_mult = [list_beta_mult]*N
	if not isinstance(list_beta_add,list):
		list_beta_add = [list_beta_add]*N
	if RndOff and (not isinstance(RndOff,list)):
		RndOff = [RndOff]*N
	if not isinstance(list_name_var,list):
		list_name_var = [list_name_var+repr(i) for i in range(N)]	
	
	
	
	# list of results : a result is a couple of couples of couples...
	# example : [[1,2],[3,4]] or [[[1,2],3],[4,5]]
	results = []
	
	
	# stack of possibilities to examin : a possibility is list of 
	# - a partial result (a list of lists of couples of indexes  )
	# - a list of non-yet-used indexes
	# example : [ [1,2], 3, 4 ]
	stack = [ range(1,N+1)  ]
	m = len(stack)
	while stack:
		
		# get first possibility
		indexes = stack.pop()
		
		# examin all the possibilities to take two of these indexes that satisfies the constraint
		# i,j are the two examined indexes (with i<j)
		for j in range(1,len(indexes)):
			for i in range(j):
				# check if the constraint is ok
				if first(indexes[i])>=first(indexes[0]):
					# re-copy the list
					result = list(indexes) 
					# then we can add element i with element j
					op_j = result.pop(j)
					op_i = result.pop(i)
					result.insert( 0, [op_i,op_j])
					# result is a final result or a partial result according to its length
					if len(result)==1:
						# add it to the list of possibilities
						#we have an oSop
						yield list2oSoP(result[0],list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, list_beta_add, fpr_final, RndOff)
					else:
						# or add this partial result to the stack (some of the indexes are not yet used)
						stack.append( result)
						if len(stack)> m :
							m = len(stack)
	print "au plus il y a %d elements dans la pile"%m
	
