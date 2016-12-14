# coding=utf8

"""
This file contains tests for the dTF class and its methods
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from pytest import mark
from pytest import raises
from fipogen.LTI import Gabarit, dTF


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




def test_GabaritConstruction():
	"""
	Test the constructor and some basic properties
	"""
	# wrong construction
	with raises(ValueError):
		Gabarit(None, [(0,0.2),(0.3,0.4),(0.5,1)], [-10,-20])
	# lowpass
	g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
	assert(g.type == 'lowpass')
	assert(g.bands[0].w2 == 0.4)
	assert(g.bands[1].w1 == 0.5)
	assert(g.bands[1].F2 == 24000)
	assert(g.bands[0].isPassBand)
	assert(g.bands[0].passGains == (-1,0))
	assert(not g.bands[1].isPassBand)
	assert(g.bands[1].stopGain == -20)

	# highpass
	g = Gabarit(48000,[ (0,9600), (12000,None) ], [-20, (0,-1)])
	assert(g.type == 'highpass')

	# bandpass
	g = Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [-20, (0, -1), -20])
	assert (g.type == 'bandpass')

	# bandstop
	g = Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [(0,-1), -20, (0,-1)])
	assert (g.type == 'bandstop')

	# inverted bands
	g = Gabarit(48000,[ (12000,None), (0,9600) ], [(0,-1), -20])
	assert(g.type == 'highpass')
	assert(g.bands[0].F1==0)
	assert(g.bands[0].F2==9600)
	assert(not g.bands[0].isPassBand)

	# multibands
	g = Gabarit(48000, [(0, 9600), (12000, 14000), (16400, 19000), (19000,None)], [(0,-1), -20, (0,-1),-40])
	assert (g.type == 'multiband')



@mark.parametrize("g", iterSimpleGabarit(), ids='')
@mark.parametrize("type", ('butter', 'cheby1', 'cheby2', 'ellip'))
#@mark.parametrize("type", ['ellip'])
@mark.parametrize("method", ('matlab','scipy'))
def test_Gabarit_to_dTF(g,type,method):
	"""
	Test if the conversion to_dTF works for matlab/scipy and various types
	"""
	H = g.to_dTF(method=method, ftype=type, designMargin=1e-3)
	print(H)
	# check it's in the gabarit +/- 1dB
	#assert(g.check_dTF(H,margin=0)[0])
	print(g.findMinimumMargin(H))
	#g.plot(H)


@mark.parametrize("g", iterSimpleGabarit(), ids='')
def test_minimumMargin(g):
	#g = Gabarit(48000,[ (0,9600), (12000,None) ], [-20, (0,-1)])
	H = g.to_dTF(method='matlab', ftype='ellip')
	#H2 = dTF(1.1*H.num,H.den)
	print(g.findMinimumMargin(H))

def test_cql():
        g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
        H = g.to_dTF(method='matlab', ftype='cheby1')
        print(H)
        print(g.findMinimumMargin(H))
