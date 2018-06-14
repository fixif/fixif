# coding: utf8

"""
This file contains Object and methods for a Filter System
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.LTI import Filter, random_Filter, iter_random_Filter
from fixif.LTI import iter_random_Butter

import pytest


def test_construction():
	"""
	Test the constructor
	"""
	# test non-consistency size
	with pytest.raises(ValueError):
		Filter(num=[1, 2, 3], den=[0, 6, 7])		# den[0] cannot be zero
	# with pytest.raises(ValueError):
	# 	Filter(num=[1, 2, 3], den=[1, 2])		# num should not be longer than den

	# test non-consistency size
	with pytest.raises(ValueError):
		Filter(A=[[1, 2], [3, 4], [5, 6]], B=1, C=2, D=3)
	with pytest.raises(ValueError):
		Filter(A=[[1, 2], [3, 4]], B=1, C=2, D=3)
	with pytest.raises(ValueError):
		Filter(A=[[1, 2], [3, 4]], B=[[1], [2]], C=2, D=3)
	with pytest.raises(ValueError):
		Filter(A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2], [1, 2]], D=3)

	with pytest.raises(ValueError):
		Filter(A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2]], num=[1, 2, 3])

	Filter(A=[[1, 2], [3, 4]], B=[[1], [2]], C=[[1, 2]], D=3, num=[1, 2, 3], den=[0, 6, 7])


@pytest.mark.parametrize("H", iter_random_Butter(20, onlyEven=True), ids=lambda x: x.name)
def test_butter(H):
	print(H.dTF)


@pytest.mark.parametrize("H", iter_random_Filter(20, seeded=True, ftype='all'), ids=lambda x: x.name)
def test_randomFilter(H):

	F = random_Filter(name=H.name)
	F.dSS.assert_close(H.dSS)
