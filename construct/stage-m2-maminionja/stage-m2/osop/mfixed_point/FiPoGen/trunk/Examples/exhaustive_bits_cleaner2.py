from matplotlib import pylab
import numpy as np
from random import randint
from math import floor,log, ceil

from scipy.stats import normaltest

length=10
sample = 150

def somme(L):
	s=0
	for l in L:
		s += l
	return s

def somme_arrondie(L,d):
	s=0
	for l in L:
		s += int(round(l*2**-(length-2-d)))
	return s

def somme_tronc(L,d):
	s=0
	for l in L:
		s += int(floor(l*2**-(length-2-d)))
	return s


def test(nb_exec, N, delta):
	Res = []
	test_ex =[]
	test_ar=[]
	test_ex2 =[]
	test_ar2=[]
	for i in range(nb_exec):
		Nbs = [randint(2**(length-1), 2**length-1) for i in range(N)]

		s1 = somme(Nbs)
		s1_ex = s1*2**(-length+2)
		s1 = int(round(s1_ex))

		s2 = somme_arrondie(Nbs,delta)
		s2 = int(floor( (s2+2**(delta-1))*2**-delta ))

		Res.append((s2-s1_ex))

		if s2-s1_ex > 0.5:
			test_ex.append(s2-s1_ex)
		if s2-s1 >0:
			test_ar.append(s2-s1)
		if s2-s1_ex <= -0.5:
			test_ex2.append(s2-s1_ex)
		if s2-s1 <0:
			test_ar2.append(s2-s1)

	m = min(Res)
	M = max(Res)
	moy = np.mean(Res)
	mini = -0.5-N*2**(-delta-1)+2**(-delta)+N*2**(-length+2)
	maxi = 0.5+N*2**(-delta-1)

	print "Plus proche : \n  - attendue : [%g , %g]\n  - observe : [%g , %g] , moyenne : %g\n"%(mini,maxi,m,M, moy)
	return Res

def test_tronc(nb_exec, N, delta):
	Res = []
	test_ex =[]
	test_ar=[]
	for i in range(nb_exec):
		Nbs = [randint(2**(length-1), 2**length-1) for i in range(N)]

		s1 = somme(Nbs)
		s1_ex = s1*2**(-length+2)
		s1 = int(round(s1_ex))

		s2 = somme_tronc(Nbs,delta)
		s2 = int(floor( (s2+2**(delta-1))*2**-delta ))

		Res.append((s2-s1_ex))

		if s2-s1_ex <= -0.5:
			test_ex.append(s2-s1_ex)
		if s2-s1 <0:
			test_ar.append(s2-s1)
#		if s1_ex-s2 < 0:
#			Res = Nbs
#			break
	m = min(Res)
	M = max(Res)
	moy = np.mean(Res)
	print "troncature : \n  - attendue : [%g , %g]\n  - observe : [%g , %g] , moyenne : %g"%(-0.5-N*2**(-delta)+2**(-delta)+N*2**(-length+2),0.5,m,M, moy)
	return Res

N=randint(5,20)
L=test(500000,N, int(ceil(log(N,2)))+1)
print normaltest(L)
#m1 = min(L)
#M1 = max(L)
#moy1 = np.mean(L)

#n1,bins1,patches1=pylab.hist(L,sample,normed=True,histtype='step',label='plus proche')


L=test_tronc(500000,N, int(ceil(log(N,2)))+2)
#print L
#n2,bins2,patches2=pylab.hist(L,sample,normed=True,histtype='step',label='troncature')
#m2 = min(L)
#M2 = max(L)
#moy2 = np.mean(L)

#pylab.axis([1.1*min([m1,m2]), 1.1*max([M1,M2]), 0, max(n1+n2)])
#pylab.legend()

#pylab.show()