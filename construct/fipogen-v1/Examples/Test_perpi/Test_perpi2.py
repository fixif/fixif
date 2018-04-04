# Exemple

from FxP.oSoP_Generator import oSoP_Generator2, best_oSoP_gen
from FxP.FPF import FPF
from FxP.Variable import Variable
from FxP.Constant import Constant
from copy import copy

N=4
Nb = 16

list_name_var=['u[n]']+['u[n-%d]'%(i) for i in range(1,N+1)]+['y[n-%d]'%(i) for i in range(1,N+1)]
#list_name_var_code = ['u%d'%(i) for i in range(0,N+1)]+['y%d'%(i) for i in range(1,N+1)]
#list_fpf_var = FPF(wl = Nb, msb = 5)
list_inter_var = [Variable(value_inf=-13, value_sup=13, wl=Nb) for i in range(N+1)]\
    +[Variable(value_inf=-17.123541221107534, value_sup=17.123541221107534, wl=Nb) for i in range(N)]
b = [0.001328017792779 ,  0.005312071171115  , 0.007968106756673  , 0.005312071171115 ,  0.001328017792779]
a = [1,-2.871116228316502 ,  3.208250066295749 , -1.634594881084453 ,  0.318709327789667]
#print b,a
list_cst = list(b)+map(lambda x:-x,list(a))[1:]
list_wl_cst = Nb
list_wl_mult = 2*Nb #Nb
wl_add = 2*Nb
fpf_final = copy(list_inter_var[N+1].FPF)
#var_final = Variable(fpf=fpf_final)
RBAM = "RAM"


best_osop = best_oSoP_gen(list_name_var,list_inter_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, formatting=False)



print best_osop._Top._total_error.moments
print best_osop._Top._total_error.inter

best_osop.Code("Tikz")
#best_osop.Code("C")

