

import numpy
import mpmath
import sollya


#from fipogen.LTI import dTFmp, dSSmp, dSS, dTF, Gabarit

from fipogen.LTI import dTFmp, dSSmp, Filter
from fipogen.SIF import SIF
from fipogen.LTI import Gabarit
from fipogen.Structures import State_Space, DFI, DFII, rhoDFII


def ComputeWCPGMargin(g, margin):
	"""
	This function computes the margin for the WCPG
	as a function of the minimal margin for the TF.

	In case when margin is equal to zero, we set the
	WCPG margin to be
		wcpg_margin = 10 ** (p + g.maxGain() / 20) - 10 ** (g.maxGain() / 20)

	where p = 10^(-3i) and i inidicates number of iterations that we have passed
	while computing the WCPG with margin==0



	Parameters
	----------
	margin - a scalar >=0
	i - a scalar, i >= 1

	Returns
	-------
	wcpg_margin
	"""

	if margin == 0:
		return 10 ** (1e-5 + g.maxGain() / 20) - 10 ** (g.maxGain() / 20)
	else:
		return margin

def ComputeTheta(S, H_hat, g, margin):
	"""
	For a given state-spae S and an approximation on its
	transfer function H_hat, this function computes a
	correction term Theta, such that the exact transfer
	function H is s.t.

	|H(z)| <= |H_hat(z)| + Theta

	This function verifies whether |Theta| < margin
	Parameter i inidicates the number of times this function
	has been called since the beginning of the outer verification.
	(when margin=0 parameter i > 1 can increase the accuracy of the WCPG)

	Parameters
	----------
	S       - dSSmp object
	H_hat   - dTFmp object
	margin  - sollyaObject
	i       - strictly positive integer

	Returns
	-------
	boolean: do we have enough space for WCPG or not?
	sollyaObject - a scalar value Theta>0

	"""

	# compute a margin for the WCPG
	wcpg_margin = ComputeWCPGMargin(g,margin)
	wcpg_margin_ini = wcpg_margin

	# compute the exact dSS corresponding to H
	S_H = H_hat.to_dSSmp()

	S_delta = S - S_H

	# compute WCPG while it doesn't make sense (wcpgm_margin is not too big compared to WCPG value)
	WCPG = S_delta.WCPGmp( wcpg_margin / 8 )[0]
	while WCPG < wcpg_margin / 16 and wcpg_margin> wcpg_margin_ini*1e-15:
		wcpg_margin /= 10
		#print( 'WCPG_margin='+str(wcpg_margin) )
		#print( 'WCPG='+str(WCPG) )
		WCPG = S_delta.WCPGmp(wcpg_margin / 8)[0]

	W = WCPG + wcpg_margin / 8
	if W >= max(margin, wcpg_margin):
		if W >= g.maxGain()/10.0:
			raise ValueError('WCPG is larger than g.maxGain()/10.0')
		return (False, W)
	else:
		return (True, W)




def CheckIfRealizationInGabarit(g, R):
	"""
	Given the gabarit object g and a realization R,
	this function checks whether the realization verifies the
	initial gabarit specifications g.

	If the filter does not verify the specifications g, the least
	(with a step equal to a power of 10) margin dBmargin such that
	the initial specifications enlarged by dBmargin are verified.

	Parameters
	----------
	g - gabarit
	q - quantization factor, a positive integer

	Returns
	-------
	(bool, dBmargin_power) - a boolean indicating whether the specifications are fulfilled
							and a float dBmargin

	"""

	prec = 100
	S = R.to_dSSexact()

	#do the first try
	H_hat = S.to_dTFmp(prec)
	margin = g.findMinimumMargin(H_hat)

	while prec < 1500:

		ThetaCheck, Theta = ComputeTheta(S, H_hat, g, abs(margin))

		# if margin was <=0, then we need to check with narrower margin
		# otherwise, we check with a wider margin
		verification_margin = margin-Theta

		if ThetaCheck:
			check, res = g.check_dTF(H_hat, margin=verification_margin)
			if check:
				margin = sollya.max(0, margin - Theta)
				marginDB = abs(sollya.log10(10**(g.maxGain()/20) + margin))
				return (True, sollya.round( margin, 53, sollya.RU), sollya.round( marginDB, 53, sollya.RU) , res)
			else:
				margin = max( margin+Theta, g.findMinimumMargin(H_hat, initMargin=verification_margin) )
		else:
			margin = g.findMinimumMargin(H_hat, initMargin=verification_margin)

		prec += prec
		H_hat = S.to_dTFmp(prec)


	return (False, None, None)


def buildApproxRealization(g, wl, struct):
	"""
	Returns a realization that is not too far to satisfy the gabarit
	(we start with a transfer function that should, according to matlab or scipy, satisfy it,
	build a realization with the structure struct
	and then we quantize its coefficients)

	Parameters:
	- g: Gabarit
	- wl: wordlength
	- struct: struture used
	"""
	# transform the gabarit into a transfer function
	TF = g.to_dTF(ftype='butter', method='matlab')
	# get Realizations for this TF
	F = Filter(tf=TF, name='sollya_test_filter')
	# make a realization, with structure struct
	R = struct(F)
	# quantize the realization coefficients
	return R.quantize(wl)





# --------- set a Gabarit
#g = Gabarit(48000,[ (0,9600), (12000,None) ], [-20, (0,-1)])
#g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -20])
#g =  Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [-20, (0, -1), -20])
#g =  Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [(0, -1), -20, (0, -1)])


# --------- build the realization we want to check
#q=64
#R = buildApproxRealization(g, q, State_Space)
#R = buildApproxRealization(g, q, rhoDFII)


#check, margin = CheckIfRealizationInGabarit(g, R)

#if check:
#	print ('------> Realization is in Gabarit with margin = %e') % margin
#else:
#	print ('------> Something went wrong! ...')
























