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


from fipogen.LTI import dTF, dTFmp
from fipogen.func_aux import mpf_matrix_to_sollya, MatlabHelper

from scipy.signal import iirdesign, freqz
from numpy import array, pi, log10
from numpy.random import seed as set_seed, choice, randint, uniform

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import mpmath
import sollya





class Band(object):
	"""A band is a zone in frequency (between two frequencies in Hz), with a gain in an interval or lower than a value
	It could be a pass band (gain in [G1;G2]) or astop band (gain<G)
	Gains are in dB, frequencies in Hz (except if Fs is None, otherwise frequencies are Nyquist normalised frequencies)
	"""
	def __init__(self, Fs, F1, F2, Gain):
		"""
		Constructor of a band (a pass band or a stop band)
		Parameters:
		- Fs: sampling Frequency (Hz), None if unspecified
			(then the frequencies are Nyquist normalised frquencies, between 0 and 1)
		- F1,F2: frequencies of the band (F2 can be None, to indicate F2 = Fs/2)
		- Gain: Gain (in dB) of the band -> negative for attenuation !!
			CONVENTION: a 2-tuple for pass Band, or a float for stop Band
		"""
		self._Fs = Fs if Fs else 2
		self._F1 = F1
		self._F2 = F2
		if isinstance(Gain, (tuple, list)):
			# pass band (the gains are sorted)
			self._stopGain = None
			self._passGains = (Gain[0],Gain[1]) if Gain[0]<Gain[1] else (Gain[1],Gain[0])
		else:
			# stop band
			self._stopGain = Gain
			self._passGains = None

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
		return 2*float(self._F2)/self._Fs if self._F2 else 1

	@property
	def passGains(self):
		return self._passGains

	@property
	def stopGain(self):
		return self._stopGain

	@property
	def isPassBand(self):
		"""is the band a pass band ?"""
		return bool(self._passGains)        # True if not None or 0

	def __lt__(self, other):
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

	def sollyaConstraint(self,bound, dBmargin):
		"""
		Returns a dictonary for sollya checkModulusFilterInSpecification
		"""
		w1 = 2*sollya.SollyaObject(self._F1)/self._Fs
		w2 = 2*sollya.SollyaObject(self._F2)/self._Fs if self._F2 else 1    # F2==None -> F2=Fs/2, so w2=1
		bound = sollya.SollyaObject(bound)

		if self.isPassBand:
			# pass band
			betaInf = 10 ** ((sollya.SollyaObject(self._passGains[0]) - dBmargin) / 20) + bound
			betaSup = 10 ** ((sollya.SollyaObject(self._passGains[1]) + dBmargin) / 20) - bound
		else:
			# stop band
			betaInf = bound
			betaSup = 10 ** ((sollya.SollyaObject(self._stopGain)+dBmargin) / 20) - bound

		return {"Omega": sollya.Interval(w1, w2), "omegaFactor": sollya.pi, "betaInf": betaInf, "betaSup": betaSup}

	def Rectangle(self, minG):
		"""
		Returns a rectangle object, to be used with matplotlib
		The rectangle corresponds to the (stop/pass) band to draw on a Bode diagram
		Parameters:
		- minG: minimum y-value for the plot
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
		Build a Gabarit, from list of bands, and list of amplitudes (in dB)
		Parameters:
		----------
		- Fs: (float) sampling frequency (set to None or .5 if the Frequency are Nyquist frequencies, between 0 and 1)
		- Fbands: list of bands (a band is a tuple (F1,F2); F2 may be None to indicates that it is the end of the band (=Fs/2))
		- Abands: list of amplitudes (in dB)
				for pass band, the amplitude is a tuple (x,y) --> the amplitude must be between x dB and y dB
				for stop band, the amplitude is a float x --> the amplitude must be lower than x dB
		- seed: seed used to generate it (not used, just stored for the record)
		"""
		# sampling frequency
		self._Fs = Fs

		if len(Fbands) != len(Abands):
			raise ValueError("Fbands and Abands should be lists/tuples with same size")

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
		# determine the type from the list of pass/stop bands
		if self._type is None:
			passBands = [b.isPassBand for b in self._bands]
			if len(self._bands) == 2 and passBands == [True, False]:
				self._type = 'lowpass'
			elif len(self._bands) == 2 and passBands == [False, True]:
				self._type = 'highpass'
			elif len(self._bands) == 3 and passBands == [True, False, True]:
				self._type = 'bandstop'
			elif len(self._bands) == 3 and passBands == [False, True, False]:
				self._type = 'bandpass'
			else:
				self._type = 'multiband'

		return self._type

	@property
	def bands(self):
		return self._bands

	def to_dTF(self, ftype='butter', method='scipy'):
		"""
		This methods HELPS to find a transfer function that *should* satisfy the gabarit
		It is just here to quickly determine a transfer function that satisfy the gabarit in a simple way
		But it cannot handle all the options these tools (matlab/scipy) offer (the best is to use these tools the way
		you want, with all the possible options, and then to check if the transfer function fulfills the gabarit

		Parameters:
		-ftype : (str) the type of IIR filter to design:
			- Butterworth   : 'butter'
			- Chebyshev I   : 'cheby1'
			- Chebyshev II  : 'cheby2'
			- Cauer/elliptic: 'ellip'
			- Bessel/Thomson: 'bessel'
		- method: (string) the method used ('scipy' for scipy.signal.iirdesign, or 'matlab' for matlab fdesign functions)

		Returns a transfer function (dTF object)
		"""
		# Start Matlab if needed
		matlabEng = None
		if method=='matlab':
			MH = MatlabHelper()
			matlabEng = MH.engine

		# normalize bands (with pass gain centered in 0dB)
		centerPassGain = max( (b.passGains[0]+b.passGains[1])/2.0 for b in self._bands if b.isPassBand )
		bands = [ b-centerPassGain for b in self._bands ]

		# arguments for matlab/scipy functions, for each type of band
		if self.type=='lowpass':
			passb, stopb = bands
			matlabParams = [passb.w2, stopb.w1, -passb.passGains[0], -stopb.stopGain]
			scipyParams = [passb.w2, stopb.w1, -passb.passGains[0], -stopb.stopGain]

		elif self.type == 'highpass':
			stopb, passb = bands
			matlabParams = [stopb.w2, passb.w1, -stopb.stopGain, -passb.passGains[0]]
			scipyParams = [passb.w1, stopb.w2, -passb.passGains[0], -stopb.stopGain]

		elif self.type == 'bandpass':
			stop1b, passb, stop2b = bands
			matlabParams = [stop1b.w2, passb.w1, passb.w2, stop2b.w1, -stop1b.stopGain, -passb.passGains[0], -stop2b.stopGain]
			scipyParams = [[passb.w1, passb.w2], [stop1b.w2, stop2b.w1], -passb.passGains[0], -stop1b.stopGain]
			if not matlabEng and stop1b.stopGain != stop2b.stopGain:
					raise ValueError("Scipy cannot handle bandpass when the two stop band have different gains")

		# elif self.type == 'bandstop':
		# 	pass1b, stopb, pass2b = bands
		# 	matlabParams = [stop1b.w2, passb.w1, passb.w2, stop2b.w1, -stop1b.stopGain, -passb.passGains[1], -stop2b.stopGain]
		# 	scipyParams = [[passb.w1, passb.w2], [stop1b.w2, stop2b.w1], -passb.passGains[1], -stop1b.stopGain]

		else:
			raise ValueError("Cannot (yet) handle multibands gabarit.")

		# call matlab or scipy methods
		if matlabEng:
			# call fdesign.lowpass/highpass/bandpass/bandstop functions, according to self.type
			try:
				de = matlabEng.fdesign.__getattr__(self.type)(*matlabParams)
				h = matlabEng.design(de, ftype,'SystemObject',1)
			except Exception as e:
				raise ValueError("Matlab cannot deal with the following gabarit:\n%s\n%s"%(self,e), exc_info=True)
			numM,denM = matlabEng.tf(h, nargout=2)
			# transform to numpy array
			num = array(numM._data.tolist())
			den = array(denM._data.tolist())
		else:
			num, den = iirdesign(*scipyParams, analog=False, ftype=ftype)

		# go back to pass gain not centered in 0dB
		num = num*10**(centerPassGain/20.0)

		return dTF(num, den)


	def plot(self, tf=None):
		"""
		Plot a gabarit, and a transfer function (if given)
		"""
		minG = -200
		if tf:
			w, h = freqz(tf.num.transpose(), tf.den.transpose())
			plt.plot( (self._Fs * 0.5 / pi) * w, 20*log10(abs(h)) )
			minG = min(20*log10(abs(h)))

		currentAxis = plt.gca()
		for b in self._bands:
			currentAxis.add_patch( b.Rectangle(minG))

		plt.show()



	def check_dTF(self, tf, bound=0, dBmargin=0):
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
		constraints = [b.sollyaConstraint(bound, dBmargin) for b in self._bands]

		# run sollya check
		res = sollya.parse("checkModulusFilterInSpecification")(num, den, constraints)
		sollya.parse("presentResults")(res)

		return dict(res)["okay"]



def parse_results(d):
	if sollya.length(d['results']) != 2:
		raise ValueError('Result dictionnary must have length = 2')

	#parsing the result for the polynomial p






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