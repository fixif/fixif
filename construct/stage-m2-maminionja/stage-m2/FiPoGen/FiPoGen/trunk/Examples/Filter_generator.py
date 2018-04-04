from FxP.oSoP_Generator import oSoP_Generator,oSoP_Generator2
from FxP.FPR import FPR
from FxP.Interval import Interval
from scipy.signal.filter_design import butter
from control import TransferFunction
from control.matlab import tf
from scipy.signal import dimpulse
from scipy.linalg import norm
from copy import deepcopy
from random import uniform,seed

def filter_like(N):
	seed()
	b = [ uniform(0.001,0.02)  for i in range(N+1)]
	a = [1]+ [ uniform(-3, 3) for i in range(N)]
	return b,a

N=4
Nb = 16

list_name_var=['u[n]']+['u[n-%d]'%(i) for i in range(1,N+1)]+['y[n-%d]'%(i) for i in range(1,N+1)]
#list_name_var_code = ['u%d'%(i) for i in range(0,N+1)]+['y%d'%(i) for i in range(1,N+1)]
list_fpr_var = FPR(beta = Nb, alpha = 5)
#list_inter_var = Interval(FPR(beta = Nb, alpha = 5))
b,a = filter_like(N)
print b,a
#b,a = [0.013778139811841412, 0.006675716344481324, 0.0050251354820911075, 0.01420356705051743, 0.009706971154156543], [1, 0.5724295013211504, 2.8310730652071294, 2.026829651455106, 1.9803449070527384, -2.327036293605821]
list_cst = list(b)+map(lambda x:-x,list(a))[1:]
list_beta_cst = Nb
list_beta_mult = 2*Nb
beta_add = 2*Nb
fpr_final = FPR(beta = 2*Nb, alpha = 9)
inter_final = Interval(fpr_final)
RBAM = "RAM"




nb=0
LT=[]
best_osop = None
best_mean = 10000
for L in oSoP_Generator(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, fpr_final.alpha, alfix = False,plus = False, RndOff = RBAM):
#for L in oSoP_Generator2(list_name_var, list_inter_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, fpr_final.alpha, alfix = False,plus = False, RndOff = RBAM):
	nb+=1
	if nb%10000==0:
		print nb
	if L._Top._total_noise[0] <= best_mean:
		if L._Top._total_noise[0] < best_mean:
			LT=[]
		LT.append(L)
		best_mean = L._Top._total_noise[0]
	#if L._Top._name == "Add_11026":
		#print L._Top._inter_res

h = LT[0].height()
for L in LT:
	if L.height() <=h:
		h=L.height()
		best_osop = L
print best_mean
print best_osop._Top._total_noise[1]


best_osop.Code("Tikz")
best_osop.Code("C")

