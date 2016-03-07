# coding: utf8

"""
This file contains Object and methods for a LTI System
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from numpy.testing import assert_allclose

from fipogen.LTI import dTF, dSS, LTI
from fipogen.LTI.random import random_dTF
from numpy.linalg           import solve

import pytest


def test_construction( ):
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		LTI( num=[1, 2, 3], den=[0, 6 ,7] )		# den[0] cannot be zero
	with pytest.raises(ValueError):
		LTI( num=[1, 2, 3], den=[1, 2] )		# num should not be longer than den

	# test non-consistency size
	with pytest.raises(ValueError):
		LTI( A=[[1, 2], [3, 4], [5, 6]], B=1, C=2, D=3 )
	with pytest.raises(ValueError):
		LTI( A=[[1, 2], [3, 4]], B=1, C=2, D=3 )
	with pytest.raises(ValueError):
		LTI( A=[[1, 2], [3, 4]], B=[[1], [2]], C=2, D=3)
	with pytest.raises(ValueError):
		LTI( A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2], [1, 2]], D=3)

	with pytest.raises(ValueError):
		LTI( A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2]], num=[1, 2, 3])

	L=LTI( A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2]], D=3, num=[1, 2, 3], den=[0, 6 ,7])



