#import sollya

_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import pytest


from fixif.LTI import dSS, Butter, dTF
#from fixif.SIF import Realization, Realization_FxP
from numpy import matrix as mat, zeros, eye, empty, float64
import numpy as np
from numpy import all
import time

import mpmath as mp

from fixif.func_aux import write_matrix_mpf, write_matrix_hex, mpf_matrix_to_sollya, mpf_get_representation, \
	python2mpf_matrix, sollya_matrix_to_numpy

from fixif.Structures import LWDF, DFII, State_Space, DFI

from fixif.Structures import iterAllRealizations, iterAllRealizationsRandomFilter
from fixif.LTI import Filter, iter_random_Filter, iter_random_dSS, random_Filter, random_dSS, dSS
#from scipy.weave import inline

# from func_aux.get_data import get_data
# from func_aux.MtlbHelper import MtlbHelper

import mpmath
from mpmath import *
from fixif.func_aux import mpf_poly_mult
from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose





def test_computeMSBSIF(nSimulations=1000):

	sollya.settings.display = sollya.binary
	nu = 1
	ny = 1
	nx = 5
	F = random_Filter(nx, ny, nu, seed=5)
	#F = Butter(5, 1.2)
	#SS = LWDF.makeRealization(F)
	SS = State_Space.makeRealization(F)


	#a hardcoded example
	#A = np.matrix([[-0.1721,  0.004845,    0.2187],[0.004845,  -0.08567,   -0.1096], [0.2187,   -0.1096,   -0.4978]])
	#B = np.matrix([[1.533], [0], [0]])
	#C = np.matrix([-0.2256,    1.117,   -1.089])
	#D = np.matrix([0.03256])
	#F = Filter(A=A,B=B,C=C,D=D)
	#SS = State_Space.makeRealization(F)



	u_bar = np.bmat([np.ones([1, nu])])
	l_y_out = -15
	#msb_u = np.bmat([np.zeros([1, SS.q])])
	#lsb_u = -15 * np.bmat([np.ones([1, SS.q])])
	msb_u = 0
	lsb_u = -15

	msb = SS._compute_MSB(u_bar)
	lsb, error_budget_y = SS._compute_LSB(l_y_out)
	Y, N = mpf_get_representation(mpmath.mpf(error_budget_y))
	error_budget_y = sollya.SollyaObject(Y) * 2**sollya.SollyaObject(N)

	lsb_t = [lsb[0, i] for i in range(0, SS.l)]
	lsb_x = [lsb[0, i] for i in range(SS.l, SS.l + SS.n)]
	lsb_y = [lsb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]

	msb_ext = SS.compute_MSB_allvar_extended(u_bar, lsb_t, lsb_x, lsb_y)
	if (msb != msb_ext).any():
		print('MSB computed with taking into account the propagation of the error due to the format (msb, lsb) differs from the initial format. Changing MSBs.\n')
		print('new MSBs:')
		msb = msb_ext
		print(msb)

	msb_t = [msb[0, i] for i in range(0, SS.l)]
	msb_x = [msb[0, i] for i in range(SS.l, SS.l + SS.n)]
	msb_y = [msb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]

	fileID = './SIF-' + time.strftime("%d%m%Y-%H%M%S")
	filename = fileID + '.txt'
	with open(filename, 'a') as f_handle:
		f_handle.write('%d\n%d\n%d\n%d\n' % (SS.q, SS.l, SS.n, SS.p))
		#for i in range(0, SS.q):
		f_handle.write('%d %d\n' % (msb_u, lsb_u))
		for i in range(0, SS.l):
			f_handle.write('%d %d\n' % (msb_t[i], lsb_t[i]))
		for i in range(0, SS.n):
			f_handle.write('%d %d\n' % (msb_x[i], lsb_x[i]))
		for i in range(0, SS.p):
			f_handle.write('%d %d %s\n' % (msb_y[i], l_y_out, str(error_budget_y).replace(" ", "").replace("\n", "")))
		#f_handle.write('%s\n' % str(error_budget_y))


		#write_matrix_hex(f_handle, SS.Z, ' ')
		Z_sollya, Zrows, Zcols  = mpf_matrix_to_sollya(python2mpf_matrix(SS.Z))

		for i in range(0, Zrows):
			for j in range(0, Zcols):
				f_handle.write('%s' % str(Z_sollya[i + j * Zcols]).replace(" ", "").replace("\n", ""))
				f_handle.write(' ')
			f_handle.write('\n')

	f_handle.close()

	print('Filter: \n')
	print(SS)
	print('y_out was initially set to: %d\n' %l_y_out)
	print('LSBs:\n')
	print(lsb)
	print('MSBs:\n')
	print(msb)


	u = np.random.rand(1, nSimulations)

	# quantize the simulations to the format lsb_u bits
	u_sollya = mpf_matrix_to_sollya(mpmath.matrix([mpmath.nint(mp.mpf(u[0,i]) * 2 ** -lsb_u) / 2 ** -lsb_u for i in range(0, nSimulations)]))[0]
	u_quantized = sollya_matrix_to_numpy(u_sollya, 1, nSimulations)


	# perform simulations either in exact or rounded

	y_simulated_sollya_exact = SS.to_dSSexact().simulate_rounded(u_quantized, prec=53)
	y_simulated_sollya = mpf_matrix_to_sollya(SS.to_dSSexact().simulate(u_quantized, exact=True))[0]


	filename = fileID + 'simulation' + '.txt'
	with open(filename, 'a') as f_handle:
		f_handle.write('%d\n' % nSimulations)
		for i in range(0,nSimulations):
			#for j in range (0, nu):
			f_handle.write('%s' % str(u_sollya[i]).replace(" ", "").replace("\n", ""))
			f_handle.write('\n')
			#for j in range(0,ny):
			f_handle.write('%s ' % str(y_simulated_sollya[i]).replace(" ", "").replace("\n", ""))
			f_handle.write('\n')
			#f_handle.write(str(y_simulated_exact_sollya[i]) + ' ')
			#f_handle.write('\n')

	f_handle.close()


	return True







def test_MSBcomputation():

	b = np.array([0.118370664306386721986719123833609046414,\
	0.490401026793067740250364749954314902425,\
	1.190570782819459605406109403702430427074,\
	1.916028855100447181314393674256280064583,\
	2.24415541717465805149345214886125177145,\
	1.916028855100447181314393674256280064583,\
	1.190570782819459383361504478671122342348,\
	0.490401026793067740250364749954314902425,\
	0.118370664306386721986719123833609046414])

	a = np.array([1,\
	0.989003287123678465064813281060196459293,\
	2.976167956020775662295818619895726442337,\
	1.512781789805480725519259976863395422697,\
	2.695082071017033342741342494264245033264,\
	0.485244776245198516928525123148574493825,\
	1.019697185038379139143671636702492833138,\
	-0.018250143199271331995170442041853675619,\
	0.19568726182868487195598561356746358797])


	bb = np.array([	0.001024353901619323454347254553908896924,\
		- 0.003663407014305803538478656378174491692,\
		0.009922413988848466370740197817212902009,\
		- 0.016887619213826352004836905962292803451,\
		0.024684048139283695788570582863030722365,\
		- 0.027439202723066401234941480424822657369,\
		0.029769234201076827384113698826695326716,\
		- 0.028347933334659319859483161962998565286,\
		0.029769234201076827384113698826695326716,\
		- 0.027439202723066401234941480424822657369,\
		0.024684048139283695788570582863030722365,\
		- 0.016887619213826352004836905962292803451,\
		0.009922413988848466370740197817212902009,\
		- 0.003663407014305803538478656378174491692,\
		0.001024353901619323454347254553908896924])

	aa = np.array([1,\
		- 8.725375200483702187170820252504199743271,\
		38.355219838025000456127600045874714851379,\
		- 110.745294497399868305365089327096939086914,\
		232.737270240590930825419491156935691833496,\
		- 374.625496202077897578419651836156845092773,\
		474.689127543620941196422791108489036560059,\
		- 479.925865263857758691301569342613220214844,\
		388.535887145793935815163422375917434692383,\
		- 250.49976697946030412822437938302755355835,\
		126.621475216987306566807092167437076568604,\
		- 48.699249987806084050134813878685235977173,\
		13.494402545098072465634686523117125034332,\
		- 2.418212469015935894844915310386568307877,\
		0.212424718070935131253307304177724290639])

	H = dTF(num=bb, den=aa)
	SS = H.to_dSS()
	WCPG = SS.WCPG()

	SIF_DFI = DFI(Filter(num=bb, den=aa), transposed=False)

	deltaH = SIF_DFI.computeDeltaSIF()

	# compute the WCPG of the error filter
	wcpgDeltaH = deltaH.dSS.WCPG()


	#print H.to_dSS().WCPG_tf()
	#print H.to_dSS().to_dSSmp().WCPGmp(2**-53)




	nSimulations = 100


	#assert(test_computeMSBSIF(nSimulations))






