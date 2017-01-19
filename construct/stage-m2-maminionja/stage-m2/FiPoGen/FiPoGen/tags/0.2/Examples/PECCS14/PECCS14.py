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
b = [0.00132801779278 ,  0.00531207117112  , 0.00796810675667  , 0.00531207117112 ,  0.00132801779278]
a = [1,-2.87111622831650 ,  3.20825006629575 , -1.63459488108445 ,  0.31870932778967]
#print b,a
list_cst = list(b)+map(lambda x:-x,list(a))[1:]
list_wl_cst = Nb
list_wl_mult = Nb #2*Nb
wl_add = Nb
fpf_final = copy(list_inter_var[N+1].FPF)
#var_final = Variable(fpf=fpf_final)
RBAM = "RAM"

#BF
osop = best_oSoP_gen(list_name_var,list_inter_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, formatting=True)

print osop._Top._total_error.moments
print osop._Top._total_error.inter
osop.Code("Tikz")
osop.Code("C")	
