#coding=utf8
#!usr/bin/env python

from sys import path


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
wcpgHu = LTI.dSS(S._AZ,S._BZ,N1,N2).WCPG
print wcpgHu