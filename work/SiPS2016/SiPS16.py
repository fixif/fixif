
from fipogen.LTI import Butter
from fipogen.Structures.Simulink import importSimulink
from fipogen.Structures import LWDF, DFII, State_Space
from numpy import vectorize,ones
from numpy import mat, count_nonzero
from math import log,ceil
from fipogen.LTI import random_dSS
#import matplotlib.pyplot as plt
#from matplotlib2tikz import save as tikz_save

import os

# set the path for matplotlib to use latex
os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'


def ceil2(x):
	return 2**ceil(log(x,2))
vceil2 = vectorize(ceil2)

#inputs
F = Butter(3,0.2, name='SiPS16')
ubar = 5.25


#Direct Form IIt from Simulink
const1 = {'-a1':-F.dTF.den[0,1], '-a2':-F.dTF.den[0,2], '-a3':-F.dTF.den[0,3], 'b0':F.dTF.num[0,0], 'b1':F.dTF.num[0,1], 'b2':F.dTF.num[0,2], 'b3':F.dTF.num[0,3] }
R1 = importSimulink("DFIItvertical.slx", constants=const1)

#R1 = DFII.makeRealization(F, transposed=True)


# LWDF (using matlab/LWDFtoolbox)
#R2bis = LWDF.makeRealization(F)
const2 = {'g1' : 0.4905, 'g2' : 0.4543, 'g3' : 0.1910}
R2 = importSimulink("LWDF_butter3.slx", constants=const2)



wl = range(4,33)
deltay = lambda R,w: float( 2 * mat(R.Hepsilon.WCPG()) * mat(vceil2( R.Hu.WCPG()*ubar)) *2**-w )		#SISO
dy1 = [ deltay(R1,w) for w in wl ]
dy2 = [ deltay(R2,w) for w in wl ]


def wmin( R, epsilon):
	return ceil( log( mat(R.Hepsilon.WCPG()) * mat(vceil2( R.Hu.WCPG()*ubar))/epsilon ,2)  ) + 1


poids= lambda R,w: [x*(count_nonzero(R.dZ)) for x in w]

print( 'R1: wmin=%d'%wmin(R1,1e-2))
print( 'R2: wmin=%d'%wmin(R2,1e-2))



