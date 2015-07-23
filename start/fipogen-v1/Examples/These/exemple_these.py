# -*- coding: utf-8 -*-

from ex_gen import *
from datetime import datetime
from oSoP.Adder import Adder
from oSoP.oSoP_Generator import best_oSoP_gen_from_dict
from exT_optim_eval import *
from pickle import dump


def erreur_finale(eps, wcpgHe, dcgHe):
	delta_y=[0,0]
	for i in range(len(eps)):
		moy=(eps[i][1]+eps[i][0])/2
		ray=(eps[i][1]-eps[i][0])/2
		delta_y[0] += -dcgHe[i]*moy - wcpgHe[i]*ray
		delta_y[1] += -dcgHe[i]*moy + wcpgHe[i]*ray
	return delta_y


# options_DFI = {'wl_var':16, 'wl_cst':16, 'wl_op':32, 'formatting':False}

# DFI = MatlabDict2FilterExample_DFI("Examples/These/ex_bis/DFI.mat", options_DFI)
# osop_DFI = best_oSoP_gen_from_dict(DFI)

# print osop_DFI._Top._total_error.moments
# print osop_DFI._Top._total_error.inter
# eps=[]
# eps.append(osop_DFI._Top._total_error.inter)
# osop_DFI.Code("C")
# # osop_DFI.Code("Tikz")
# D = loadmat("Examples/These/ex_bis/DFI.mat")
# dcgHe = D["dcHe"][0]
# wcpgHe = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]
# print erreur_finale(eps, wcpgHe, dcgHe)



# print Z2tex("Examples/These/rhoDFIIt.mat")
# W_var ={"rhoDFIIt":[17,17,18,18,17,18,16,16,18,18,17,18,17,17,17,18,16],\
# W_var ={"rhoDFIIt":[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19],\
# 	"ss1":[19,13,16,13,12,11,5,3,15],\
# 	"ss2":[19,22,19,21,20,22,22,22,15],\
# 	"ss3":[15,15,15,15,15,18,18,16,15],\
# 	"ss4":[16,17,17,18,18,20,17,19,15],\
# 	"ss5":[17,18,18,17,17,19,17,17,15],\
# 	"ss6":[16,18,17,19,18,20,17,18,15],\
# 	"LGS":[5,18,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,18,\
#  		5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,18,5,5,5,5,5,5,5,5,17,\
#  		5,5,5,5,5,5,5,18,5,5,5,5,5,5,18,5,5,5,5,5,5,19,5,5,5,5,5,5,19,5,5,5,5,5,5,19,5,5,5,5,5,5,19,5,5,5,5,5,5,19,5,5,5,5,5,5,21,\
#  		5,5,5,5,5,5,5,21,18,18,18,18,18,17,17,21,18,18,18,18,18,17,17,13]}
#rho W_var = [20,19,19,18,18,17,13,11,19,19,19,19,18,16,12,11,18]
#ss2 W_var = [21,21,20,22,21,20,22,20,17]
#LGS W_var = [5,21,5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,5,21,5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,5,20,\
 	#5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,5,20,5,5,5,5,5,5,5,21,5,5,5,5,5,5,5,5,19,5,5,5,5,5,5,5,19,5,5,5,5,5,5,5,5,20,\
 	#5,5,5,5,5,5,5,20,5,5,5,5,5,5,20,5,5,5,5,5,5,20,5,5,5,5,5,5,19,5,5,5,5,5,5,20,5,5,5,5,5,5,21,5,5,5,5,5,5,21,5,5,5,5,5,5,20,\
 	#5,5,5,5,5,5,5,20,20,20,20,19,19,19,18,20,20,20,20,19,19,19,18,17]
#ss3 W_var = [17,17,14,18,17,18,19,15,17]
#ss4 W_var = [19,20,17,19,18,19,18,20,17]
#SS5 W_var = [20,20,17,19,18,19,19,19,17]
#ss6 W_var = [18,19,17,18,19,19,18,18,17]
L_osops = []
Noms = ["rhoDFIIt","ss5","ss6","rhoDFIIt","LGS","ss1"]
for nom in Noms:
	print ""
	print nom
	#print Z2tex("Examples/These/ex_bis/%s.mat"%(nom))
	#optim
	#WL_cst, WL_var = wl_cst_var("Examples/These/ex_bis/%s.mat"%(nom),W_var[nom])
	#DWL = {"W_var":W_var[nom], "WL_cst":WL_cst, "WL_var":WL_var, "formatting":True}
	options_DFI = {'wl_var':16, 'wl_cst':16, 'wl_op':32, 'formatting':False}


	startTime = datetime.now()
	DSIF = MatlabDict2FilterExample_SIF("Examples/These/ex_bis/%s.mat"%(nom), dicos=None, options=options_DFI)
	OSOP =best_oSoP_gen_from_dict(DSIF)
	eps=[]
	for i,osop in enumerate(OSOP):
		print osop._Top._total_error.moments
		print osop._Top._total_error.inter
		eps.append(osop._Top._total_error.inter)
		#if isinstance(osop._Top, Adder):
			#osop.Code("Tikz",indice=i,name=nom)
		#osop.Code("C",indice=i,name=nom)
		L_osops.append(osop)

	print(datetime.now()-startTime)

	D = loadmat("Examples/These/ex_bis/%s.mat"%(nom))
	dcgHe = D["dcHe"][0]
	wcpgHe = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]
	print erreur_finale(eps, wcpgHe, dcgHe)

# fichier = open("Examples/These/liste_osops_19.pkl", "w")
# dump(L_osops, fichier)
# fichier.close()
