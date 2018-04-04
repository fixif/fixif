
from arith import CheckIfRealizationInGabarit

from fipogen.LTI import Gabarit, Filter, dTF
from fipogen.SIF import Realization
from fipogen.LTI import random_Filter
from fipogen.Structures import iterStructuresAndOptions, State_Space, rhoDFII, DFI, DFII, LWDF

import pytest
from pytest import mark, fixture
from pytest import raises
import numpy

# a simple gabarit iterator
def iterSimpleGabarit():
	# lowpass
	yield Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
	# highpass
	yield Gabarit(48000,[ (0,9600), (12000,None) ], [-20, (0,-1)])
	# bandpass
	yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [-20, (0, -1), -20])
	# bandstop
	yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [(0,-1), -20, (0,-1)])
	# multibands
	#yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, 19000), (19000,None)], [(0,-1), -20, (0,-1),-40])


fakeFilter = random_Filter(2,1,1)


#@mark.parametrize("g", iterSimpleGabarit(), ids=lambda x:x.type)
@mark.parametrize("type", ('cheby2', 'butter'))
#@mark.parametrize("method", ('scipy',))
@mark.parametrize("wl", (32,16,8))
@mark.parametrize("SandO", iterStructuresAndOptions(fakeFilter), ids=lambda x:x[0].name)
def test_CheckIfRealizationInGabarit(SandO, wl, type, method='matlab'):

	# create the initial transfer function (designMargin = 0)
	g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
	H = g.to_dTF(method=method, ftype=type, designMargin=0)
	filt = Filter(tf=H)
	# build the realizatoin from the structure and options
	st,options = SandO
	if options:
		R = st.makeRealization(filt, **options)
	else:
		R = st.makeRealization(filt)
	Rapprox = R.quantize(wl)

	# check if realization in Gabarit
	print('------> Checking Realization: %s' % (R.structureName))
	check, margin, marginDB, res = CheckIfRealizationInGabarit(g, Rapprox)
	if check:
		print('------> Realization %s is in Gabarit with margin = %s\n marginDB = %s' % (R.structureName, margin, marginDB))
	else:
		print('------> Something went wrong! ...')
	assert (check)




def test_example1_LWDF():


	# These are the coefficients of an alliptic filter created with MATLAB
	#filter has passband in [0, 0.1] with ripple 0.1dB and stopband from 0.3
	#with minimum attenuation -80dB
	#
	# b = numpy.matrix([3.770838943200613e-04, \
	#                   - 2.024690051110791e-04, \
	#                   3.407766155670199e-04, \
	#                   3.407766155670199e-04, \
	#                   - 2.024690051110791e-04, \
	#                   3.770838943200613e-04])
	# a = numpy.matrix([1.000000000000000e+00, \
	#                   - 4.340164570232563e+00, \
	#                   7.668918353331406e+00, \
	#                   - 6.884599315526233e+00, \
	#                   3.136630548401215e+00, \
	#                   - 5.797542329642728e-01])


	g = Gabarit(48000, [(0, 2400), (7200, None)], [(0, -0.2), -80.1])

	TF = g.to_dTF(ftype='ellip', method='matlab', centeredZero=True)
	F = Filter(num=TF.num, den=TF.den)
	R = LWDF.makeRealization(F)
	w = 16
	Rq = R.quantize(w)

	check, margin, marginDB, res = CheckIfRealizationInGabarit(g, R)
	if check:
		print(
		'------> Realization %s is in Gabarit with\n margin = %s\n marginDB = %s' % (R.structureName, margin, marginDB))
	else:
		print('------> Something went wrong! ...')
	#assert (check)

	check, margin, marginDB, res = CheckIfRealizationInGabarit(g, Rq)
	if check:
		print(
			'------> Realization %s quantized to w=%d is in Gabarit with\n margin = %s\n marginDB = %s' % (
			R.structureName, w, margin, marginDB))
	else:
		print('------> Something went wrong! ...')

	assert (check)

#
# def test_StrangeError():
# 	g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
# 	H = g.to_dTF(method='matlab', ftype='butter', designMargin=1e-3)
# 	wl = 64
# 	for R in iterAllRealizations(Filter(tf=H)):
# 		Rapprox = R.quantize(wl)
#
# 		check, margin = CheckIfRealizationInGabarit(g, Rapprox)
# 		if check:
# 			print ('------> Realization %s is in Gabarit with margin = %e') % (Rapprox._structureName, margin)
# 		else:
# 			print ('------> Something went wrong! ...')
