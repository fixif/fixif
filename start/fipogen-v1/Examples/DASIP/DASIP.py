# Exemples pour DASIP-12

from Ordered_SoP import *
from QADoSoP import QAD_oSop_Generator
from FPR import FPR
from scipy.signal.filter_design import butter
import cPickle
from control import TransferFunction
from control.matlab import tf
from scipy.signal import dimpulse
from scipy.linalg import norm

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
#
#list_name_var = [ 'u[n]', 'u[n-1]', 'u[n-2]', 'u[n-3]','u[n-4]', 'y[n-1]', 'y[n-2]', 'y[n-3]', 'y[n-4]']
list_name_var = [ 'u[n]', 'u[n-1]', 'u[n-2]', 'u[n-3]', 'y[n-1]', 'y[n-2]', 'y[n-3]']
#list_name_var = [ 'u[n]', 'u[n-1]', 'u[n-2]',  'y[n-1]', 'y[n-2]']
#list_name_var = [ 'x0', 'x1', 'x2', 'x3', 'x4']
N=3
list_fpr_var = FPR(beta = 8, gamma=3)
b,a = butter(N,0.166)
list_cst = list(b)+map(lambda x:-x,list(a))[1:]
list_beta_cst = 8
list_beta_mult = 16
list_beta_add = 16
fpr_final = FPR(beta = 8, alpha = 8)
RBAM = "RBM"
	
nb=0
LT=[]
for L in QAD_oSop_Generator(list_name_var, list_fpr_var, list_cst, list_beta_cst, list_beta_mult,list_beta_add, fpr_final, RBAM):
	nb+=1
	L.Calc_FPR_Noise(alfix=True)
	if nb%1000 == 0:
		print nb
	#p,nh = p_norm_delta_h(L)
	p = 115.5106973742*L._Top._total_noise[1]+(24.5987341*L._Top._total_noise[0])**2
	LT.append((L,p,L.height()))

LT.sort(key = lambda x: x[2])
LT[0][0].Code("Tikz")
LT[-1][0].Code("Tikz")
print p_norm_delta_h(LT[-1][0])

#print len(LminP)
#print min(pList),max(pList)
#print nb
#for L in LminP:
	#L.Code("Tikz")


#print LminP.Code("fix")
#LminP.Code("Tikz")

