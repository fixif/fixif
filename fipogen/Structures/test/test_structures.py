#coding: utf8

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fipogen.Structures import iterAllRealizations, LWDF
from fipogen.LTI import Filter, iter_random_Filter
from fipogen.LTI import iter_random_Butter
from fipogen.LTI import iter_random_dTF
from fipogen.Structures import DFI

import pytest



@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_buildAllPossibleSISORealizationsFromdTF( H ):
	"""
	Check all the SISO structures (including MIMO structures)
	check that the correspong transfer function is equal to the initial transfer function
	"""
	print('')

	for R in iterAllRealizations(Filter(tf=H, stable=False)):
		print ( R.name +"\t")
		H.assert_close( R.dSS.to_dTF() )



@pytest.mark.parametrize( "F", iter_random_Filter(20, n=(5, 15), p=(1, 5), q=(1, 5)))
def test_buildAllPossibleMIMORealizationsFromdSS( F ):
	"""
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
	print('')
	for R in iterAllRealizations(F):
		print ( R.name +"\t")
		F.dSS.assert_close( R.dSS )



@pytest.mark.parametrize( "F", iter_random_Filter(20, n=(5, 10), p=(1, 2), q=(1, 2)))
def test_buildAllPossibleStableSISORealizationsFromdSS( F ):
	"""
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
	print('')
	for R in iterAllRealizations(F):
		print ( R.name +"\t")
		F.dSS.assert_close( R.dSS )





@pytest.mark.parametrize( "H", iter_random_Butter(20, form='lowpass'))
def test_LWDF( H ):
	"""
	Check the LWDF structure
	check that the correspong transfer function is equal to the initial transfer function
	"""
	R = LWDF.makeRealization( H)
	H.dTF.assert_close( R.dSS.to_dTF(), eps=1e-4 )
