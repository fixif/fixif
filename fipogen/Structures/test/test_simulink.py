#coding: utf8

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"




import pytest
from fipogen.Structures.Simulink import importSimulink



def test_simulink():
	R = importSimulink( 'direct_form2.slx'  )
	print(R)

	# R.dSS.to_dTF.assert_close( ... )