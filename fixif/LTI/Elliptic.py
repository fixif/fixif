# coding=utf-8

"""
This file contains Object and methods for a elliptic filter
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from numpy.random.mtrand import randint, seed as numpy_seed, choice, random_sample		# seed is renamed numpy_seed, so that I can use the variable seed
from scipy.signal import ellip

from fixif.LTI import Filter


def quantify(x, q):
	"""quantize a number"""
	return round(x*q)/q


class Elliptic(Filter):

	def __init__(self, n, rp, rs, Wn, etype='low', name='Elliptic'):
		"""
		Create an elliptic filter
		Use the same argument as scipy.signal elliptic filter

		n: (int)The order of the filter.
		rp: (float) The maximum ripple allowed below unity gain in the passband. Specified in decibels, as a positive number.
		rs: (float) The minimum attenuation required in the stop band. Specified in decibels, as a positive number.
		Wn : (array_like) A scalar or length-2 sequence giving the critical frequencies. For elliptic filters, this is the point in the transition band at which the gain first drops below -rp. For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample. (Wn is thus in half-cycles / sample.) For analog filters, Wn is an angular frequency (e.g. rad/s).

		btype: (string) {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}: the type of filter. Default is ‘lowpass’.

		see `https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.signal.ellip.html`

		Returns a Elliptic object (Filter)
		"""

		self.n = n
		self.rp = rp
		self.rs = rs
		self.Wn = Wn
		self.etype = etype

		# call the parent class constructor
		num, den = ellip(n, rp, rs, Wn, etype)
		super(Elliptic, self).__init__(num=num, den=den, stable=True, name=name)





def iter_random_Elliptic(number, n=(5, 10), rp=(0,10), rs=(30,80), Wc=(0.1, 0.8), W1=(0.1, 0.5), W2=(0.5, 0.8), form=None, seeded=True, quant=None):
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
		- quant: quantized the coefficients with quant bits (None by default -> no quantization)
		- seeded: (boolean) indicates if the random  should be done with a particular seed or not (in order to be reproductible, the seed is stored in the name of the filter)

	"""
	seeds = [randint(0, 1e9) if seeded else None for _ in range(number)]  # generate a particular seed for each random dSS, or None (if seeded is set to False)
	for s in seeds:
		yield random_Elliptic(n=n, rp=rp, rs=rs, Wc=Wc, W1=W1, W2=W2, form=form, seed=s, quant=quant)



def random_Elliptic(n=(5, 10), rp=(10,50), rs=(10,50), Wc=(0.1, 0.8), W1=(0.1, 0.5), W2=(0.5, 0.8), form=None, seed=None, quant=None):
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
		- quant: quantized the coefficients with quant bits (None by default -> no quantization)
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
			raise ValueError("iter_random_Elliptic: W1 should be lower than W2")
		Wn1 = (W1[1] - W1[0]) * random_sample() + W1[0]
		Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
		while Wn2 <= Wn1:
			Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
		W = [Wn1, Wn2]
	else:
		# choose 1 frequency
		W = (Wc[1] - Wc[0]) * random_sample() + Wc[0]
	# choose rp and rs
	rip = (rp[1]-rp[0]) * random_sample() + rp[0]
	rst = (rs[1] - rs[0]) * random_sample() + rs[0]
	# choose order
	order = randint(*n)
	# do we quantified the parameter (to be able to print them exactly, for example)
	if quant:
		rip = quantify(rip, quant)
		rst = quantify(rst, quant)
		if isinstance(W, list):
			W = [quantify(W[0], quant), quantify(W[1], quant)]

	return Elliptic(order, rp=rip, rs=rst, Wn=W, etype=form, name='Elliptic-random-%d' % seed)



