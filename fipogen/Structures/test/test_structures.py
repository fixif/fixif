#coding: utf8

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"




from fipogen.LTI import LTI
from fipogen.Structures import iterStructures,LWDF
from fipogen.LTI.random import iter_random_dTF, iter_random_dSS, iter_random_Butter

import pytest


@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_buildAllPossibleRealizationsFromdTF( H ):
	"""
	Check all the SISO structures (including MIMO structures)
	check that the correspong transfer function is equal to the initial transfer function
	"""
	print('')

	for R in iterStructures( LTI( tf=H, stable=False) ):
		print ( R.fullName +"\t")
		H.assert_close( R.SIF.dSS.to_dTF() )



@pytest.mark.parametrize( "S", iter_random_dSS(20, stable=True, n=(5, 15), p=(1, 2), q=(1, 2)))
def test_buildAllPossibleRealizationsFromdSS( S ):
	"""
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
	print('')
	for R in iterStructures( LTI( ss=S, stable=True)  ):
		print ( R.fullName +"\t")
		S.assert_close( R.SIF.dSS )



@pytest.mark.parametrize( "H", iter_random_Butter(20, form='lowpass'))
def test_LWDF( H ):
	"""
	Check the LWDF structure
	check that the correspong transfer function is equal to the initial transfer function
	"""
	R = LWDF( H)
	H.dTF.assert_close( R.SIF.dSS.to_dTF(), eps=1e-4 )
