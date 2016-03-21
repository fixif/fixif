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

from fipogen.LTI import dSS,dTF
from scipy.signal import butter


class LTI(object):
	"""
	A LTI (Linear Time Invariant) object is described either a transfer function and state-space
	"""
	def __init__(self, num=None, den=None, A=None, B=None, C=None, D=None, tf=None, ss=None, stable=None):
		"""
		Create a LTI from numerator and denominator OR from A,B,C,D matrices
		Parameters
		----------
		num, den: numerator and denominator of the transfer function
		A,B,C,D: State-Space matrices
		dTF: a dTF object
		dSS: a dSS object
		"""
		self._dSS = None
		self._dTF = None

		if A is not None and B is not None and C is not None and D is not None:
			self._dSS = dSS( A, B, C, D)
		elif num is not None and den is not None:
			self._dTF = dTF( num, den)
		elif tf is not None:
			self._dTF = tf
		elif ss is not None:
			self._dSS = ss
		else:
			raise ValueError( 'LTI: the values given to the LTI constructor are not correct')

		# is the filter stable?
		if stable is None:
			#TODO: compute the eigenvalues to know if it is stable or not
			self._stable = False
		else:
			self._stable = stable



	@property
	def dSS(self):
		if self._dSS is None:
			self._dSS = self._dTF.to_dSS()
		return self._dSS


	@property
	def dTF(self):
		if not self.isSISO():
			raise ValueError( 'LTI: cannot convert a MIMO filter to dTF (not yet)')
		if self._dTF is None:
			self._dTF = self._dSS.to_dTF()
		return self._dTF


	def isSISO(self):
		"""
		Returns True if the lti filter is a Single Input Single Output filter
		"""
		if self._dTF or self._dSS.D.shape == (1,1):
			return True
		else:
			return False


	def isStable(self):
		"""
		Returns True if the filter is known to be stable
		"""
		return self._stable


	def isButter(self):
		"""
		Returns True if the filter is known to be a Butterworth filter
		"""
		return self.__class__ == Butter



class Butter(LTI):

	def __init__(self, n, Wn, btype='low'):
		"""
		Create a Butterworth filter
		Parameters
		----------
		N: (int) The order of the filter
		W: (array-like) A scalar or length-2 sequence giving the critical frequencies. For a Butterworth filter, this is the point at which the gain drops to 1/sqrt(2) that of the passband (the “-3 dB point”). For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample. (Wn is thus in half-cycles / sample.) For analog filters, Wn is an angular frequency (e.g. rad/s).

		btype: (string) {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter (default is ‘lowpass’)

		see `http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html`

		Returns a Butter object (LTI)
		"""
		self._stable = True
		self._butterworth = True
		self._dSS = None
		num, den = butter(n, Wn, btype)
		self._dTF = dTF( num, den)

		self.n = n
		self.Wn = Wn
		self.btype = btype
