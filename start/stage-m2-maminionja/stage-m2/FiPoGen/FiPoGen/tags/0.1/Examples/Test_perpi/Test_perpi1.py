# Exemples pour DASIP-12

from oSoP.oSoP_Generator import oSoP_Generator
from oSoP.FPF import FPF
from oSoP.Variable import Variable
from oSoP.Constant import Constant
#from scipy.signal.filter_design import butter
#from control import TransferFunction
#from control.matlab import tf
#from scipy.signal import dimpulse
#from scipy.linalg import norm
from copy import deepcopy

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
list_wl_mult = 2*Nb
wl_add = 2*Nb
fpf_final = list_inter_var[N+1].FPF.copy()
#var_final = Variable(fpf=fpf_final)
RBAM = "RAM"




nb=0
LT=[]
best_osop = None
best_mean = 10000
#for L in oSoP_Generator(list_name_var, list_fpf_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, fpf_final.msb, alfix = False,plus = False, RndOff = RBAM):
for L in oSoP_Generator(list_name_var, list_inter_var, list_cst, list_wl_cst, list_wl_mult, wl_add, fpf_final, fpf_final.msb, alfix = False,plus = False, RndOff = RBAM):
	nb+=1
	if nb%10000==0:
		print nb
	#print L._Top._total_error.moments
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



print best_osop._Top._total_error.moments
print best_osop._Top._total_error.inter
print best_osop._var_final.FPF
print best_osop._var_final.integers
print best_osop._var_final.approx_values
print best_osop._var_final.values

#print best_osop._Top._var_result.FPF, best_osop._Top._var_result.values
best_osop.Code("Tikz")
best_osop.Code("C")

