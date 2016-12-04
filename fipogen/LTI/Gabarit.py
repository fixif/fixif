# coding: utf8

"""
This file contains the class Gabarit for a freq. specification
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from copy import copy
from fipogen.LTI import dTF
from scipy.signal import iirdesign, freqz
from numpy import atleast_1d, array, pi,log

#import matplotlib.pyplot as plt
#from matplotlib.patches import Rectangle

import sollya

class Band(object):
	"""Normalized band
	pass band or stop band"""
	def __init__(self, w1, w2, Gain):
		self._w1 = w1
		self._w2 = w2
		self._Gain = Gain

	@property
	def w1(self):
		return self._w1

	@property
	def w2(self):
		return self._w2

	@property
	def Gain(self):
		return self._Gain

	@property
	def isPassBand(self):
		"""is the band a pass band ?"""
		return isinstance(self._Gain,(tuple,list))

	def __le__(self, other):
		"""compare two bands"""
		return self.w1 < other.w1

	def __sub__(self,other):
		"""Substract a Band and a Gain"""
		return Band(self._w1, self._w2, self._Gain-other if not self.isPassBand else (self._Gain[0]-other, self._Gain[1]-other))

	def sollyaConstraint(self,eps):
		"""
		Returns a dictonary for sollya checkModulusFilterInSpecification
		"""
		w1 = sollya.SollyaObject(self.w1)
		w2 = sollya.SollyaObject(self.w2)
		eps = sollya.SollyaObject(eps)

		if self.isPassBand:
			# pass band
			betaInf = 10 ** (sollya.SollyaObject(self.Gain[1]) / 20)*(1-eps)
			betaSup = 10 ** (sollya.SollyaObject(self.Gain[0]) / 20)*(1+eps)
		else:
			betaInf = 0
			betaSup = 10 ** (sollya.SollyaObject(self.Gain) / 20)

		return {"Omega": sollya.Interval(w1, w2), "omegaFactor": sollya.pi, "betaInf": betaInf, "betaSup": betaSup}


class Gabarit(object):
	"""
	A Gabarit object represents a freq. specification
	It is decomposed in bands, that can be pass-band (amplitude in [x;y]) or stop-band (amplitude less than z)
	"""

	def __init__(self, Fs, Fbands, Abands):
		"""

		Parameters:
		----------
		- Fs: (float) sampling frequency (set to None or .5 if the Frequency are Nyquist frequencies, between 0 and 1)
		- Fbands: list of bands (a band is a tuple (F1,F2); F2 may be None to indicates that it is the end of the band (=Fs/2))
		- Abands: list of amplitudes (in dB)
				for pass band, the amplitude is a tuple (x,y) --> the amplitude must be between x dB and y dB
				for stop band, the amplitude is a float x --> the amplitude must be lower than x dB
		"""
		# sampling frequency
		self._Fs = Fs if Fs else .5

		# store the bands (sorted)
		self._bands = [ Band(2.0*F1/self._Fs, 2.0*F2/self._Fs if F2 else 1, G) for (F1,F2),G in zip(Fbands, Abands) ]       # division par Fs, est-ce à faire dans sollya ?
		self._bands.sort()

		self._type = None


	@property
	def type(self):
		"""
		Returns the type of gabarit (lowpass, highpass, stopband, passband or multiband)
		Determine the type if it is not yet determined
		"""
		if self._type is None:
			passBands = [b.isPassBand for b in self._bands]
			if len(self._bands) == 2 and passBands == [True, False]:
				self._type = 'lowpass'
			else:
				self._type = 'multiband'
		return self._type

	def to_dTF(self, ftype='butter'):
		"""
		Returns a transfer function (dTF object) that *should* satisfy the gabarit
		using scipy.signal.iirdesin

		Parameters:
		ftype : (str) the type of IIR filter to design:
		- Butterworth   : 'butter'
		- Chebyshev I   : 'cheby1'
		- Chebyshev II  : 'cheby2'
		- Cauer/elliptic: 'ellip'
		- Bessel/Thomson: 'bessel'
		"""

		if self.type=='lowpass':
			# lowpass
			passb, stopb = self._bands
			#gain = passb.Gain[0]
			#passb = passb - gain
			#stopb = stopb - gain
			num, den = iirdesign(passb.w2, stopb.w1, -passb.Gain[1], -stopb.Gain, analog=False, ftype=ftype)
		else:
			raise ValueError("Not yet implemented")

		return dTF(num, den)


	def plot(self, tf=None):
		"""Plot a gabarit"""
		if tf:
			w, h = freqz(tf.num.transpose(), tf.den.transpose())
			plt.plot( (self._Fs * 0.5 / pi) * w, 20*log(abs(h)) )

		currentAxis = plt.gca()
		for b in self._bands:
			if b.isPassBand:
				currentAxis.add_patch(Rectangle((b.w1*.5*self._Fs, b.Gain[0]), (b.w2-b.w1)*.5*self._Fs, b.Gain[1]-b.Gain[0], facecolor="red", alpha=0.3))
			else:
				currentAxis.add_patch(Rectangle((b.w1 * .5 * self._Fs, b.Gain), (b.w2 - b.w1) * .5 * self._Fs, -1e3, facecolor="red", alpha=0.3))

		plt.show()

	def check_dTF(self, tf, eps=0):
		"""
		Check if a transfer function satisfy the Gabarit
		This is done using Sollya and gabarit.sol

		Parameters:
		- tf: (dTF) transfer function we want to check

		Returns a boolean (display feedback?)
		"""

		# load gabarit.sol
		sollya.suppressmessage(57, 174, 130, 457)
		sollya.execute("fipogen/LTI/gabarit.sol")

		# build sollya objects
		num = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(array(tf.num)[0,:])))
		den = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(array(tf.den)[0,:])))

		# build the constraints to verify
		constraints = [b.sollyaConstraint(eps) for b in self._bands]

		# run sollya check
		res = sollya.parse("checkModulusFilterInSpecification")(num, den, constraints)
		sollya.parse("presentResults")(res)

		return dict(res)["okay"]
