#coding=utf8
#!usr/bin/env python

from sys import path
path.append('/Users/benoitlopez/Documents/Thèse/fipogen/start/fipogen-v1')


import LTI
import SIF

from oSoP.Constant import Constant

from scipy.io import loadmat
import numpy as np


D=loadmat("scripts/benoit_11_2015/ARITH23_BLTH_ex.mat")

Z=[D["SIF_DFI"][0][0][i] for i in range(4,13)]
S = SIF.SIF(Z)
print(LTI.dSS(S._AZ,S._BZ,S._CZ,S._DZ).WCPG)