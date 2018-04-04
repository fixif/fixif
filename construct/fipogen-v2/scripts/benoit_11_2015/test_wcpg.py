#coding=utf8
#!usr/bin/env python

import sys, os
sys.path.insert(0, os.path.abspath('.'))

import LTI
import SIF

from scipy.io import loadmat
import numpy as np



D=loadmat("scripts/benoit_11_2015/ARITH23_BLTH_ex.mat")

Z=[D["SIF_SS"][0][0][i] for i in range(4,13)]
S=SIF.SIF(Z)

print "###  WCPG H  ###"
wcpgH = LTI.dSS(S._AZ,S._BZ,S._CZ,S._DZ).WCPG
print wcpgH

N1 = np.bmat(np.r_[S.invJ*S.M,S._AZ,S._CZ])
N2 = np.bmat(np.r_[S.invJ*S.N,S._BZ,S._DZ])

print "\n###  WCPG Hu  ###"

print(N1)
for i in range(N1.shape[0]):
	for j in range(N1.shape[1]):
		print N1[i,j]
	print ""
print(N2)
for i in range(N2.shape[0]):
	print N2[i,0]

# with the print function calling the variables the bug is not there
# maybe the C wrapper needs to use more INCREF on incoming variables so that those
# are not trashed by the python VM during the call, either by
# the python program or before entering into wrapper WCPG routine
# (which should not be the case, as we use intermediate variables

wcpgHu = LTI.dSS(S._AZ,S._BZ,N1,N2).WCPG
print wcpgHu