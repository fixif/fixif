

import numpy
import mpmath
import sollya

from sollya import *

#from fipogen.LTI import dTFmp, dSSmp, dSS, dTF, Gabarit

from fipogen.LTI import dTFmp, dSSmp, Filter
from fipogen.SIF import SIF
from fipogen.LTI import Gabarit
from fipogen.Structures import LWDF, State_Space, DFI, DFII, rhoDFII



# --------- set a Gabarit
#g = Gabarit(.....)
g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])


# --------- transform the gabarit to the TF
# TF = g.to_TF(....)

TF = g.to_dTF(ftype='butter', method='matlab')

# --------- get Realizations for this TF
F = Filter(tf=TF, name='sollya_test_filter')

R = State_Space(F)
#for R in iterAllRealizations():

	# --------- quantize the realization coefficients
q = 16
Rq = R.quantize(q, rnd='n')

# --------- get the exact dSSmp corresponding to this realization
#S = Rq.dSS.to_dSSmp() #method of SIF!!
S = Rq.dSSexact()
# --------- set the bound for which we compute the gabarit
pp = 10
bound = 10 ** (-pp)

# --------- set the initial precision for the TF computation
prec = max(100, numpy.log2(bound))

# while True:

# while True:

# --------- compute the transfer function corresponding to the dSS
H = S.to_dTFmp(prec)

# --------- compute the exact dSS corresponding to H
S_H = H.to_dSSmp()

# --------- compute S_delta = S - S_H
S_delta = S - S_H

# set the initial precision for the WCPG computation to eps=log2(bound) + 2
eps = max(64, log2(bound) + 2)

# while True:
# --------- compute the WCPG of the S_delta with error bound 2**-eps
W = S_delta.WCPGmp(eps)

# --------- if WCPG + eps > bound then we need to either increase the precision fo the WCPG computation or
#                                                increase the precision of the TF computation

if W[0] + 2 ** (-eps) > bound:
	print 'ooops'
else:
	#g.check_dTF(TF)
	#g.check_dTF(H.to_dTF(),  W[0] + 2 ** (-eps))
	g.check_dTF(H,  W[0] + 2 ** (-eps))
	#g.check_dTF(TF,  W[0] + 2 ** (-eps))

print 'lolololo'


















