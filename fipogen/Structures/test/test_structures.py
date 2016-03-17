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
from fipogen.Structures import iterStructures
from fipogen.LTI.random import random_dTF, random_dSS

import pytest


@pytest.mark.parametrize( "H", random_dTF( 20, stable=True ))
def test_buildAllPossibleRealizationsFromdTF( H ):
	"""
	Check all the SISO structures (including MIMO structures)
	check that the correspong transfer function is equal to the initial transfer function
	"""
	print('')

	for R in iterStructures( LTI( tf=H) ):
		print ( R.fullName +"\t")
		H.assert_close( R.SIF.dSS.to_dTF() )



@pytest.mark.parametrize( "S", random_dSS( 20, stable=True, n=(5,15), p=(1,10), q=(1,10) ))
def test_buildAllPossibleRealizationsFromdSS( S ):
	"""
	Check all the possible realizations
	Check that the corresponding system (state-space) corresponds to the initial one
	"""
	print('')
	for R in iterStructures( LTI( ss=S),  ):
		print ( R.fullName +"\t")
		S.assert_close( R.SIF.dSS )

