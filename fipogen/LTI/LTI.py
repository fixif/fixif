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


from fipogen.LTI import dTF, dSS

class LTI(object):
	"""
	A LTI (Linear Time Invariant) object is described either a transfer function and state-space
	"""
	def __init__(self, num=None, den=None, A=None, B=None, C=None, D=None):
		"""
		Create a LTI from numerator and denominator OR from A,B,C,D matrices
		Parameters
		----------
		num, den: numerator and denominator of the transfer function
		A,B,C,D: State-Space matrices
		"""
		self._dSS = None
		self._dTF = None

		if A is not None and B is not None and C is not None and D is not None:
			self._dSS = dSS( A, B, C, D)
		elif num is not None and den is not None:
			self._dTF = dTF( num, den)
		else:
			raise ValueError( 'LTI: the values given to the LTI constructor are not correct')


	@property
	def dSS(self):
		if self._dSS is None:
			self._dSS = self._dTF.to_dSS()
		return self._dSS


	@property
	def dTF(self):
		if self._dTF is None:
			self._dTF = self._dSS.to_dTF()
		return self._dTF
