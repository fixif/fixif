from fipogen.LTI import dSS, dTF, iter_random_dSS, iter_random_dTF, iter_random_Butter, to_dTFmp, sub_dSSmp, to_dSSmp, random_dSS
from fipogen.SIF import *
from fipogen.func_aux import *

import numpy as np
import mpmath as mpm

import sollya



def get_TFmp(S, prec):
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


	T_b, T_a = to_dTFmp(S.A, S.B, S.C, S.D, prec)

	T_A, T_B, T_C, T_D = to_dSSmp(T_b, T_a)
	T_Adbl, T_Bdbl, T_Cdbl, T_Ddbl = to_dSSmp(T_b, T_a, mpmatrices=False)

	dSS_Tdbl = dSS(T_Adbl, T_Bdbl, T_Cdbl, T_Ddbl)

	#compute the difference between S and dSS_T

	dSS_delta_dbl = S.sub_dSS(dSS_Tdbl)

	delta_A, delta_B, delta_C, delta_D = sub_dSSmp(python2mpf_matrix(S.A),python2mpf_matrix(S.B), python2mpf_matrix(S.C), python2mpf_matrix(S.D), T_A, T_B, T_C, T_D)

	Theta = dSS_delta_dbl.WCPG()


	return T_b, T_a, Theta



s = sollya.SollyaObject('123')
print s
S = random_dSS(5, 1, 1)
#for prec in range(50, 1000, 50):
#	b, a, theta = get_TFmp(S, prec)
#	print 'Transfer function: \n \t num: %s \n \t den: %s \nTheta: %s\n'% (repr(b.transpose()), repr(a.transpose()), repr(theta))

