

import numpy
import mpmath
import sollya


#from fipogen.LTI import dTFmp, dSSmp, dSS, dTF, Gabarit

from fipogen.LTI import dTFmp, dSSmp, Filter
from fipogen.SIF import SIF
from fipogen.LTI import Gabarit
from fipogen.Structures import State_Space, DFI, DFII, rhoDFII



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



	# --------- get the exact dSSmp corresponding to this realization

	prec = 100
	S = R.to_dSSexact()
	H_hat = S.to_dTFmp(prec)

	# find a margin where H_hat fits
	margin = g.findMinimumMargin(H_hat)

	#
	if margin==0:
		wcpg_margin = 10**(1e-3+g.maxGain()/20)-10**(g.maxGain()/20)
	else:
		wcpg_margin = margin

	# --------- compute the exact dSS corresponding to H
	S_H = H_hat.to_dSSmp()
	S_delta = S - S_H
	W = list(S_delta.WCPGmp(wcpg_margin/8))[0] + wcpg_margin/8
	if W>wcpg_margin:
		prec += 100





	#
	#
	# prec = 100
	# prec_increase_ntimes = 3  # number of times we will try to increase the precision of H computation
	# wcpg_prec_increase_times = 3
	# H_final_prec = prec
	# check_gabarit = False
	#
	# # -------- We check at first if H passes or not without margins or WCPG
	# # -------- If it passes, we need to set the bound for the WCPG.
	# # -------- I propose to set this bound to 2^q
	# #--------- If it does not work, we will try to deduce the least dBmargin
	# print ('\n-------> Trying to check if the transfer function H checks the initial gabarit...')
	# H = S.to_dTFmp(prec)
	# if g.check_dTF(H):
	# 	# --------- compute the exact dSS corresponding to H
	# 	S_H = H.to_dSSmp()
	# 	# --------- compute S_delta = S - S_H
	# 	S_delta = S - S_H
	# 	# set the initial precision for the WCPG computation to at least 2^(q+4)
	# 	wcpg_eps = max(64, q + 8)
	# 	check_for_wcpg = False
	# 	i = 0
	# 	while i < wcpg_prec_increase_times and not check_for_wcpg:
	# 		# --------- compute the WCPG of the S_delta with error bound 2**-eps
	# 		W = S_delta.WCPGmp(wcpg_eps)
	# 		check_for_wcpg = (W[0] + 2 ** (-wcpg_eps) < 2^q)
	# 		wcpg_eps = wcpg_eps * 2
	#
	# 	if not check_for_wcpg:
	# 		print ('\n-------> Tried computing the wcpg %d times but still did not work. Now will try to increase the dBmargin.') % wcpg_prec_increase_times
	# 	else:
	# 		if g.check_dTF(H, bound=W[0] + 2 ** (-wcpg_eps), dBmargin=0):
	# 			return (True, 0)
	#
	# # --------- If H does not pass the check after quantization,
	# # --------- we try to compute the least dBmargin_power such that the check of the transfer function H
	# # --------- passes with  dBmargin = 10 ** dBmargin_power.
	# # --------- Then, we compute the WCPG(S_H) with absolute error < 10 ** (dBmargin_power - 4)
	# # ---------(I don't think that is right, we need to have a relative bound which depends on the constraints ?)
	# print ('\n-------> Looking for the least dBmargin s.t. at least for the transfer function H the specifications checks out...')
	# dBmargin_power = 0
	# check_for_H = g.check_dTF(H, bound=0, dBmargin=10 ** dBmargin_power)
	# if not check_for_H:
	# 	raise ValueError('\n-------> We are in a very extreme case when we have dBmargin > 1. For the moment, I do not how to proceed')
	#
	# while check_for_H:
	# 	dBmargin_power -= 1
	# 	check_for_H = g.check_dTF(H, bound=0, dBmargin=10 ** dBmargin_power)
	#
	# 	#	 --------- For the first time the check does not pass we try to increase the precision prec_increase_ntimes times.
	# 	#    --------- We modify the H_final_prec (on which the WCPG computation depends).
	# 	i = 1
	# 	while i < prec_increase_ntimes and not check_for_H:
	# 		print('\n-------> Trying to increase the precision of the computation of H')
	# 		i += 1
	# 		H_final_prec = H_final_prec * 2
	# 		H = S.to_dTFmp(prec * 2)
	# 		check_for_H = g.check_dTF(H, bound=0, dBmargin=10 ** dBmargin_power)
	#
	# 	# --------- If we tried and still no luck, we reset H_final_prec to prec bits, with wich the previous step worked
	# 	# --------- Else if it worked with H_final_prec we update variable prec and try to dicrease the dBmargin_power again
	# 	if not check_for_H:
	# 		H_final_prec = prec
	# 	else:
	# 		prec = H_final_prec
	# 		H_final_prec = prec
	#
	# print '\n-------> Minimal dBmargin for which the check of H (with prec=%d) passes: 10 ** %d = %s\n' % (H_final_prec, dBmargin_power + 1, 10 ** (dBmargin_power + 1))
	# #print '\n-------> The final precision of the H computation must be at least %d bits. \n' % H_final_prec
	#
	# # -------- Here, we know that with dBmargin =  10 ** dBmargin_power, transfer function H,
	# # -------- computed with H_final_prec bits, checks the gabarit. Now, we check it with the WCPG.
	# # -------- If it does not work, we increase the WCPG precision several times.
	# # -------- If this does not help, we increase the dBmargin
	#
	# while not check_gabarit and dBmargin_power < 1:
	# 	dBmargin_power = dBmargin_power + 1
	# 	# --------- compute the exact dSS corresponding to H
	# 	S_H = H.to_dSSmp()
	# 	# --------- compute S_delta = S - S_H
	# 	S_delta = S - S_H
	# 	# set the initial precision for the WCPG computation to eps=log2(bound) + 2
	# 	wcpg_eps = max(64, sollya.log2(10 ** dBmargin_power) + 4)
	# 	check_for_wcpg = False
	# 	i = 0
	# 	while i < wcpg_prec_increase_times and not check_for_wcpg:
	# 		# --------- compute the WCPG of the S_delta with error bound 2**-eps
	# 		W = S_delta.WCPGmp(wcpg_eps)
	# 		check_for_wcpg = (W[0] + 2 ** (-wcpg_eps) < 10 ** dBmargin_power)
	# 		wcpg_eps = wcpg_eps * 2
	# 		i+=1
	#
	# 	if not check_for_wcpg:
	# 		print ('\n-------> Tried computing the wcpg %d times but still did not work. Increase the dBmargin.') % wcpg_prec_increase_times
	# 	else:
	# 		check_gabarit = g.check_dTF(H, bound=W[0] + 2 ** (-wcpg_eps/2), dBmargin=10 ** dBmargin_power)
	#
	# if check_gabarit:
	# 	return (True, 10**dBmargin_power)
	# else:
	# 	raise ValueError('Could not check the gabarit, the dBmargin is larger than 10')
	#




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
g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -20])

# --------- build the realization we want to check
q=25
R = buildApproxRealization(g, q, State_Space)
#R = buildApproxRealization(g, q, rhoDFII)


CheckIfRealizationInGabarit(g, R)
























