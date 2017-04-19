
from fipogen.LTI import dSS, Butter, dTF, dSSmp, dTFmp
from fipogen.SIF import Realization, Realization_FxP
from numpy import matrix as mat, zeros, eye, empty, float64
import numpy as np
import time
import numpy


from fipogen.func_aux import write_matrix_mpf, write_matrix_hex, mpf_matrix_to_sollya, mpf_get_representation, \
	python2mpf_matrix, sollya_matrix_to_numpy

from fipogen.Structures import LWDF, DFII, State_Space, DFI

from fipogen.Structures import iterAllRealizations, iterAllRealizationsRandomFilter
from fipogen.LTI import Filter, iter_random_Filter, iter_random_dSS, random_Filter, random_dSS, dSS


import mpmath
from mpmath import *
import sollya



def computeLSB_MSB(sif,lsb_y_out, u_bar):
	"""
	Given a SISO filter Realization and the output format lsb_y_out,
	this function computes such MSB and LSB positions for
	all variables involved in computations that the output error
	of the filter is bounded by 2^lsb_out.

	Also, the function returns the error budget (expressed in ulps)
	for the computation of the SOPC that corresponds to the
	output variable y.


	Parameters
	----------
	sif - Relization describing a SISO filter (1 input and 1 output) in SIF
	u_bar - the bound on the input interval
	lsb_y_out - the required LSB position of the output y

	Returns
	-------
	lsb_out
	msb_out
	error_budget

	"""

	msb = sif._compute_MSB(u_bar)
	lsb, error_budget_y = sif._compute_LSB(lsb_y_out)
	Y, N = mpf_get_representation(mpmath.mpf(error_budget_y))
	error_budget_y = (sollya.SollyaObject(Y) * 2 ** sollya.SollyaObject(N)) / 2**-lsb_y_out

	lsb_t = [lsb[0, i] for i in range(0, sif.l)]
	lsb_x = [lsb[0, i] for i in range(sif.l, sif.l + sif.n)]
	lsb_y = [lsb[0, i] for i in range(sif.l + sif.n, sif.l + sif.n + sif.p)]
	lsb[0,sif.l + sif.n] = lsb_y_out

	msb_ext = sif.compute_MSB_allvar_extended(u_bar, lsb_t, lsb_x, lsb_y)
	if ((msb != msb_ext).any()):
		print(
		'MSB computed with taking into account the propagation of the error due to the format (msb, lsb) differs from the initial format. Changing MSBs.\n')
		print('new MSBs:')
		msb = msb_ext
		print(msb)

	#msb_t = [msb[0, i] for i in range(0, sif.l)]
	#msb_x = [msb[0, i] for i in range(sif.l, sif.l + sif.n)]
	#msb_y = [msb[0, i] for i in range(sif.l + sif.n, sif.l + sif.n + sif.p)]

	return lsb, msb, error_budget_y


def doSimulations(sif, lsb_u, nSimulations=1000, exact=False, prec=53):
	"""
	This function performs simulations of a SISO filter realization described with SIF.
	The inputs are random variables in the interval (-1,1) further rounded to lsb_u bits.
	If exact=True, the simulations are performed in exact arithmetic.
	Otherwise, the simulations of a filter is performed with correct rounding to prec bits:
	on each iteration of the filter computations are performed with correct
	rounding to nearest.
	The result of the simulations is returned as a lit of sollya objects.

	Parameters
	----------
	sif             - SISO filter realization
	lsb_u           - the number of fractional bits for the filter's inputs
	nSimulations    - number of simulations
	exact           - a boolean
	prec            - precision for the simulations of exact=False

	Returns
	-------

	y_simulated

	"""

	u = np.random.rand(1, nSimulations)

	# quantize the simulations to the format lsb_u bits
	u_sollya = mpf_matrix_to_sollya(mpmath.matrix([mpmath.nint(mpmath.mpf(u[0, i]) * 2 ** -lsb_u) / 2 ** -lsb_u for i in range(0, nSimulations)]))[0]
	u_quantized = sollya_matrix_to_numpy(u_sollya, 1, nSimulations)

	# perform simulations either in exact or rounded
	if exact:
		y_simulated = mpf_matrix_to_sollya(sif.to_dSSexact().simulate(u_quantized, exact=True))[0]
	else:
		y_simulated = sif.to_dSSexact().simulate_rounded(u_quantized, prec=prec)

	return u_sollya, y_simulated



def Realization_to_Flopoco(R, u_bar=1, lsb_u=-12, msb_u=0, lsb_y=-12, T=100):
	"""

	Parameters
	----------
	R
	u_bar
	lsb_u
	msb_u
	lsb_y
	T

	Returns
	-------
	SIF_specs - name of the file containing the SOPCS specifications for Flopoco
	SIF_simulation - nalem of the filte containing the testbench for Flopoco

	"""

	lsb, msb, error_budget = computeLSB_MSB(R,lsb_y, u_bar)
	print "LSB positions: %s" % lsb
	print "MSB positions: %s" % msb
	print "error bidget: %s" % str(error_budget)



	u_test, y_test = doSimulations(R, lsb_u, nSimulations=T, exact=True, prec=53)

	Z = R.Z



	fileID = './SIF-' + time.strftime("%d%m%Y-%H%M%S")
	SIF_specs = fileID + '.txt'
	with open(SIF_specs, 'a') as f_handle:
		f_handle.write('%d\n%d\n%d\n%d\n' % (R.q, R.l, R.n, R.p))
		f_handle.write('%d %d\n' % (msb_u, lsb_u))
		for i in range(0, msb.shape[1]-1):
			f_handle.write('%d %d\n' % (msb[0,i], lsb[0,i]))
		f_handle.write('%d %d %s\n' % (msb[0,msb.shape[1]-1], lsb_y, str(error_budget).replace(" ", "").replace("\n", "")))

		Z_sollya, Zrows, Zcols = mpf_matrix_to_sollya(python2mpf_matrix(R.Z))
		for i in range(0, Zrows):
			for j in range(0, Zcols):
				f_handle.write('%s' % str(Z_sollya[i + j * Zcols]).replace(" ", "").replace("\n", ""))
				f_handle.write(' ')
			f_handle.write('\n')

	SIF_simulation = fileID + 'simulation' + '.txt'
	with open(SIF_simulation, 'a') as f_handle:
		f_handle.write('%d\n' % T)
		for i in range(0, T):
			f_handle.write('%s' % str(u_test[i]).replace(" ", "").replace("\n", ""))
			f_handle.write('\n')
			f_handle.write('%s ' % str(y_test[i]).replace(" ", "").replace("\n", ""))
			f_handle.write('\n')

	f_handle.close()

	return SIF_specs, SIF_simulation


def printFlopoco(specs_fname, simulations_fname):
	flopocostring = '/Users/anastasiialozanova/Work/flopoco/flopoco/build/flopoco FixSIF paramFileName="' + specs_fname + '" testsFileName="' + simulations_fname + '" TestBench n=0'
	print flopocostring
	return flopocostring

def callFLOPOCO(specs_fname, simulations_fname):
	import subprocess
	command = printFlopoco(specs_fname, simulations_fname)
	try:
		flopoco_output = subprocess.check_output(command, stderr = subprocess.STDOUT,shell = True)
	except subprocess.CalledProcessError as e:
		print e.message
		raise ValueError("FloPoCo call is not successful: %s\n", command)

	if flopoco_output.find("To run the simulation using gHDL, type the following in a shell prompt:") < 0:
		raise ValueError("FloPoCo call is not successful\n")

	flopoco_output = flopoco_output.split("\n")
	i = flopoco_output.index("To run the simulation using gHDL, type the following in a shell prompt:")
	ghdl1 = flopoco_output[i+1]
	ghdl2 = flopoco_output[i+2]
	ghdl3 = flopoco_output[i+3]

	try:
		print "compiling VHDL.....",
		ghdl1_output = subprocess.check_output(ghdl1, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl1)
	print "OK"
	try:
		print "compiling tests.....",
		ghdl2_output = subprocess.check_output(ghdl2, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl2)
	print "OK"
	try:
		print "testing.....",
		ghdl3_output = subprocess.check_output(ghdl3, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl3)

	if ghdl3_output.find("(report note): 0 error(s) encoutered.") > 0:
		print "Success!"
		return True
	else:
		print "Some of the tests failed.\n %s" % ghdl3_output
		return False


def underwaterAcousticsExample():
	b = numpy.matrix([
		0.000000459047935933202453993417623684392,\
		0,\
		- 0.000003213335551532417072074804959003202,\
		0,\
		0.000009640006654597252063257362131309947,\
		0,\
		- 0.00001606667775766208790147286655791703,\
		0,\
		0.00001606667775766208790147286655791703,\
		0,\
		- 0.000009640006654597252063257362131309947,\
		0,\
		0.000003213335551532417072074804959003202,\
		0,\
		- 0.000000459047935933202453993417623684392	])

	a = numpy.matrix([1,\
		10.119168425703881197819100634660571813583,\
		50.368718721819398354000441031530499458313,\
		162.169271594177132556069409474730491638184,\
		375.674400846890137017908273264765739440918,\
		660.571854665738555922871455550193786621094,\
		907.657287531431734350917395204305648803711,\
		989.117538197241401576320640742778778076172,\
		858.784412851431284252612385898828506469727,\
		591.350285655579909871448762714862823486328,\
		318.201031784725728357443585991859436035156,\
		129.967303320702541213904623873531818389893,\
		38.197046210551278022649057675153017044067,\
		7.262400616632169736419655237114056944847,\
		0.67943470904311342728476574848173186183])




	return b,a

fOrder = 3
#F = random_Filter(fOrder, 1, 1, seed=100) ---> works
F = random_Filter(fOrder, 1, 1, seed=101 )
b,a = underwaterAcousticsExample()

F = Filter(num=b, den=a)
#R = State_Space.makeRealization(F)
R = DFI(F, transposed=False)
u_bar = 1
msb_u = 0
lsb_u = -15
lsb_y = -15

R_specs, R_sim = Realization_to_Flopoco(R, u_bar, lsb_u, msb_u, lsb_y, 100)

res = callFLOPOCO(R_specs, R_sim)
print res




#
# def test_computeMSBSIF(nSimulations=1000):
#
# 	sollya.settings.display = sollya.binary
# 	nu = 1
# 	ny = 1
# 	nx = 5
# 	F = random_Filter(nx, ny, nu, seed=5)
# 	#F = Butter(5, 1.2)
# 	#SS = LWDF.makeRealization(F)
# 	SS = State_Space.makeRealization(F)
#
#
# 	#a hardcoded example
# 	#A = np.matrix([[-0.1721,  0.004845,    0.2187],[0.004845,  -0.08567,   -0.1096], [0.2187,   -0.1096,   -0.4978]])
# 	#B = np.matrix([[1.533], [0], [0]])
# 	#C = np.matrix([-0.2256,    1.117,   -1.089])
# 	#D = np.matrix([0.03256])
# 	#F = Filter(A=A,B=B,C=C,D=D)
# 	#SS = State_Space.makeRealization(F)
#
#
#
# 	u_bar = np.bmat([np.ones([1, nu])])
# 	l_y_out = -15
# 	#msb_u = np.bmat([np.zeros([1, SS.q])])
# 	#lsb_u = -15 * np.bmat([np.ones([1, SS.q])])
# 	msb_u = 0
# 	lsb_u = -15
#
# 	msb = SS._compute_MSB(u_bar)
# 	lsb, error_budget_y = SS._compute_LSB(l_y_out)
# 	Y, N = mpf_get_representation(mpmath.mpf(error_budget_y))
# 	error_budget_y = sollya.SollyaObject(Y) * 2**sollya.SollyaObject(N)
#
# 	lsb_t = [lsb[0, i] for i in range(0, SS.l)]
# 	lsb_x = [lsb[0, i] for i in range(SS.l, SS.l + SS.n)]
# 	lsb_y = [lsb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]
#
# 	msb_ext = SS.compute_MSB_allvar_extended(u_bar, lsb_t, lsb_x, lsb_y)
# 	if ((msb != msb_ext).any()):
# 		print('MSB computed with taking into account the propagation of the error due to the format (msb, lsb) differs from the initial format. Changing MSBs.\n')
# 		print('new MSBs:')
# 		msb = msb_ext
# 		print(msb)
#
# 	msb_t = [msb[0, i] for i in range(0, SS.l)]
# 	msb_x = [msb[0, i] for i in range(SS.l, SS.l + SS.n)]
# 	msb_y = [msb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]
#
# 	fileID = './SIF-' + time.strftime("%d%m%Y-%H%M%S")
# 	filename = fileID + '.txt'
# 	with open(filename, 'a') as f_handle:
# 		f_handle.write('%d\n%d\n%d\n%d\n' % (SS.q, SS.l, SS.n, SS.p))
# 		#for i in range(0, SS.q):
# 		f_handle.write('%d %d\n' % (msb_u, lsb_u))
# 		for i in range(0, SS.l):
# 			f_handle.write('%d %d\n' % (msb_t[i], lsb_t[i]))
# 		for i in range(0, SS.n):
# 			f_handle.write('%d %d\n' % (msb_x[i], lsb_x[i]))
# 		for i in range(0, SS.p):
# 			f_handle.write('%d %d %s\n' % (msb_y[i], l_y_out, str(error_budget_y).replace(" ", "").replace("\n", "")))
# 		#f_handle.write('%s\n' % str(error_budget_y))
#
#
# 		#write_matrix_hex(f_handle, SS.Z, ' ')
# 		Z_sollya, Zrows, Zcols  = mpf_matrix_to_sollya(python2mpf_matrix(SS.Z))
#
# 		for i in range(0, Zrows):
# 			for j in range(0, Zcols):
# 				f_handle.write('%s' % str(Z_sollya[i + j * Zcols]).replace(" ", "").replace("\n", ""))
# 				f_handle.write(' ')
# 			f_handle.write('\n')
#
# 	f_handle.close()
#
# 	print('Filter: \n')
# 	print(SS)
# 	print('y_out was initially set to: %d\n' %l_y_out)
# 	print('LSBs:\n')
# 	print(lsb)
# 	print('MSBs:\n')
# 	print(msb)
#
#
# 	u = np.random.rand(1, nSimulations)
#
# 	# quantize the simulations to the format lsb_u bits
# 	u_sollya = mpf_matrix_to_sollya(mpmath.matrix([mpmath.nint(mp.mpf(u[0,i]) * 2 ** -lsb_u) / 2 ** -lsb_u for i in range(0, nSimulations)]))[0]
# 	u_quantized = sollya_matrix_to_numpy(u_sollya, 1, nSimulations)
#
#
# 	# perform simulations either in exact or rounded
#
# 	y_simulated_sollya_exact = SS.to_dSSexact().simulate_rounded(u_quantized, prec=53)
# 	y_simulated_sollya = mpf_matrix_to_sollya(SS.to_dSSexact().simulate(u_quantized, exact=True))[0]
#
#
# 	filename = fileID + 'simulation' + '.txt'
# 	with open(filename, 'a') as f_handle:
# 		f_handle.write('%d\n' % nSimulations)
# 		for i in range(0,nSimulations):
# 			#for j in range (0, nu):
# 			f_handle.write('%s' % str(u_sollya[i]).replace(" ", "").replace("\n", ""))
# 			f_handle.write('\n')
# 			#for j in range(0,ny):
# 			f_handle.write('%s ' % str(y_simulated_sollya[i]).replace(" ", "").replace("\n", ""))
# 			f_handle.write('\n')
# 			#f_handle.write(str(y_simulated_exact_sollya[i]) + ' ')
# 			#f_handle.write('\n')
#
# 	f_handle.close()
#
#
# 	return True
#





#
# def test_MSBcomputation():
#
# 	b = np.array([0.118370664306386721986719123833609046414,\
# 	0.490401026793067740250364749954314902425,\
# 	1.190570782819459605406109403702430427074,\
# 	1.916028855100447181314393674256280064583,\
# 	2.24415541717465805149345214886125177145,\
# 	1.916028855100447181314393674256280064583,\
# 	1.190570782819459383361504478671122342348,\
# 	0.490401026793067740250364749954314902425,\
# 	0.118370664306386721986719123833609046414])
#
# 	a = np.array([1,\
# 	0.989003287123678465064813281060196459293,\
# 	2.976167956020775662295818619895726442337,\
# 	1.512781789805480725519259976863395422697,\
# 	2.695082071017033342741342494264245033264,\
# 	0.485244776245198516928525123148574493825,\
# 	1.019697185038379139143671636702492833138,\
# 	-0.018250143199271331995170442041853675619,\
# 	0.19568726182868487195598561356746358797])
#
#
# 	bb = np.array([	0.001024353901619323454347254553908896924,\
# 		- 0.003663407014305803538478656378174491692,\
# 		0.009922413988848466370740197817212902009,\
# 		- 0.016887619213826352004836905962292803451,\
# 		0.024684048139283695788570582863030722365,\
# 		- 0.027439202723066401234941480424822657369,\
# 		0.029769234201076827384113698826695326716,\
# 		- 0.028347933334659319859483161962998565286,\
# 		0.029769234201076827384113698826695326716,\
# 		- 0.027439202723066401234941480424822657369,\
# 		0.024684048139283695788570582863030722365,\
# 		- 0.016887619213826352004836905962292803451,\
# 		0.009922413988848466370740197817212902009,\
# 		- 0.003663407014305803538478656378174491692,\
# 		0.001024353901619323454347254553908896924])
#
# 	aa = np.array([1,\
# 		- 8.725375200483702187170820252504199743271,\
# 		38.355219838025000456127600045874714851379,\
# 		- 110.745294497399868305365089327096939086914,\
# 		232.737270240590930825419491156935691833496,\
# 		- 374.625496202077897578419651836156845092773,\
# 		474.689127543620941196422791108489036560059,\
# 		- 479.925865263857758691301569342613220214844,\
# 		388.535887145793935815163422375917434692383,\
# 		- 250.49976697946030412822437938302755355835,\
# 		126.621475216987306566807092167437076568604,\
# 		- 48.699249987806084050134813878685235977173,\
# 		13.494402545098072465634686523117125034332,\
# 		- 2.418212469015935894844915310386568307877,\
# 		0.212424718070935131253307304177724290639])
#
# 	H = dTF(num=bb, den=aa)
# 	SS = H.to_dSS()
# 	WCPG = SS.WCPG()
#
# 	SIF_DFI = DFI(Filter(num=bb, den=aa), transposed=False)
#
# 	deltaH = SIF_DFI.computeDeltaSIF()
#
# 	# compute the WCPG of the error filter
# 	wcpgDeltaH = deltaH.dSS.WCPG()
#
#
# 	#print H.to_dSS().WCPG_tf()
# 	#print H.to_dSS().to_dSSmp().WCPGmp(2**-53)
#
#
#
#
# 	nSimulations = 100
#
#
# 	#assert(test_computeMSBSIF(nSimulations))




