from FPR import FPR
from random import randint
from math import floor,log

M = 10
L = [FPR(beta = randint(4,10),gamma = randint(0,10)) for i in range(M)]
for l in L :
	print l
amax = -10
for x in L:
	if x._alpha > amax :
		amax = x._alpha
fpr_final = FPR(beta = 8, alpha = amax+1)
print "Final "+repr(fpr_final)
X=[]
for x in L :
	if x._gamma > fpr_final._gamma :
		X.append(x)
N = len(X)

d = int(floor(log(N-1,2)))+1
for x in X:
	if fpr_final._gamma + d -1 > - x._alpha:
		x._gamma = fpr_final._gamma + d
	else :
		X.remove(x)

k=0
ret=0
s=1
for i in range(fpr_final._gamma + d,fpr_final._gamma,-1):
	k = ret
	for x in X:
		if (i <= x._gamma) and (i >= x._gamma - x._beta+1):
			k += 1
	s = k%2
	ret = k/2

for x in X :
	print x
print ret
	
	