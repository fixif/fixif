#coding=utf8

"""
This file contains a function to generate random Discrete State Spaces
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Richard Murray", "Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from fipogen.LTI import dSS, dTF, Butter

from numpy                  import zeros, dot, eye, pi, cos, sin
from numpy.random           import rand, randn, randint, choice, random_sample
from numpy.linalg           import solve, LinAlgError
from numpy import matrix as mat




def iter_random_dSS(number = 1, stable = True, n = (5, 10), p = (1, 5), q = (1, 5), pRepeat = 0.01, pReal = 0.5, pBCmask = 0.90, pDmask = 0.8, pDzero = 0.5):
	"""
	Generate some n-th order random (stable or not) state-spaces, with q inputs and p outputs
	copy/Adapted from control-python library (thanks guys): https://sourceforge.net/projects/python-control/
	possibly already adpated from Mathworks or Octave

	Parameters:
		- number: number of state-space to generate
		- stable: indicate if the state-spaces are stable or not
		- n: tuple (mini,maxi) number of states (default:  random between 5 and 10)
		- p: number of outputs (default: 1)
		- q: number of inputs (default: 1)

		- pRepeat: Probability of repeating a previous root (default: 0.01)
		- pReal: Probability of choosing a real root (default: 0.5). Note that when choosing a complex root, the conjugate gets chosen as well. So the expected proportion of real roots is pReal / (pReal + 2 * (1 - pReal))
		- pBCmask: Probability that an element in B or C will not be masked out (default: 0.9)
		- pDmask: Probability that an element in D will not be masked out (default: 0.8)
		- pDzero: Probability that D = 0 (default: 0.5)

	Returns:
		- returns a generator of dSS objects (to use in a for loop for example)

	..Example::
		>>> sys = list( iter_random_dSS( 12, True, (10,20)) )
		>>> for S in iter_random_dSS( 12, True, (10,20)):
		>>>		print( S )


	"""
	for i in range(number):
		if stable:
			yield random_dSS(randint(*n), randint(*p), randint(*q), pRepeat, pReal, pBCmask, pDmask, pDzero)
		else:
			nn=randint(*n)
			pp=randint(*p)
			qq=randint(*q)
			A = mat(rand(nn,nn))
			B = mat(rand(nn,qq))
			C = mat(rand(pp,nn))
			D = mat(rand(pp,qq))
			yield dSS(A,B,C,D)




def iter_random_dTF(number = 1, order = (5, 10)):
	"""
	Generate some n-th order random (stable or not) SISO transfer functions

	Parameters:
		- number: number of state-space to generate
		- order: tuple (mini,maxi) order of the filter (default:  random between 5 and 10)

	Returns:
		- returns a generator of dTF objects (to use in a for loop for example)

	..Example::
		>>> sys = list( iter_random_dTF( 12, (10,20)) )
		>>> for S in iter_random_dTF( 12, (10,20)):
		>>>		print( S.num )

	"""
	for i in range(number):
		n = randint(*order)
		yield random_dTF( n )




def iter_random_Butter( number=1, n=(5,10), Wc=(0.1,0.8), W1=(0.1,0.5), W2=(0.5,0.8), form=None, onlyEven=True):
	"""
	Generate some n-th order Butterworh filters
	Parameters
		----------
		number: number of Butterworth filters generated
		n: (int) The order of the filter
		Wc: used if btype is 'lowpass' or 'highpass'
			Wc is a tuple (min,max) for the cut frequency
		W1 and W2: used if btype is ‘bandpass’, ‘bandstop’
			W1 and W2 are tuple (min,max) for the two start/stop frequencies
		btype: (string) {None, ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}. Gives the type of filter. If None, the type is randomized
	"""
	for i in range(number):
		# choose the form
		if form is None:
			f = choice( ("lowpass", "highpass", "bandpass", "bandstop") )
		else:
			f = form
		# choose Wn
		if f in ("bandpass", "bandstop"):
			# choose 2 frequencies
			if W2[1] <= W1[0]:
				raise ValueError( "iter_random_Butter: W1 should be lower than W2")
			Wn1 = (W1[1] - W1[0]) * random_sample() + W1[0]
			Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
			while Wn2<=Wn1:
				Wn2 = (W2[1] - W2[0]) * random_sample() + W2[0]
			W=[Wn1,Wn2]
		else:
			# choose 1 frequency
			W = (Wc[1] - Wc[0]) * random_sample() + Wc[0]
		# choose order
		order = randint(*n)
		if onlyEven and order%2==0:
			order += 1

		yield Butter( order, W, f)



def random_dTF( n):
	"""
	Generate a n-th order random transfer function (non necesseraly stable)
	Parameters:
	    - n: order of the transfer function
	"""
	num = mat(rand(1,n))
	den = mat(rand(1,n))
	return dTF( num, den)


def random_dSS(n, p, q, pRepeat = 0.01, pReal = 0.5, pBCmask = 0.90, pDmask = 0.8, pDzero = 0.5):
	"""
	Generate ONE n-th order random  stable state-spaces, with q inputs and p outputs
	copy/Adapted from control-python library (Richard Murray): https://sourceforge.net/projects/python-control/ (thanks guys!)
	possibly already adpated/copied from Mathworks or Octave

	Parameters:
		- n: number of states (default:  random between 5 and 10)
		- p: number of outputs (default: 1)
		- q: number of inputs (default: 1)

		- pRepeat: Probability of repeating a previous root (default: 0.01)
		- pReal: Probability of choosing a real root (default: 0.5). Note that when choosing a complex root, the conjugate gets chosen as well. So the expected proportion of real roots is pReal / (pReal + 2 * (1 - pReal))
		- pBCmask: Probability that an element in B or C will not be masked out (default: 0.90)
		- pDmask: Probability that an element in D will not be masked out (default: 0.8)
		- pDzero: Probability that D = 0 (default: 0.5)

	Returns:
		- a dSS object
	"""
	# Check for valid input arguments.
	if n < 1 or n % 1:
		raise ValueError( "states must be a positive integer.  #states = %g." % n)
	if q < 1 or q % 1:
		raise ValueError( "inputs must be a positive integer.  #inputs = %g." % q)
	if p < 1 or p % 1:
		raise ValueError( "outputs must be a positive integer.  #outputs = %g." % p)

	# Make some poles for A.  Preallocate a complex array.
	poles = zeros(n) + zeros(n) * 0.j
	i = 0

	while i < n:

		if rand() < pRepeat and i != 0 and i != n - 1:
			# Small chance of copying poles, if we're not at the first or last  element.
			if poles[i - 1].imag == 0:
				poles[i] = poles[i - 1] # Copy previous real pole.
				i += 1

			else:
				poles[i:i + 2] = poles[i - 2:i] # Copy previous complex conjugate pair of poles.
				i += 2

		elif rand() < pReal or i == n - 1:
			poles[i] = 2. * rand() - 1. # No-oscillation pole.
			i += 1

		else:
			mag = rand() # Complex conjugate pair of oscillating poles.
			phase = 2. * pi * rand()
			poles[i] = complex(mag * cos(phase), mag * sin(phase))
			poles[i + 1] = complex(poles[i].real, -poles[i].imag)
			i += 2

	# Now put the poles in A as real blocks on the diagonal.

	A = zeros((n, n))
	i = 0

	while i < n:

		if poles[i].imag == 0:
			A[i, i] = poles[i].real
			i += 1

		else:
			A[i, i] = A[i + 1, i + 1] = poles[i].real
			A[i, i + 1] = poles[i].imag
			A[i + 1, i] = -poles[i].imag
			i += 2


	while True: # Finally, apply a transformation so that A is not block-diagonal.
		T = randn(n, n)

		try:
			A = dot(solve(T, A), T)  # A = T \ A * T
			break

		except LinAlgError:
			# In the unlikely event that T is rank-deficient, iterate again.
			pass

	# Make the remaining matrices.
	B = randn(n, q)
	C = randn(p, n)
	D = randn(p, q)

	# Make masks to zero out some of the elements.
	while True:
		Bmask = rand(n, q) < pBCmask
		if not Bmask.all():  # Retry if we get all zeros.
			break

	while True:
		Cmask = rand(p, n) < pBCmask
		if not Cmask.all():  # Retry if we get all zeros.
			break

	if rand() < pDzero:
		Dmask = zeros((p, q))

	else:
		while True:
			Dmask = rand(p, q) < pDmask
			if not Dmask.all():  # Retry if we get all zeros.
				break


	# Apply masks.
	B = B * Bmask
	C = C * Cmask
	D = D * Dmask

	return dSS(A, B, C, D)
