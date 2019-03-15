__author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Anastasia Volkova", "Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from os import path
import mpmath
from numpy import zeros, ones, matrix, power, ndenumerate, kron, multiply, nditer
from numpy import floor, log2, ceil
from string import Template

from fixif.config import SIF_TEMPLATES_PATH

# functions to define some parameters in a AMPL .dat file
def generateAMPLParam(name, val, format="%f"):
	"""generate AMPL code for the data of a given parameter
	Parameters:
		- name: name of the parameter
		- val: value of this parameter (int or a numpy matrix)
		- format: the C string format used to display the parameter ("%d" for an integer, etc.)
	Returns: a string to be inserted in a .dat file
	"""
	if isinstance(val, int):
		return "param %s := %d;" % (name, val)
	if val.shape[0] == 1 or val.shape[1] == 1:
		# 1d vector
		return "param %s := \n%s;" % (name, "\n".join(("%d "+format) % (i[0]+1, wm) for i, wm in ndenumerate(val)))
	else:
		# 2d array
		col = " ".join(str(x+1) for x in range(val.shape[1]))
		data = "\n".join(str(i+1)+" "+" ".join(format%x for x in nditer(val[i,:])) for i in range(val.shape[0]))
		return "param %s : %s := \n%s;" % (name, col, data)




class R_FxP:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the following methods in the Realization class
	the Realization class will inherit from R_FxP class

	This class adds methods to perform the FxP implementation with multiple wordlength paradigm
	"""



	def _computeNaiveMSB(self, u_bar, output_info=None):
		"""Compute the MSB of t, x and y without taking into account the errors in the filter evaluation, and the
		errors in the computation of this MSB (the WCPG computation and the log2 associated)
		Returns a vector of MSB
		Parameters:
			- u_bar: vector of bounds on the inputs of the system
		Returns: a vector of MSB such that the intermediate variables, the states and the output do not overflow
		WHEN WE DO NOT THE ROUNDOFF ERRORS INTO ACCOUNT

		we just use the equation  m = ceil( log2( <<Hzeta>>. u_bar ) )
		"""
		# compute the WCPG of Hzeta
		zeta_bar = self.Hzeta.WCPG(output_info) * u_bar

		# TODO: Do it as it should be done, as in FxPF (see Nastia thesis p113)
		with mpmath.workprec(500):
			# and then the log2
			msb = [int(mpmath.ceil(mpmath.log(x[0], 2))) for x in zeta_bar.tolist()]

		return msb


	def _w_tilde(self, u_bar):
		"""Compute w_tilde, the threshold for the word-length w such that
		MSB = computeNaiveMSB    if w >= w_tilde
		MSB = computeNaiveMSB+1  if w < w_tilde
		(this doesn't count into account the roundoff error, as in FxPF)
		See ARITH26 paper
		Parameters:
			- u_bar: vector of bounds on the inputs of the system
		Returns: a vector of thresholds w_tilde

		We use:  w_tilde = 1 + ceil(log2(zeta_bar)) - floor(log2( 2^ceil(log2(zeta_bar)) - zeta_bar ))
		with zeta_bar = <<Hzeta>>.u_bar
		"""
		#TODO: test if zeta_bar is a power of 2 (should be +Inf in that case)
		zeta_bar = self.Hzeta.WCPG() * u_bar

		with mpmath.workprec(500):  # TODO: compute how many bit we need !!
			wtilde = [int(1+mpmath.ceil(mpmath.log(x[0], 2)) - mpmath.floor(mpmath.log(mpmath.power(2, mpmath.ceil(mpmath.log(x[0], 2))) - x[0], 2))) for x in zeta_bar.tolist()]

		return wtilde


	def optimalUniformWL(self, u_bar, eps):
		"""
		Compute the minimal wordlength such that the output error is less than eps (component-wise)
		in the context where ALL THE WORD-LENGTH ARE THE SAME (and with KCM SoP)
		Parameters:
			- u_bar: vector of bounds on the inputs of the system
			- eps: vector of constraints on the output (each output must be less than the associate eps)
		Returns: (integer) the wordlength that, when used for the intermediate variables, the states and the oututs,
		satisfies the output error constraints
		"""

		def delta(w):
			"""function that compute delta(w), a vector of 0 or 1"""
			d = zeros(w.shape)
			for i in range(w.size):
				d[i] = 1 if w[i] < w_tilde[i] else 0
			return d

		# determining the MSB and w_tilde
		m_tilde = matrix(self._computeNaiveMSB(u_bar)).transpose()
		w_tilde = matrix(self._w_tilde(u_bar)).transpose()

		# error
		Weps = self.Hepsilon.WCPG()
		E = multiply(Weps, kron(ones((self.p, 1)), power(2, m_tilde.transpose())))

		# determining the minimal word-length with uniform scheme
		w_guess = int(max(ceil(log2(E * ones((self.l + self.n + self.p, 1))) - log2(eps)))[0, 0])
		return w_guess if all(E * power(2, -w_guess + delta(w_guess * ones((self.l + self.n + self.p, 1)))) < eps) else w_guess + 1


	def optimalWL(self, u_bar, eps, AMPLfilename='xmpl.dat', AMPLpath='.', wmax=64):
		""" see ARITH26 article
		Compute the minimal wordlength such that the output error is less than eps (component-wise)
		when the SoPC are done with KCM
		-> define the optimal problem
		-> generate the AMPL solver
		#TODO: run the solver, and get back the result

		Parameters:
			- u_bar: vector of bounds on the inputs of the system
			- eps: vector of constraints on the output (each output must be less than the associate eps)
			- AMPLfilename: (string) name of the AMPL file generated
			- path: (string) path where to store the AMPL file
			- wmax: int maximum value for the word-length

		#TODO: Returns: (integer) the wordlength that, when used for the intermediate variables, the states and the oututs,
		satisfies the output error constraints
		Returns: (inter) sub-optimal solution (but easy to get; works well when p=1)
		"""
		# make wmax a vector
		wmax = wmax * ones((self.l + self.n + self.p, 1))

		# determining the MSB
		m_tilde = matrix(self._computeNaiveMSB(u_bar)).transpose()
		w_tilde = matrix(self._w_tilde(u_bar)).transpose()

		# error
		Weps = self.Hepsilon.WCPG()
		E = multiply(Weps, kron(ones((self.p, 1)), power(2, m_tilde.transpose())))

		# generate the .dat file
		AMPLcode = {
			'def_p': generateAMPLParam('p', self.p),
			'def_np': generateAMPLParam('np', self.p + self.n + self.l),
			'def_u': generateAMPLParam('u', wmax, "%d"),
			'def_E': generateAMPLParam('E', E),
			'def_eps': generateAMPLParam('eps', eps),
			'def_wtilde': generateAMPLParam('wtilde', w_tilde, "%d")}

		# generate the xmpl.dat file
		with open(SIF_TEMPLATES_PATH + "xmpl.dat.template") as f:
			AMPL = Template(f.read())
		with open(path.join(AMPLpath, AMPLfilename), 'w') as f:
			f.write(AMPL.substitute(AMPLcode))

		if self.p == 1:
			return [ int(ceil(log2(Ei*(self.n+self.p+self.l)) - log2(eps[0,0]))) for Ei in nditer(E) ]
		else:
			weq=[]
			for j in range(self.l+self.n+self.p):
				weq.append( int(max(ceil(log2(E[i,j]*(self.n+self.p+self.l)) - log2(eps[i,0])) for i in range(self.p)) ))
			return weq
