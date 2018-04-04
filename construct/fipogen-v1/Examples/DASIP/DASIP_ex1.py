# Exemples pour DASIP-12

from FxP.oSoP_Generator import oSoP_Generator,oSoP_Generator2
from FxP.FPR import FPR
from FxP.Variable import Variable
from FxP.Constant import Constant
from scipy.signal.filter_design import butter
from control import TransferFunction
from control.matlab import tf
from scipy.signal import dimpulse
from scipy.linalg import norm
from copy import deepcopy


def p_norm_delta_h(osop):
	P = 115.5106973742*osop._Top._total_noise[1]+(24.5987341*osop._Top._total_noise[0])**2
	qList = osop.quantized()
	bq = qList[0:N+1]
	aq = map(lambda x:-x,qList[N+1:])
	h = tf(b,a)
	hq = tf(bq,[1]+aq)
	delta_h = h-hq
	Norm =  norm(dimpulse((delta_h.num[0][0],delta_h.den[0][0],1))[1])
	return P, Norm

N=3
Nb = 16

list_name_var=['u[n]']+['u[n-%d]'%(i) for i in range(1,N+1)]+['y[n-%d]'%(i) for i in range(1,N+1)]
#list_name_var_code = ['u%d'%(i) for i in range(0,N+1)]+['y%d'%(i) for i in range(1,N+1)]
list_fpr_var = FPR(beta = Nb, alpha = 5)
#list_inter_var = Variable(fpr=list_fpr_var)
b,a = butter(N,0.166)
#print b,a
list_cst = list(b)+map(lambda x:-x,list(a))[1:]
list_beta_cst = Nb
list_beta_mult = 2*Nb
beta_add = 2*Nb
fpr_final = FPR(beta = 4*Nb, alpha = 15)
#var_final = Variable(fpr=fpr_final)
RBAM = "RAM"




nb=0
LT=[]
best_osop = None
best_mean = 10000
#for L in oSoP_Generator(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, fpr_final.alpha, alfix = False,plus = False, RndOff = RBAM):
for L in oSoP_Generator2(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult, beta_add, fpr_final, fpr_final.alpha, alfix = False,plus = False, RndOff = RBAM):
	nb+=1
	#if nb%10000==0:
		#print nb
	if L._Top._total_noise[0] <= best_mean:
		if L._Top._total_noise[0] < best_mean:
			LT=[]
		LT.append(L)
		best_mean = L._Top._total_noise[0]
		best_osop = L



#h = LT[0].height()
#for L in LT:
	#if L.height() <=h:
		#h=L.height()
		#best_osop = L
		
		
		
		
print best_mean
print best_osop._Top._total_noise[1]

#print best_osop._Top._var_result.FPR, best_osop._Top._var_result.values
best_osop.Code("Tikz")
#best_osop.Code("C")

