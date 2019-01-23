__author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Anastasia Volkova", "Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



import numpy as np
from fixif.SIF import SIF
from mpmath import ceil, floor, log, workprec, power




class R_FxP:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the following methods in the Realization class
	the Realization class will inherit from R_algorihtm class
	"""


	def flopoco(self, LSB_y_out, u_bar):
		"""
		This function generates MSB and LSB formats for a Fixed-Point implementation
		using the FloPoCo tool.

		User must indicate the desired LSB format for the output and the bound on
		the inputs.

		As result, function sets fields MSB and LSB to the formats which will guarantee
		that the output filter has output faithfully rounded to the LSB_y_out bits.


		Parameters
		----------
		self
		LSB_y_out: a p-element list of integers representing the LSB constraints on the y
		u_bar

		Returns
		-------

		"""
		pass




	def _compute_LSB(self, l_y_out):

		if not isinstance(l_y_out, int):
			raise ValueError("I implemented the function only for the case of 1 output! \n")
		# we need to add one more bit to the account for the
		# final rounding error
		l_y_out = l_y_out-1

		# construct the error-filter
		deltaSIF = self.computeDeltaSIF()

		# compute the WCPG of the error filter
		wcpgDeltaH = deltaSIF.dSS.WCPG()

		# we repartition the error budget equally for all variables
		c = self.l + self.n + self.p

		# In order to respect the overall error |deltaY(k)| < 2^(l_y_out-1)
		# we need to compute the temporary, state and output variables with LSB l_i
		# l_i = max(l_y_out) - g_i
		# where the correction term g_i is computed via
		# g_i = 1 + max_j { ceil( log2 ( c * wcpgDeltaH[j, i] ) )}

		g = np.bmat([1 + max(np.ceil(np.log2(c * wcpgDeltaH[:, i] * 2**-l_y_out))) for i in range(0, c)])

		# the error budget for the output y(k) that will be later passed on to FloPoCo
		error_budget_y = 2**-mpmath.ceil(mpmath.log(c * wcpgDeltaH[0, c-1] * 2**-l_y_out, 2))/2**(l_y_out+1)

		for x in (g == np.inf):
			if x.any():
				print('Divided by zero\n')


		lsb = np.bmat(l_y_out - g - 1)

		return lsb, error_budget_y


	def computeNaiveMSB(self, u_bar, output_info=None):
		"""Compute the MSB of t, x and y without taking into account the errors in the filter evaluation, and the
		errors in the computation of this MSB (the WCPG computation and the log2 associated)
		Returns a vector of MSB"""

		# compute the WCPG of Hzeta
		zeta_bar = self.Hzeta.WCPG(output_info) * u_bar

		with workprec(500):  # TODO: use right precision !! Or do it as it should be done, as in FxPF (see Nastia thesis p113)
			# and then the log2
			msb = [int(ceil(log(x[0], 2))) for x in zeta_bar.tolist()]

		return msb

	def w_tilde(self, u_bar):
		"""compute w_tilde, the threshold for the word-length w such that
		MSB = computeNaiveMSB    if w >= w_tilde
		MSB = computeNaiveMSB+1  if w < w_tilde
		(this doesn't count into account the roundoff error, as in FxPF"""

		zeta_bar = self.Hzeta.WCPG() * u_bar

		with workprec(500):  # TODO: compute how many bit we need !!
			wtilde = [int(1+ceil(log(x[0], 2)) - floor(log(power(2, ceil(log(x[0], 2))) - x[0], 2))) for x in zeta_bar.tolist()]

		return wtilde


	def compute_MSB_allvar_extended(self, u_bar, lsb_t, lsb_x, lsb_y):

		# building L, R and S matrices for the extended SIF, which will have
		# a vector (t,x,y) as an output vector
		C1 = np.bmat([[np.eye(self.l, self.l)], [np.zeros([self.n, self.l])], [self.L]])  # L
		C2 = np.bmat([[np.zeros([self.l, self.n])], [np.eye(self.n, self.n)], [self.R]])  # R
		C3 = np.bmat([[np.zeros([self.l, self.q])], [np.zeros([self.n, self.q])], [self.S]])  # S

		# building an extended SIF
		S_ext = SIF((self.J, self.K, C1, self.M, self.N, self.P, self.Q, C2, C3))

		wcpg = S_ext.dSS.WCPG()


		# compute the error filter deltaH which corresponds to the extended SIF
		deltaH = S_ext.computeDeltaSIF()
		wcpgDeltaH = deltaH.dSS.WCPG()



		# compute msb via formula
		# msb_i = ceil( log2 ( (<<H>> * u_bar)_i + (<<deltaH>> * 2^lsb_ext)_i ))

		y_bar = wcpg * u_bar

		# lsb_ext2 = np.matrix([ lsb_ext[0, 0:deltaH.l] lsb_ext[0, deltaH.l:deltaH.l + deltaH.n] lsb_ext[0] ])
		lsb_bar = np.concatenate((lsb_t, lsb_x, lsb_t, lsb_x, lsb_y), axis=0)
		lsb_bar = np.bmat([lsb_bar])

		lsb_bar = np.matrix([2 ** lsb_bar[0, i] for i in range(0, lsb_bar.size)])
		delta_bar = wcpgDeltaH * lsb_bar.transpose()

		if y_bar.size == delta_bar.size:
			msb = np.bmat([np.ceil(np.log2(y_bar[i] + delta_bar[i])) for i in range(0, delta_bar.size)])
			return msb
		else:
			print('Something went wrong, error with sizes :( \n')
			return 0

