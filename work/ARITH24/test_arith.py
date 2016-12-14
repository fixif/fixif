
from arith import CheckIfRealizationInGabarit

from fipogen.LTI import Gabarit, Filter
from fipogen.SIF import Realization
from fipogen.Structures import iterAllRealizations, State_Space, rhoDFII, DFI, DFII

import pytest
from pytest import mark
from pytest import raises

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

@mark.parametrize("g", iterSimpleGabarit(), ids='')
@mark.parametrize("type", ('butter', 'cheby2', 'ellip'))
@mark.parametrize("method", ('matlab','scipy'))
@mark.parametrize("q", ('64','16','32'))
@mark.parametrize("R", (State_Space, rhoDFII, DFI, DFII))
def test_CheckIfRealizationInGabarit(g,type,method, q, R):
	H = g.to_dTF(method=method, ftype=type, designMargin=1e-3)
	wl=int(q)
	Rapprox = R(Filter(tf=H)).quantize(wl)
	#for R in iterAllRealizations(Filter(tf=H)):
	#Rapprox = State_Space(Filter(tf=H)).quantize(wl)
	print ('------> Checking Realization: %s') % (Rapprox._structureName)
	check, margin, res = CheckIfRealizationInGabarit(g, Rapprox)
	if check:
		print ('------> Realization %s is in Gabarit with margin = %e') % (Rapprox._structureName, margin)
		print ('------> The Sollya result is %s') % (res)
	else:
		print ('------> Something went wrong! ...')
		print ('------> The Sollya result is %s') % (res)
	print('Asserting now')
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
