# coding=utf8

"""
This file contains tests for the dTF class and its methods
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from fipogen.LTI import dTF
from fipogen.LTI.random import iter_random_dTF

import pytest



def test_construction( ):
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		dTF( [1, 2, 3], [0, 6 ,7] )		# den[0] cannot be zero
	with pytest.raises(ValueError):
		dTF( [1, 2, 3], [1, 2] )		# num should not be longer than den


@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_str( H ):
	str(H)


@pytest.mark.parametrize( "H", iter_random_dTF(20))
def test_to_dSS( H ):
	S = H.to_dSS()
	HH = S.to_dTF()

	H.assert_close( HH )
