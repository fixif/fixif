# coding=utf8

"""
This file contains tests for the FPF class and its methods
"""


__author__ = "Thibault Hilaire, Benoit Lopez"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import pytest
from fipogen.oSoP import FPF


def test_construct(self):
	"""Unit test for the FPF constructor"""
	# construct FPF with less than 2 args
	with pytest.raises(ValueError):
		f = FPF(16)
	with pytest.raises(ValueError):
		f = FPF(msb=12)
	with pytest.raises(ValueError):
		f = FPF(lsb=-6)		
	
	# construct FPF with only wl and (lsb or msb)
	f = FPF(16,lsb=-12)
	self.assertEqual(f.wml(),(16,3,-12))
	f = FPF(16,msb=3)
	self.assertEqual(f.wml(),(16,3,-12))
	f = FPF(16,msb=0)
	self.assertEqual(f.wml(),(16,0,-15))
	with pytest.raises(ValueError):
		f = FPF(16,12,-5)
	
	# construct form string
	f = FPF(formatStr="Q8.12")
	self.assertEqual( f.wml(), (20,7,-12))
	f = FPF(formatStr="sQ4.3")
	self.assertEqual( f.wml(), (7,3,-3))
	f = FPF(formatStr="uQ4.3")
	self.assertEqual( f.wml(), (7,3,-3))
	f = FPF(formatStr="(8,-12)")
	self.assertEqual( f.wml(), (21,8,-12))
	f = FPF(formatStr="u(8,-12)")
	self.assertEqual(f.signed, False)
	self.assertEqual( f.wml(), (21,8,-12))
	with pytest.raises(ValueError):
		f = FPF(formatStr="totoQ6.8")
		
	f = FPF( msb=7,lsb=0,signed=True)
	self.assertEqual( f.interval(), (-128,127))
	f = FPF( msb=7,lsb=0,signed=False)
	self.assertEqual( f.interval(), (0,255))
	
def test_shif(self):
	f = FPF(16,3,-12)
	f.shift(2)
	self.assertEqual(f.wml(),(16,5,-10))

	
def test_approx(self):
	F=FPF(16,8)
	self.assertEqual(F.approx(25),25)
	self.assertEqual(F.approx(25.001),25)
	self.assertEqual(F.approx(25.26789),25.265625)
		
