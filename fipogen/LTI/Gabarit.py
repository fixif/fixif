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
from scipy.signal import iirdesign
from numpy import atleast_1d, array


import sollya


class Gabarit(object):
	"""
	A Gabarit object represents ...
	"""

	def __init__(self, Fs, Fstop, Fpass, Astop, Apass):
		"""

		Parameters:
		----------
		- Fs: (float) sampling frequency
		- Fstop: (float or list of 2 floats) stop band frequency(ies)
		- Fpass: (float or list of 2 floats) pass frequency(ies)
		- Astop: (float) attenuation in the stop band (in dB)
		- Apass: (float) attenuation in the pass band (in dB)

		"""
		self._Fs = Fs
		self._Fstop = copy(Fstop)
		self._Fpass = copy(Fpass)
		self._Astop = Astop
		self._Apass = Apass

		# determine the type (lowpass, highpass, bandstop, bandpass)
		# from
		Fpass = atleast_1d(Fpass)
		Fstop = atleast_1d(Fstop)
		band_type = 2 * (len(Fpass) - 1)
		band_type += 1
		if Fpass[0] >= Fstop[0]:
			band_type += 1
		self._band = {1: 'lowpass', 2: 'highpass',3: 'bandstop', 4: 'bandpass'}[band_type]


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
		wp = 2 * float(self._Fpass) / self._Fs
		ws = 2 * float(self._Fstop) / self._Fs

		num, den = iirdesign(wp, ws, self._Apass, self._Astop, ftype=ftype)
		return dTF(num, den)




	def check_dTF(self, tf):
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
		num = sollya.horner(sum(float(x) * sollya._x_ ** i for i, x in enumerate(array(tf.num)[0,:])))
		den = sollya.horner(sum(float(x) * sollya._x_ ** i for i, x in enumerate(array(tf.den)[0,:])))

		# build the constraints to verify
		constraints = []
		if self._band == 'lowpass':
			constraints.append( self._SollyaPassConstraint(0, self._Fpass) )
			constraints.append( self._SollyaStopConstraint(self._Fstop, None))
		elif self._band == 'highpass':
			constraints.append(self._SollyaStopConstraint(0, self._Fstop) )
			constraints.append( self._SollyaPassConstraint(self._Fpass, None))
		elif self._band == 'passband':
			constraints.append(self._SollyaStopConstraint(0, self._Fstop[0]) )
			constraints.append( self._SollyaPassConstraint(self._Fpass[0], self._Fpass[1]) )
			constraints.append(self._SollyaStopConstraint(self._Fstop[1], None))
		elif self._band == 'stopband':
			constraints.append(self._SollyaPassConstraint(0, self._Fpass[0]) )
			constraints.append( self._SollyaStopConstraint(self._Fstop[0], self._Fstop[1]) )
			constraints.append(self._SollyaPassConstraint(self._Fpass[1], None))

		# run sollya check
		res = sollya.parse("checkModulusFilterInSpecification")(num, den, constraints)
		sollya.parse("presentResults")(res)

		return True # res.okay



	def _SollyaPassConstraint(self, F1, F2, maxPass=0):
		"""
		Build a dictionary (for Sollya) of pass band from F1 to F2

		Parameters:
		- F1, F2: frequencies of the pass band  (F2==None means that F2=Fs/2 (but we do have to ensure the correct division by 2)
		- maxPass: in dB

		Returns a dictionary with Omega, omegaFactor, betaInf and betaSup
		"""
		Apass = sollya.double(self._Apass)
		Gpass = sollya.double(maxPass)
		Omega = sollya.Interval(2*sollya.double(F1)/self._Fs, 2*sollya.double(F2)/self._Fs if F2 else sollya.double(1))
		return {"Omega": Omega, "omegaFactor": sollya.pi, "betaInf": 10**(-Apass/20), "betaSup": 10**(Gpass/20)}


	def _SollyaStopConstraint(self, F1, F2):
		"""
		Build a dictionary (for Sollya) of strop band from F1 to F2

		Parameters:
		- F1, F2: frequencies of the stop band

		Returns a dictionary with Omega, omegaFactor, betaInf and betaSup
		"""
		Astop = sollya.double(self._Astop)
		Omega = sollya.Interval(2*sollya.double(F1)/self._Fs, 2*sollya.double(F2)/self._Fs)
		return {"Omega": Omega, "omegaFactor": sollya.pi, "betaInf": 0, "betaSup": 10**(-Astop/20)}