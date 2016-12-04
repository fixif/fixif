

import numpy
import mpmath
import sollya

from sollya import *

#from fipogen.LTI import dTFmp, dSSmp, dSS, dTF, Gabarit

from fipogen.LTI import dTFmp, dSSmp
from fipogen.SIF import SIF, Realization



def blablabla(S, prec):
	"""
	Given a dSS system S (we consider that dSS objest has exact state-space matrices),
	this function computes a bound on the absolute value of its transfer function:
	 |H(z)| <= |T(z)| + Theta,

	 where
	    - T(z) is an approximation on the transfer function of dSS (computed in multiple precision
	 but still not exact)
	    - Theta is the WCPG <<delta_dSS>> of the system delta_dSS, which is the difference between
	    the exact initial system dSS and the exact system dSS_T, whcih corresponds to the computed transfer function T(z)

	Parameters
	----------
	S

	Returns
	-------
	b, a - MP matrices holding the numerator and denominator of the transfer function T(z)
	Theta - scalar
	"""



# --------- set a Gabarit
#g = Gabarit(.....)

# --------- transform the gabarit to the TF
# TF = g.to_TF(....)


# --------- get Realizations for this TF

#for R in iterAllRealizations():

	# --------- quantize the realization coefficients
	# Rq = R.quantizeMatrices(q = 16)

	# --------- get the exact dSSmp corresponding to this realization
	#S = Rq.SIF.to_dSSmp()

	# --------- set the bound for which we compute the gabarit
	#x = 10
	#bound = 10**sollyaObject(-x)

	# --------- set the initial precision for the TF computation
	#prec = max(100, log2(bound))

	#while True:

		#while True:

			# --------- compute the transfer function corresponding to the dSS
			#H = S.to_dTFmp(prec)

			# --------- compute the exact dSS corresponding to H
			#S_H = H.to_dSSmp()

			# --------- compute S_delta = S - S_H
			#S_delta = S - S_H

			# set the initial precision for the WCPG computation to eps=log2(bound) + 2
			# eps = max(64, log2(bound) + 2)

			#while True:
				# --------- compute the WCPG of the S_delta with error bound 2**-eps
				#W = S_delta.WCPGmp(eps)

				# --------- if WCPG + eps > bound then we need to either increase the precision fo the WCPG computation or
				#                                                increase the precision of the TF computation

				#if W[0] + 2**(-eps) > bound:














