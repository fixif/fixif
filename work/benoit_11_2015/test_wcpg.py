#coding=utf8
#!usr/bin/env python


from LTI import dSS
from SIF import SIF

from scipy.io import loadmat
import numpy as np



D=loadmat("../work/benoit_11_2015/ARITH23_BLTH_ex.mat")

Z=[D["SIF_SS"][0][0][i] for i in range(4,13)]
S=SIF(Z)

print "###  WCPG H  ###"
wcpgH = S.dSS.WCPG()
print wcpgH

N1 = np.bmat(np.r_[ S.invJ*S.M, S.AZ, S.CZ ])
N2 = np.bmat(np.r_[ S.invJ*S.N, S.BZ, S.DZ ])

print "\n###  WCPG Hu  ###"

Hu = dSS( S.AZ,S.BZ, N1, N2)
print Hu.WCPG()