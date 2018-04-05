__author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Anastasia Volkova", "Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from scipy import signal
import numpy as np
from numpy import all
from fixif.LTI import Filter
from fixif.LTI import dSS

from fixif.SIF import Realization
from fixif.SIF import SIF
from fixif.func_aux import dynMethodAdder

import numpy as np

# list of methods to be added to the Realization class
__all__ = ['_compute_LSB', '_compute_MSB', 'compute_MSB_allvar_extended', 'flopoco']



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
	LSB_y_out - a p - element list of integers representing the LSB constraints on the y
	u_bar

	Returns
	-------

	"""



def _compute_LSB(self, l_y_out):

	l_y_out = np.matrix([l_y_out])

	#construct the error-filter
	deltaSIF = self.computeDeltaSIF()

	#compute the WCPG of the error filter
	wcpgDeltaH = deltaSIF.dSS.WCPG()

	#we repartition the error budget equally for all variables
	c = self.l + self.n + self.p


	# In order to respect the overall error |deltaY(k)| < 2^(l_y_out-1)
	# we need to compute the temporary, state and output variables with LSB l_i
	# l_i = max(l_y_out) - g_i
	# where the correction term g_i is computed via
	# g_i = 1 + max_j { ceil( log2 ( c * wcpgDeltaH[j, i] ) )}

	g = np.bmat([1 + max(np.ceil(np.log2(c * wcpgDeltaH[:,i]))) for i in range(0, c)])

	for x in (g==np.inf):
		if x.any():
			print('Divided by zero\n')


	lsb = np.bmat([max(l_y_out) - g])

	return lsb




def _compute_MSB(self, u_bar):

	# self._Z = np.bmat([[-J, M, N], [K, P, Q], [L, R, S]])

	C1 = np.bmat([[np.eye(self.l, self.l)], [np.zeros([self.n, self.l])], [self.L]]) #L
	C2 = np.bmat([[np.zeros([self.l, self.n])], [np.eye(self.n, self.n)], [self.R]])	#R
	C3 = np.bmat([ [np.zeros([self.l, self.q])], [np.zeros([self.n, self.q])], [self.S]])	#S


	#building an extended SIF
	S_ext = SIF((self.J, self.K, C1, self.M, self.N, self.P, self.Q, C2, C3))

	#print "New number of outputs: "
	#print S_ext.p

	wcpg = S_ext.dSS.WCPG()

	#print "WCPG:"
	#print wcpg

	y_bar = wcpg * u_bar
	msb=np.bmat([np.ceil(np.log2(x)) for x in y_bar])

	return msb

def compute_MSB_allvar_extended(self, u_bar, lsb_t, lsb_x, lsb_y):

	# building L, R and S matrices for the extended SIF, which will have
	# a vector (t,x,y) as an output vector
	C1 = np.bmat([[np.eye(self.l, self.l)], [np.zeros([self.n, self.l])], [self.L]])  # L
	C2 = np.bmat([[np.zeros([self.l, self.n])], [np.eye(self.n, self.n)], [self.R]])  # R
	C3 = np.bmat([[np.zeros([self.l, self.q])], [np.zeros([self.n, self.q])], [self.S]])  # S

	# building an extended SIF
	S_ext = SIF((self.J, self.K, C1, self.M, self.N, self.P, self.Q, C2, C3))

	wcpg = S_ext.dSS.WCPG()

	#compute the error filter deltaH which corresponds to the extended SIF
	deltaH = S_ext.computeDeltaSIF()
	wcpgDeltaH = deltaH.dSS.WCPG()

	# compute msb via formula
	# msb_i = ceil( log2 ( (<<H>> * u_bar)_i + (<<deltaH>> * 2^lsb_ext)_i ))

	y_bar = wcpg * u_bar

	#lsb_ext2 = np.matrix([ lsb_ext[0, 0:deltaH.l] lsb_ext[0, deltaH.l:deltaH.l + deltaH.n] lsb_ext[0] ])
	lsb_bar = np.concatenate((lsb_t, lsb_x, lsb_t, lsb_x, lsb_y), axis=0)
	lsb_bar = np.bmat([lsb_bar])

	lsb_bar = np.matrix([2 ** lsb_bar[0, i] for i in range(0, lsb_bar.size)])
	delta_bar = wcpgDeltaH * lsb_bar.transpose()

	if(y_bar.size == delta_bar.size):
		msb = np.bmat([np.ceil(np.log2(y_bar[i] + delta_bar[i])) for i in range(0, delta_bar.size)])
		return msb
	else:
		print('Something went wrong, error with sizes :( \n')
		return 0






