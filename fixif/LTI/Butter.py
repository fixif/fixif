# coding: utf8

"""
This file contains Object and methods for a Butterworth filter
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from numpy.random.mtrand import randint, seed as numpy_seed, choice, random_sample		# seed is renamed numpy_seed, so that I can use the variable seed
from scipy.signal import butter

from fixif.LTI import Filter


class Butter(Filter):

	def __init__(self, n, Wn, btype='low', name='Butterworth'):
		"""
		Create a Butterworth filter
		Parameters
		----------
		n: (int) The order of the filter
		Wn: (array-like) A scalar or length-2 sequence giving the critical frequencies. For a Butterworth filter, this is the point at which the gain drops to 1/sqrt(2) that of the passband (the “-3 dB point”). For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample. (Wn is thus in half-cycles / sample.) For analog filters, Wn is an angular frequency (e.g. rad/s).

		btype: (string) {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter (default is ‘lowpass’)

		see `http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html`

		Returns a Butter object (Filter)
		"""

		self._butterworth = True
		self.n = n
		self.Wn = Wn
		self.btype = btype

		# call the parent class constructor
		num, den = butter(n, Wn, btype)
		super(Butter, self).__init__(num=num, den=den, stable=True, name=name)





def iter_random_Butter(number, n=(5, 10), Wc=(0.1, 0.8), W1=(0.1, 0.5), W2=(0.5, 0.8), form=None, onlyEven=True, seeded=True):
	"""
	Generate some n-th order Butterworh filters
	Parameters
		----------
		- number: number of Butterworth filters generated
		- n: (int) The order of the filter
		- Wc: used if btype is 'lowpass' or 'highpass'
			Wc is a tuple (min,max) for the cut frequency
		- W1 and W2: used if btype is ‘bandpass’, ‘bandstop’
			W1 and W2 are tuple (min,max) for the two start/stop frequencies
		- form: (string) {None, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter. If None, the type is randomized
		- onlyEven: if True, only even order filter are generated
		- seeded: (boolean) indicates if the random dSS should be done with a particular seed or not (in order to be reproductible, the seed is stored in the name of the filter)

	"""
	seeds = [randint(0, 1e9) if seeded else None for _ in range(number)]  # generate a particular seed for each random dSS, or None (if seeded is set to False)
	for s in seeds:
		yield random_Butter(n=n, Wc=Wc, W1=W1, W2=W2, form=form, onlyEven=onlyEven, seed=s)



def random_Butter(n=(5, 10), Wc=(0.1, 0.8), W1=(0.1, 0.5), W2=(0.5, 0.8), form=None, onlyEven=True, seed=None):
	"""
	Generate a n-th order Butterworh filters
	Parameters
		----------
		- n: (int) The order of the filter
		- Wc: used if btype is 'lowpass' or 'highpass'
			Wc is a tuple (min,max) for the cut frequency
		- W1 and W2: used if btype is ‘bandpass’, ‘bandstop’
			W1 and W2 are tuple (min,max) for the two start/stop frequencies
		- form: (string) {None, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter. If None, the type is randomized
		- onlyEven: if True, only even order filter are generated
		- seed: if not None, indicates the seed toi use for the random part (in order to be reproductible, the seed is stored in the name of the filter)
	"""
	# change the seed if asked
	if seed:
		numpy_seed(seed)
	# choose a form if asked
	if form is None:
		form = choice(("lowpass", "highpass", "bandpass", "bandstop"))
	# choose Wn
	if form in ("bandpass", "bandstop"):
		# choose 2 frequencies
		if W2[1] <= W1[0]:
			raise ValueError("iter_random_Butter: W1 should be lower than W2")
		Wn1 = (W1[1] - W1[0]) * random_sample() + W1[0]
		Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
		while Wn2 <= Wn1:
			Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
		W = [Wn1, Wn2]
	else:
		# choose 1 frequency
		W = (Wc[1] - Wc[0]) * random_sample() + Wc[0]
	# choose order
	order = randint(*n)
	if onlyEven and order % 2 == 0:
		order += 1

	return Butter(order, W, form, name='Butterworth-random-%d' % seed)
