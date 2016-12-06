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
from fipogen.LTI import dTF, dTFmp
from scipy.signal import iirdesign, freqz
from numpy import atleast_1d, array, pi,log10
from numpy.random import seed as set_seed, choice, randint, uniform
from fipogen.func_aux import mpf_matrix_to_sollya

import mpmath

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import sollya


class Band(object):
	"""A band is a zone in frequency (between two frequencies in Hz), with a gain in an interval or lower than a value
	It could be a pass band (gain in [G1;G2]) or astop band (gain<G)
	Gains are in dB, frequencies in Hz (except if Fs is None, otherwise frequencies are Nyquist normalised frequencies)
	"""
	def __init__(self, Fs, F1, F2, Gain):
		"""
		Constructor
		Parameters:
		- Fs: sampling Frequency (Hz), None if unspecified
			(then the frequencies are Nyquist normalised frquencies, between 0 and 1)
		- F1,F2: frequencies of the band (F2 can be None, to indicate F2 = Fs/2)
		- Gain: Gain (in dB) of the band -> negative for attenuation !!
			a 2-tuple for pass Band, or a float for stop Band
		"""
		self._Fs = Fs if Fs else 2
		self._F1 = F1
		self._F2 = F2
		self._stopGain = Gain if not isinstance(Gain, (tuple, list)) else None
		self._passGains = Gain if isinstance(Gain, (tuple, list)) else None

	@property
	def Fs(self):
		return self._Fs

	@property
	def F1(self):
		return self._F1

	@property
	def F2(self):
		return self._F2 if self._F2 else float(self._Fs/2)

	@property
	def w1(self):
		"""Normalized frequency (approx. due to the division)"""
		return 2*float(self._F1)/self._Fs

	@property
	def w2(self):
		"""Normalized frequency (approx. due to the division)"""
		return 2*float(self._F2)/self._Fs

	@property
	def passGains(self):
		return self._passGains

	@property
	def stopGain(self):
		return self._stopGain

	@property
	def isPassBand(self):
		"""is the band a pass band ?"""
		return bool(self._passGains)

	def __le__(self, other):
		"""compare two bands"""
		return self.F1 < other.F1

	def __sub__(self,other):
		"""Substract a Band and a Gain"""
		try:
			stopGain = self._stopGain-other if self._stopGain else None
			passGains = (self._passGains[0]-other, self._passGains[1]-other) if self._passGains else None
		except Exception as e:
			raise ValueError("The gain should be a constant")
		return Band(self._Fs, self._F1, self._F2, passGains or stopGain)

	def __repr__(self):
		return "Band(%s,%s,%s,stopGain=%s,passGains=%s)" % (self.Fs, self.F1, self.F2, self._stopGain, self._passGains)

	def __str__(self):
		if self.isPassBand:
			return "Freq. [%sHz,%sHz]: Passband in [%sdB, %sdB]"%(self.F1, self.F2, self._passGains[0], self._passGains[1])
		else:
			return "Freq. [%sHz,%sHz]: Stopband at %sdB"%(self.F1, self.F2, self._stopGain)

	def sollyaConstraint(self,bound):
		"""
		Returns a dictonary for sollya checkModulusFilterInSpecification
		"""
		w1 = 2*sollya.SollyaObject(self._F1)/self._Fs
		w2 = 2*sollya.SollyaObject(self._F2)/self._Fs if self._F2 else 1    # F2==None -> F2=Fs/2, so w2=1
		bound = sollya.SollyaObject(bound)

		if self.isPassBand:
			# pass band
			betaSup = 10 ** (sollya.SollyaObject(self._passGains[0]) / 20) - bound
			betaInf = 10 ** (sollya.SollyaObject(self._passGains[1]) / 20)+bound
		else:
			betaInf = 0
			betaSup = 10 ** (sollya.SollyaObject(self._stopGain) / 20)+bound

		return {"Omega": sollya.Interval(w1, w2), "omegaFactor": sollya.pi, "betaInf": betaInf, "betaSup": betaSup}

	def Rectangle(self, minG):
		"""
		Returns a rectangle to be used with matplotlib, corresponding to the band
		minG: minimum y-value for the plot
		"""

		if self.isPassBand:
			return Rectangle((self.F1, self.passGains[0]), (self.F2 - self.F1), self.passGains[1] - self.passGains[0], facecolor="red", alpha=0.3)
		else:
			return Rectangle((self.F1, self.stopGain), self.F2 - self.F1, minG, facecolor="red", alpha=0.3)



class Gabarit(object):
	"""
	A Gabarit object represents a freq. specification
	It is decomposed in bands, that can be pass-band (amplitude in [x;y]) or stop-band (amplitude less than z)
	"""

	def __init__(self, Fs, Fbands, Abands, seed=None):
		"""

		Parameters:
		----------
		- Fs: (float) sampling frequency (set to None or .5 if the Frequency are Nyquist frequencies, between 0 and 1)
		- Fbands: list of bands (a band is a tuple (F1,F2); F2 may be None to indicates that it is the end of the band (=Fs/2))
		- Abands: list of amplitudes (in dB)
				for pass band, the amplitude is a tuple (x,y) --> the amplitude must be between x dB and y dB
				for stop band, the amplitude is a float x --> the amplitude must be lower than x dB
		- seed: seed used to generate it (not used, just stored)
		"""
		# sampling frequency
		self._Fs = Fs

		# store the bands (sorted)
		self._bands = [ Band(Fs, F1, F2, G) for (F1,F2),G in zip(Fbands, Abands) ]
		self._bands.sort()

		self._type = None
		self._seed = seed

	def __str__(self):
		seed = "Seed=%s\n"%(self._seed) if self._seed else ""
		return "%sType: %s (Fs=%sHz)\n%s"%(seed, self.type, self._Fs, "\n".join(str(b) for b in self._bands))

	@property
	def seed(self):
		return self._seed

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


	def to_dTF(self, ftype='butter', method='scipy'):
		"""
		Returns a transfer function (dTF object) that *should* satisfy the gabarit
		using scipy.signal.iirdesin

		Parameters:
		-ftype : (str) the type of IIR filter to design:
			- Butterworth   : 'butter'
			- Chebyshev I   : 'cheby1'
			- Chebyshev II  : 'cheby2'
			- Cauer/elliptic: 'ellip'
			- Bessel/Thomson: 'bessel'
		- method: (string) the method used ('scipy' for scipy.signal.iirdesign, or 'matlab' for )
		"""
		# Start Matlab if needed
		matlabEng = None
		if method=='matlab':
			from matlab.engine import start_matlab   # http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
			matlabEng = start_matlab()
			# TODO: avoir une class MatlbabHelper, qui permet de n'avoir qu'une seule instance d'engine matlab pour ne pas avoir à la redémarrer à chaque fois

		gain = 0
		if self.type=='lowpass':
			# lowpass
			passb, stopb = self._bands
			gain = passb.passGains[0]
			passb = passb - gain
			stopb = stopb - gain

			if matlabEng:
				de = matlabEng.fdesign.lowpass(passb.F2, stopb.F1, -passb.passGains[1], -stopb.stopGain, self._Fs)
			else:
				num, den = iirdesign(passb.w2, stopb.w1, -passb.passGains[1], -stopb.stopGain, analog=False, ftype=ftype)


		if matlabEng:
			h = matlabEng.design(de, ftype,'SystemObject',1)
			numM,denM = matlabEng.tf(h, nargout=2)
			# transform to numpy array
			num = array(numM._data.tolist())
			den = array(denM._data.tolist())


		num = num*10**(gain/20.0)

		return dTF(num, den)


	def plot(self, tf=None):
		"""Plot a gabarit"""
		minG = -200
		if tf:
			w, h = freqz(tf.num.transpose(), tf.den.transpose())
			plt.plot( (self._Fs * 0.5 / pi) * w, 20*log10(abs(h)) )
			minG = min(20*log10(abs(h)))

		currentAxis = plt.gca()
		for b in self._bands:
			currentAxis.add_patch( b.Rectangle(minG))

		plt.show()

	def check_dTF(self, tf, bound=0):
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

		if isinstance(tf.num[0,0], mpmath.mpf):
			tf_num_sollya, len_num, _ = mpf_matrix_to_sollya(tf.num)
			tf_den_sollya, len_den, _ = mpf_matrix_to_sollya(tf.den)
			num = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(tf_num_sollya)))
			den = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(tf_den_sollya)))
		else:
		# build sollya objects
			num = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(array(tf.num)[0,:])))
			den = sollya.horner(sum(sollya.SollyaObject(x) * sollya._x_ ** i for i, x in enumerate(array(tf.den)[0,:])))

		# build the constraints to verify
		constraints = [b.sollyaConstraint(bound) for b in self._bands]

		# run sollya check
		res = sollya.parse("checkModulusFilterInSpecification")(num, den, constraints)
		sollya.parse("presentResults")(res)

		return dict(res)["okay"]




def iter_random_Gabarit( number, form=None):
	"""
	Generate some random gabarits
	Parameters
	- number: number of gabarit generated
	- form: (string) {None, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter. If None, the type is randomized
	"""
	for x in range(number):
		yield random_Gabarit(form=form)



def random_Gabarit(form=None, seed=None):
	"""
	Generate a random Gabarit
	Parameters:
	- form: (string) {None, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter. If None, the type is randomized
	- seed: if not None, indicates the seed to use for the random part (in order to be reproductible, the seed is stored in the name of the gabarit)
	"""
	# change the seed if asked (otherwise, set the seed)
	if not seed:
		set_seed(None)  # (from doc):  If seed is omitted or None, current system time is used
		seed = randint(0, 16777215)  # between 0 and 2^24-1
	set_seed(seed)

	# choose a form if asked
	if form is None:
		#form = choice(("lowpass", "highpass", "bandpass", "bandstop"))
		form = choice(("lowpass"))

	Fs = randint(500,100000)
	bands = []
	Gains = []

	# lowpass
	if form=='lowpass':
		Fpass = uniform(0.01,0.9)*Fs/2  # Wpass between 0.01 and 0.9
		Fstop = uniform(Fpass,Fs/2)     # Wstop between Wpass and 1
		gp = uniform(-5,5)              # upperband for pass in [-5;5]
		gps = uniform(0.1,5)            # pass width in [0.1;5]
		gs = uniform( -80, 2*(gp-gps))   # stop band in [-80 and 2*lowerband]
		bands = [ (0,Fpass), (Fstop,None) ]
		Gains = [ (gp, gp-gps), gs ]
	else:
		raise ValueError('The form is not valid')

	return Gabarit(Fs, bands, Gains, seed=seed)