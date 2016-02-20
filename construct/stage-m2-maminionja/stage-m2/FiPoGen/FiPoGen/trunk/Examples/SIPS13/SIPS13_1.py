# -*- coding: utf-8 -*-

# Exemples pour SIPS-13

from oSoP.oSoP_Generator import oSoP_Generator
from oSoP.FPR import FPR
from oSoP.Variable import Variable
from oSoP.Constant import Constant
from copy import deepcopy


def best_oSoP_gen(list_name_var, list_inter_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, alpha_final, alfix = False,plus = False, RndOff = "RAM"):
	LT=[]
	best_osop = None
	best_mean = 10000
	for L in oSoP_Generator2(list_name_var, list_inter_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, alpha_final, alfix = False,plus = False, RndOff = RBAM):
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


N=4
Nb = 16
list_beta_cst = Nb
list_beta_mult = 2*Nb
beta_add = 2*Nb
RBAM = "RAM"
Best_oSoP=[]



# définition des variables à partir de leur intervalle de définition
# u: 10
u = Variable(value_inf=-10, value_sup=10, beta=Nb)
# T0: 37.753689143952471
T0 = Variable(value_inf=-37.753689143952471, value_sup=37.753689143952471, beta=Nb)
# xn[0]: 33.074773700982021
xn0 = Variable(value_inf=-33.074773700982021, value_sup=33.074773700982021, beta=Nb)
# xn[1]: 17.801683667907806
xn1 = Variable(value_inf=-17.801683667907806, value_sup=17.801683667907806, beta=Nb)
# xn[2]: 9.915357623867267
xn2 = Variable(value_inf=-9.915357623867267, value_sup=9.915357623867267, beta=Nb)
# xn[3]: 11.906912315145979
xn3 = Variable(value_inf=-11.906912315145979, value_sup=11.906912315145979, beta=Nb)
# y: 37.753689143952471
y=Variable(value_inf=-37.753689143952471, value_sup=37.753689143952471, beta=Nb)



""" Premier Produit Scalaire """
# T0 =  xn[0] + 0.467891544297045103295573653667815960943698883056640625*u    ;

list_name_var=['xn[0]','u']
list_inter_var = [xn0.copy(),u.copy()]
list_cst = [ 1.0 ,0.467891544297045103295573653667815960943698883056640625]
fpr_final = y.FPR.copy()

Best_oSoP.append(best_oSoP_gen(list_name_var, list_inter_var, list_cst, 
                       list_beta_cst, list_beta_mult, 
                       beta_add, fpr_final, 
                       fpr_final.alpha))

""" Second Produit Scalaire """
# xn[0] = -0.12236628927527419541387843082702602259814739227294921875*xn[0]
# + -1.3554822828291879233120198477990925312042236328125*u    \
# + -0.00029145984329026486392422157223336398601531982421875*T0   \
# + xn[1] ;

list_name_var=['xn[0]','u', 'T0','xn[1]']
list_inter_var = [xn0.copy(),u.copy(),T0.copy(),xn1.copy()]
list_cst = [-0.12236628927527419541387843082702602259814739227294921875,-1.3554822828291879233120198477990925312042236328125,-0.00029145984329026486392422157223336398601531982421875,1.]
fpr_final = xn0.FPR.copy()

Best_oSoP.append(best_oSoP_gen(list_name_var, list_inter_var, list_cst, 
                       list_beta_cst, list_beta_mult, 
                       beta_add, fpr_final, 
                       fpr_final.alpha))

""" Troisième Produit Scalaire """
# xn[1] = 0.388136596759655450039616653157281689345836639404296875*xn[1]\
# + 0.54284325134847366545187696829088963568210601806640625*u    \
# + 0.0469279637109754066415234774467535316944122314453125*T0   \
# + xn[2]   ;
list_name_var=['xn[1]','u', 'T0','xn[2]']
list_inter_var = [xn1.copy(),u.copy(),T0.copy(),xn2.copy()]
list_cst = [0.388136596759655450039616653157281689345836639404296875,0.54284325134847366545187696829088963568210601806640625, 0.0469279637109754066415234774467535316944122314453125, 1. ]
fpr_final = xn1.FPR.copy()

Best_oSoP.append(best_oSoP_gen(list_name_var, list_inter_var, list_cst, 
                       list_beta_cst, list_beta_mult, 
                       beta_add, fpr_final, 
                       fpr_final.alpha))

""" Quatrième Produit Scalaire """
#xn[2] = -0.7620024487294585480157138590584509074687957763671875*xn[2]\
# + -0.25421489137462227603236897266469895839691162109375*u    \
# + -0.00485692688638879321860741811178741045296192169189453125*T0   \
# + xn[3]   ;
list_name_var=['xn[2]','u', 'T0','xn[3]']
list_inter_var = [xn2.copy(),u.copy(),T0.copy(),xn3.copy()]
list_cst = [-0.7620024487294585480157138590584509074687957763671875,-0.25421489137462227603236897266469895839691162109375,-0.00485692688638879321860741811178741045296192169189453125, 1.]
fpr_final = xn2.FPR.copy()

Best_oSoP.append(best_oSoP_gen(list_name_var, list_inter_var, list_cst, 
                       list_beta_cst, list_beta_mult, 
                       beta_add, fpr_final, 
                       fpr_final.alpha))

""" Cinquième Produit Scalaire """
#    xn[3] = 0.88082344225689779282362223966629244387149810791015625*xn[3]\
# + -0.1419926166774596598685320714139379560947418212890625*u    \
# + 0.0002717061364786166333118444526917301118373870849609375*T0   ;
list_name_var=['xn[3]','u', 'T0']
list_inter_var = [xn3.copy(),u.copy(),T0.copy()]
list_cst = [0.88082344225689779282362223966629244387149810791015625,-0.1419926166774596598685320714139379560947418212890625,0.0002717061364786166333118444526917301118373870849609375]
fpr_final = xn3.FPR.copy()

Best_oSoP.append(best_oSoP_gen(list_name_var, list_inter_var, list_cst, 
                       list_beta_cst, list_beta_mult, 
                       beta_add, fpr_final, 
                       fpr_final.alpha))




for i,osop in enumerate(Best_oSoP):
	print osop._Top._total_error.moments
	print osop._Top._total_error.inter
	print osop._var_final.FPR
	osop.Code("Tikz",indice=i)
	osop.Code("C",indice=i)	


#print best_osop._Top._var_result.FPR, best_osop._Top._var_result.values


