from fipogen.LTI import LTI
from fipogen.Structures import Structure
from fipogen.LTI.random import random_dTF, random_dSS
import sys
import pytest


@pytest.mark.parametrize( "H", random_dTF( 20 ))
def test_buildAllPossibleRealizationFromdTF( H ):

	for R in Structure.iterStructures( LTI( tf=H) ):
		print ("\n" + R.fullName +"\t")
		H.assert_close( R.SIF.dSS.to_dTF() )



@pytest.mark.parametrize( "S", random_dSS( 20, False, n=(5,15), p=(1,10), q=(1,10) ))
def test_buildAllPossibleRealizationFromdSS( S ):

	for R in Structure.iterStructures( LTI( ss=S) ):
		S.assert_close( R.SIF.dSS )

