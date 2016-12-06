

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
S = Rq.dSSexact()


pp = 10
prec = 100
check_for_H = False
check_gabarit = False

while pp > 0 and not check_gabarit:
	bound = 10 ** (-pp)
	while prec < 500:
		H = S.to_dTFmp(prec)
		check_for_H = g.check_dTF(H)
		if check_for_H:
			break
		prec = prec + 100

	if check_for_H:

		# --------- compute the exact dSS corresponding to H
		S_H = H.to_dSSmp()
		# --------- compute S_delta = S - S_H
		S_delta = S - S_H
		# set the initial precision for the WCPG computation to eps=log2(bound) + 2
		eps = max(64, log2(bound) + 2)
		# --------- compute the WCPG of the S_delta with error bound 2**-eps
		W = S_delta.WCPGmp(eps)

		if W[0] + 2 ** (-eps) > bound:
			print 'WCPG is too large...'
		else:
			check_gabarit = g.check_dTF(H, W[0] + 2 ** (-eps))

	pp = pp - 2























