from Ordered_SoP import *
import random as rd
from FPR import FPR
from scipy.signal.filter_design import butter


#################################################################################################
#Srcript
#################################################################################################

list_fpr_var = [FPR(10,3),FPR(8,2),FPR(8,6),FPR(8,4)]

#b,a = butter(3,[0.2,0.3])
#list_cst = list(a)+map(lambda x:-x,list(b))[1:]
list_cst = [-1.9121,12.1819,11.577,-7.6734]

list_beta_cst = [8,9,8,8]
list_beta_mult = 16
list_beta_add = 16
#list_name_var = ["U(n-%d)"%(i,) for i in range(4)]+["Y(n-%d)"%(i,) for i in range(1,4)]
list_name_var = ['X'+repr(i) for i in range(len(list_cst))]
#osop = oSoP()
#osop._Multipliers = [Multiplier(list_cst[i], list_beta_cst, list_fpr_var, list_name_var[i], list_beta_mult,"RAM") for i in range(7)]
#osop._Top = osop._Multipliers[0]
#osop = insert_adder_on_multiplier(0, osop, 1, list_beta_add)
#osop = insert_adder_on_multiplier(1, osop, 2, list_beta_add)
#osop = insert_adder_on_adder(1, osop, 3, list_beta_add)
#osop = insert_adder_on_multiplier(3, osop, 4, list_beta_add)
#osop = insert_adder_on_multiplier(1, osop, 5, list_beta_add)
#osop = insert_adder_on_multiplier(1, osop, 6, list_beta_add)
#osop._Top._fpr_res = FPR(8,15)
#osop.Calc_FPR_Noise(alfix = True, plus = False)
#osop.Code("Tikz")


LT = oSoP_Generator(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult,list_beta_add,FPR(8,13),"RBM")

best_tree=LT[0]
best_tree.Calc_FPR_Noise(alfix = False, plus = False)
#best_tree.Code("Tikz")

#LT[0].Calc_FPR_Noise(alfix = True, plus = True)
##LT[0]._Top.Calc_FPR_Noise()
t_eq=[]
h=len(list_cst)
for t in LT:
	##if t._Top._total_noise[1] < best_var:
		##best_var = t._Top._total_noise[1]
		##best_tree = t
		##t_eq=[best_tree]
	if t.height() <= h :
		if t.height() == h :
			t_eq.append(t)
		else:
			t_eq = [t]
		h=t.height()


best_mean = LT[0]._Top._total_noise[0]
best_var = LT[0]._Top._total_noise[1]
for t in t_eq:	
	t.Calc_FPR_Noise(alfix = False, plus = False)
	if t._Top._total_noise[0] <= best_mean:
		#if (t._Top._total_noise[0] == best_mean):
			#t_eq.append(t)
		#else:
		best_mean = t._Top._total_noise[0]
		best_var = t._Top._total_noise[1]
		best_tree = t

#best_tree.Code("Tikz")
##print len(t_eq)
####for t in t_eq:
####	print t._Top._total_noise[1]
#h=len(list_cst)
#for t in t_eq:
	###if t._Top._total_noise[1] < best_var:
		###best_var = t._Top._total_noise[1]
		###best_tree = t
		###t_eq=[best_tree]
	#if t.height() < h :
		#h=t.height()
		#best_tree = t
best_tree.Code("Tikz")

