# coding: utf8

"""
This file contains Object and methods for a Discrete State Space
"""
from numpy.core.umath import pi, cos, sin
from numpy.random.mtrand import randint, seed, rand, randn

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof", "Anastasia Lozanova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from numpy					import inf, empty, float64, shape, identity, absolute, dot, eye, array, asfarray, ones, matrix, matrix, matrix, matrix, zeros  # , astype
from numpy					import matrix as mat, Inf, set_printoptions
from numpy					import eye, zeros, r_, c_, sqrt
from numpy.linalg			import inv, det, solve, eigvals, LinAlgError
from numpy.linalg.linalg	import LinAlgError
from scipy.linalg			import solve_discrete_lyapunov
from slycot					import sb03md, ab09ad
from copy					import copy
from scipy.weave			import inline
from scipy.signal import ss2tf

import mpmath, numpy

from numpy.testing import assert_allclose

from fipogen.func_aux		import python2mpf_matrix, mp_poly_product, mpc_get_real


class dSS(object):
	r"""
	The dSS class describes a discrete state space realization

	A state space system :math:`(A,B,C,D)` is defined by

	.. math::

		\left\lbrace \begin{aligned}
		x(k+1) &= Ax(k) + Bu(k) \\
		y(k)   &= Cx(k) + Du(k)
		\end{aligned}\right.

	with :math:`A \in \mathbb{R}^{n \times n}, B \in \mathbb{R}^{n \times q}, C \in \mathbb{R}^{p \times n} \text{ and } D \in \mathbb{R}^{p \times q}`.

	**Dimensions of the state space :**

	.. math::
		:align: left
		n,p,q \in \mathbb{N}

	==  ==================
	n   number of states
	p   number of outputs
	q   number of inputs
	==  ==================

	Additional data available, computed once when asked for :
	dSS.Wo, dSS.Wc, dSS.norm_h2, dSS.WCPG

	- Gramians : Wo and Wc
	- "Norms"   : H2-norm (H2norm), Worst Case Peak Gain (WCPG) (see doc for each)

	"""

	_W_method = 'slycot1'  # linalg, slycot1


	def __init__(self, A, B, C, D):
		"""
		Construction of a discrete state space

		.. TODO

			force docstring to appear in doc because calling spec is important
			add special section to document event_spec and examples
		"""

		self._A = mat(A)  # User input
		self._B = mat(B)
		self._C = mat(C)
		self._D = mat(D)

		# Initialize state space dimensions from user input
		(self._n, self._p, self._q) = self._check_dimensions()  # Verify coherence, set dimensions

		# Initialize Gramians
		self._Wo = None
		self._Wc = None

		# Initialize norms
		self._H2norm = None    # keep ?
		self._DC_gain = None    # keep ?
		self._WCPG = None


	# Properties
	@property
	def A(self):
		return self._A

	@property
	def B(self):
		return self._B

	@property
	def C(self):
		return self._C

	@property
	def D(self):
		return self._D

	@property
	def n(self):
		return self._n

	@property
	def p(self):
		return self._p

	@property
	def q(self):
		return self._q

	# Wc and Wo are computed only once
	@property
	def Wo(self):
		if (self._Wo is None):
			self.calc_Wo()
		return self._Wo

	@property
	def Wc(self):
		if (self._Wc is None):
			self.calc_Wc()
		return self._Wc

	@property
	def size(self):
		"""
		Return size of state space
		"""
		return (self._n, self._p, self._q)


	#======================================================================================#
	# Observers (Wo, Wc) calculation
	#======================================================================================#
	def calc_Wo(self, method=None):
		"""
		Computes observers :math:`W_o`  with method 'method' :

		:math:`W_o` is solution of equation :
		.. math::
			A^T * W_o * A + C^T * C = W_o

		Available methods :

		- ``linalg`` : ``scipy.linalg.solve_discrete_lyapunov``, 4-digit precision with small sizes,
		1 digit precision with bilinear algorithm for big matrixes (really bad).
		not good enough with usual python data types

		- ``slycot1`` : using ``slycot`` lib with func ``sb03md``, like in [matlab ,pydare]
		see http://slicot.org/objects/software/shared/libindex.html

		- ``None`` (default) : use the default method defined in the dSS class (dSS._W_method)

		..Example::

			>>>mydSS = random_dSS() ## define a new state space from random data
			>>>mydSS.calc_Wo('linalg') # use numpy
			>>>mydSS.calc_Wo('slycot1') # use slycot
			>>>mydSS.calc_Wo() # use the default method defined in dSS

		.. warning::

			solve_discrete_lyapunov does not work as intended, see http://stackoverflow.com/questions/16315645/am-i-using-scipy-linalg-solve-discrete-lyapunov-correctl
			Precision is not good (4 digits, failed tests)

		"""

		if method is None:
			method = dSS._W_method

		if (method == 'linalg'):
			try:
				X = solve_discrete_lyapunov(self._A.transpose(), self._C.transpose() * self._C)
				self._Wo = mat(X)

			except LinAlgError as ve:
				if (ve.info < 0):
					e = LinAlgError(ve.message)
					e.info = ve.info
				else:
					e = LinAlgError( "dSS: Wo: scipy Linalg failed to compute eigenvalues of Lyapunov equation")
					e.info = ve.info
				raise e

		elif (self._W_method == 'slycot1'):
			# Solve the Lyapunov equation by calling the Slycot function sb03md
			# If we don't use "copy" in the call, the result is plain false

			try:
				X, scale, sep, ferr, w = sb03md(self.n, -self._C.transpose() * self._C, copy(self._A.transpose()), eye(self.n, self.n), dico='D', trana='T')
				self._Wo = mat(X)

			except ValueError as ve:

				if ve.info < 0:
					e = ValueError(ve.message)
					e.info = ve.info
				else:
					e = ValueError("dSS: Wo: The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
					e.info = ve.info
				raise e

		else:
			raise ValueError("dSS: Unknown method to calculate observers (method=%s)"%method)


	def calc_Wc(self, method=None):
		"""
		Computes observers :math:`W_c`  with method 'method' :

		:math:`W_c` is solution of equation :
		.. math::
			A * W_c * A^T + B * B^T = W_c

		Available methods :

		- ``linalg`` : ``scipy.linalg.solve_discrete_lyapunov``, 4-digit precision with small sizes,
		1 digit precision with bilinear algorithm for big matrixes (really bad).
		not good enough with usual python data types

		- ``slycot1`` : using ``slycot`` lib with func ``sb03md``, like in [matlab ,pydare]
		see http://slicot.org/objects/software/shared/libindex.html

		- ``None`` (default) : use the default method defined in the dSS class (dSS._W_method)

		..Example::

			>>>mydSS = random_dSS() ## define a new state space from random data
			>>>mydSS.calc_Wc('linalg') # use numpy
			>>>mydSS.calc_Wc('slycot1') # use slycot
			>>>mydSS.calc_Wo() # use the default method defined in dSS

		.. warning::

			solve_discrete_lyapunov does not work as intended, see http://stackoverflow.com/questions/16315645/am-i-using-scipy-linalg-solve-discrete-lyapunov-correctl
			Precision is not good (4 digits, failed tests)

		"""
		if method is None:
			method = dSS._W_method

		if (method == 'linalg'):
			try:
				X = solve_discrete_lyapunov(self._A, self._B * self._B.transpose())
				self._Wc = mat(X)

			except LinAlgError as ve:
				if (ve.info < 0):
					e = LinAlgError(ve.message)
					e.info = ve.info
				else:
					e = LinAlgError( "dSS: Wc: scipy Linalg failed to compute eigenvalues of Lyapunov equation")
					e.info = ve.info
				raise e

		elif (self._W_method == 'slycot1'):
			# Solve the Lyapunov equation by calling the Slycot function sb03md
			# If we don't use "copy" in the call, the result is plain false

			try:
				X, scale, sep, ferr, w = sb03md(self.n, -self._B * self._B.transpose(), copy(self._A), eye(self.n, self.n), dico='D', trana='T')
				self._Wc = mat(X)

			except ValueError as ve:

				if ve.info < 0:
					e = ValueError(ve.message)
					e.info = ve.info
				else:
					e = ValueError("dSS: Wc: The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
					e.info = ve.info
				raise e

		else:
			raise ValueError("dSS: Unknown method to calculate observers (method=%s)"%method)


	#======================================================================================#
	# Norms calculation
	#======================================================================================#

	def H2norm(self):
		r"""

		Compute the H2-norm of the system

		.. math::

			\langle \langle H \rangle \rangle = \sqrt{tr ( C*W_c * C^T + D*D^T )}


		"""
		# return cached value if already computed
		if self._H2norm is not None:
			return self._H2norm

		# otherwise try to compute it
		try:
			# less errors when Wc is big and Wo is small
			M = self._C * self.Wc * self._C.transpose() + self._D * self._D.transpose()
			self._H2norm = sqrt(M.trace())
		except:
			try:
				M = self._B.transpose() * self.Wo * self._B + self._D * self._D.transpose()
				self._H2norm = sqrt(M.trace())
			except:
				raise ValueError( "dSS: h2-norm : Impossible to compute M. Default value is 'inf'" )

		return self._H2norm






	#======================================================================================#
	def WCPG(self):

		r"""
		Compute the Worst Case Peak Gain of the state space

		.. math::
			\langle \langle H \rangle \rangle \triangleq |D| + \sum_{k=0}^\infty |C * A^k * B|

		Using algorithm developed in paper :
		[CIT001]_

		.. [CIT001]
			Lozanova & al., calculation of WCPG

		"""
		# compute the WCPG value if it's not already done
		if self._WCPG is None:

			try:
				A = array(self._A)
				B = array(self._B)
				C = array(self._C)
				D = array(self._D)
				n,p,q = self.size
				W = empty( (p, q), dtype=float64)

				code = "return_val = WCPG_ABCD( &W[0,0], &A[0,0], &B[0,0], &C[0,0], &D[0,0], n, p, q);"
				support_code = 'extern "C" int WCPG_ABCD(double *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q);'
				err = inline(code, ['W', 'A', 'B', 'C', 'D', 'n', 'p', 'q'], support_code=support_code, libraries=["WCPG"])
				if err==0:
					# change numpy display formatter, so that we can display the full coefficient in hex (equivalent to printf("%a",...) in C)
					set_printoptions(formatter={'float_kind':lambda x:x.hex()})
					print(self)
					raise ValueError( "WCPG: cannot compute WCPG")
				self._WCPG = mat(W)
			except:
				raise ValueError( "dSS: Impossible to compute WCPG matrix. Is WCPG library really installed ?")

		return self._WCPG




	#======================================================================================#
	def calc_DC_gain(self):

		r"""
		Compute the DC-gain of the filter

		.. math::
			\langle H \rangle = C * (I_n - A)^{-1} * B + D

		"""
		# compute the DC gain if it is not already done
		if self._DC_gain is None:
			try:
				self._DC_gain = self._C * inv(identity(self._n) - self._A) * self._B + self._D
			except:
				raise ValueError( 'dSS: Impossible to compute DC-gain from current discrete state space' )

		return self._DC_gain


	#======================================================================================#
	def _check_dimensions( self ):
		"""
		Computes the number of inputs and outputs.
		Check for concordance of the matrices' size
		"""

		# A
		a1, a2 = self._A.shape
		if a1 != a2:
			raise ValueError( 'dSS: A is not a square matrix' )
		n = a1

		# B
		b1, b2 = self._B.shape
		if b1 != n:
			raise ValueError( 'dSS: A and B should have the same number of rows' )
		inputs = b2

		# C
		c1, c2 = self._C.shape
		if c2 != n:
			raise ValueError( 'dSS: A and C should have the same number of columns')
		outputs = c1

		# D
		d1, d2 = self._D.shape
		if (d1 != outputs or d2 != inputs):
			raise ValueError( 'dSS: D should be consistent with C and B' )

		return n, outputs, inputs


	#======================================================================================#
	def __str__(self):
		"""
		Display the state-space
		"""

		def tostr(M, name):
			if M is not None:
				return name + "= " + repr(M) + "\n"
			else:
				return name + " is not computed\n"

		def plural(n):
			return 's' if n>0 else ''

		str_mat = """State Space (%d state%s, %d output%s and %d input%s)
		A= %s
		B= %s
		C= %s
		D= %s
		"""% (self._n, plural(self._n), self._p, plural(self._p), self._q, plural(self._q), repr(self._A), repr(self._B), repr(self._C), repr(self._D) )

		# Observers Wo, Wc
		#str_mat += tostr( self._Wc, 'Wc')
		#str_mat += tostr( self._Wo, 'Wo')

		# norms
		#str_mat += tostr( self._H2norm, 'H2-norm')
		#str_mat += tostr( self._WCPG, 'WCPG')

		return str_mat


	#======================================================================================#
	def __mul__(self, other):
		"""
		We overload the multiplication operator so that two state spaces in series  give
		a resultant state space with formula checked in matlab and available at :
		https://en.wikibooks.org/wiki/Control_Systems/Block_Diagrams
		To be able to multiply matrixes, systems must respect some constraints
		"""

		# TODO: we must verify the following conditions for matrix multiplication
		# n2 = n1
		# p2 = q1
		# q2 = p1
		# p2 = n1 (=> n2 = p2)
		# n2 = q1 (=> id)

		n1, p1, q1 = self.size
		n2, p2, q2 = other.size

		if (not(n1 == n2)):
			raise ValueError( "dSS: States spaces must have same number of states n")
		elif (not(p1 == n2)):
			raise ValueError( "dSS: second state space should have same number of states as first state number of inputs")
		elif (not(n1 == q2)):
			raise ValueError( "dSS: second state space should have same number of outputs as first state number of states")
		elif (not(p1 == q2)):
			raise ValueError( "dSS: second state space should have number of outputs equal to first state space number of inputs")
		elif (not(q1 == p2)):
			raise ValueError( "dSS: second state space number of inputs should be equal to first state space number of outputs")

		#TODO: possible simplification if self.A==other.A ??

		amul = r_[c_[ self.A, self.B*other.C ], c_[ zeros((n2, n1)), other.A ]]
		bmul = r_[ self.B*other.D, other.B ]
		cmul = c_[ self.C, self.D*other.C ]
		dmul = self.D*other.D

		return dSS(amul, bmul, cmul, dmul)


	#======================================================================================#
	def __repr__(self):
		return str(self)


	# get subsystem
	def __getitem__(self, *args):

		return dSS(self._A, self._B[:,args[0][1]], self._C[args[0][0],:], self._D[args[0][0],args[0][1]])




	def to_dTF(self):
		"""
		Transform a SISO state-space into a transfer function

		"""

		if self._p!=1 or self._q!= 1:
			raise ValueError( 'dSS: the state-space must be SISO to be converted in transfer function')
		from fipogen.LTI import dTF
		num,den = ss2tf( self._A, self._B, self._C, self._D)
		return dTF( num[0], den )


	def assert_close(self, other):
		# at this point, it should exist an invertible matrix T such that
		# self.A == inv(T) * other.A * T
		# self.B == inv(T) * other.B
		# self.C == other.C * T
		# self.D == other.D

		#TODO: this is probably not enough...
		assert_allclose( self.C*self.B, other.C*other.B, atol=1e-12)
		assert_allclose( self.C*self.A*self.B, other.C*other.A*other.B, atol=1e-12)
		assert_allclose( self.C*self.A*self.A*self.B, other.C*other.A*other.A*other.B, atol=1e-12)
		assert_allclose( self.D, other.D, atol=1e-12)


	def balanced(self):
		"""
		Returns an equivalent balanced state-space system

		Use ab09ad method from Slicot to get balanced state-space
		see http://slicot.org/objects/software/shared/doc/AB09AD.html

		Returns
		- a dSS object
		"""

		Nr, Ar, Br, Cr, hsv = ab09ad( 'D', 'B', 'N', self.n, self.q, self.p, self.A, self.B, self.C, nr=self.n, tol=1e-18)
		if Nr==0:
			raise ValueError("dSS: balanced: The selected order nr is greater than the order of a minimal realization of the given system. It was set automatically to a value corresponding to the order of a minimal realization of the system")
		return dSS( Ar, Br, Cr, self.D)

	def sub_dSS(self, S, add=False):
		"""
		This method computes the difference between self and a filter S given in the argument such that
		the result filter H := self - S has
			H.A = [[self.A, zeros(self.n, S.n)], [zeros(S.n, self.n), S.A]]
			H.B = [[self.B], [S.B]]
			H.C = [self.C, -S.C]
			H.D = [self.D - S.D]
		Parameters
		----------
		S - a dSS to substract from self

		Returns
		-------
		H - a dSS which is equal to (self - S)
		"""

		newA = numpy.concatenate((self.A, numpy.zeros([self.n, S.n])), axis=1)
		tmp = numpy.concatenate((numpy.zeros([S.n, self.n]), S.A), axis=1)
		newA = numpy.concatenate((newA, tmp), axis=0)

		#newA = numpy.matrix([[self.A, numpy.zeros(self.n, S.n)], [numpy.zeros(S.n, self.n), S.A]])
		newB =numpy.concatenate((self.B, S.B), axis=0)
		#newB = numpy.matrix([[self.B], [S.B]])
		if add:
			#newC = numpy.matrix([self.C, S.C])
			newC = numpy.concatenate((self.C, S.C), axis = 1)
			newD = self.D + S.D
		else:
			#newC = numpy.matrix([self.C, -S.C])
			newC = numpy.concatenate((self.C, -S.C), axis=1)
			newD = self.D - S.D

		return dSS(newA, newB, newC, newD)




# def sub_dSSmp(A1, B1, C1, D1, A2, B2, C2, D2, add=False):
# 	"""
# 	Given two state-space systems S1 and S2 with coefficients in multiple precision metrices,
# 	this function computes the difference H:=S1-S2, where system H has output h := y1(k) - y2(k).
#
# 	Parameters
# 	----------
# 	A1,...,D1 - state matrices of system S1
# 	A2,...,D2 - state matrices of system S2
#
# 	Returns
# 	-------
# 	A, B, C, D - state matrices of the filter H
# 	"""
# 	n1 = A1.rows
# 	n2 = A2.rows
# 	p1 = D1.rows
# 	p2 = D2.rows
# 	q1 = D1.cols
# 	q2 = D2.cols
#
# 	if q1 != q2:
# 		raise ValueError('Cannot substract two State-Space systems with different size of inputs')
# 	if p1 != p2:
# 		raise ValueError('Cannot substract two State-Space systems with different size of outputs')
# 	q = q1
# 	p = p1
#
# 	A = mpmath.mp.zeros(n1 + n2, n1 + n2)
# 	B = mpmath.mp.zeros(n1 + n2, q)
# 	C = mpmath.mp.zeros(p, n1 + n2)
# 	D = mpmath.mp.zeros(p, q)
#
#
# 	for i in range(0, n1):
# 		for j in range(0, n1):
# 			A[i,j] = A1[i,j]
#
# 	for i in range(0, n2):
# 		for j in range(0, n2):
# 			A[i + n1, j+n1] = A2[i,j]
#
# 	for i in range(0, n1):
# 		for j in range(0, q):
# 			B[i,j] = B1[i,j]
# 	for i in range(0, n2):
# 		for j in range(0, q):
# 			B[i+n1, j] = B2[i,j]
#
# 	for i in range(0, p):
# 		for j in range(0, n1):
# 			C[i,j] = C1[i,j]
#
# 	if add:
# 		for i in range(0, p):
# 			for j in range(0,q):
# 				D[i,j] = mpmath.fadd(D1[i,j], D2[i,j], exact=True)
#
# 		for i in range(0, p):
# 			for j in range(0, n2):
# 				C[i, j + n1] = C2[i, j]
# 	else:
# 		for i in range(0, p):
# 			for j in range(0, q):
# 				D[i, j] = mpmath.fsub(D1[i, j], D2[i, j], exact=True)
# 		for i in range(0, p):
# 			for j in range(0, n2):
# 				C[i, j + n1] = -C2[i, j]
#
#
# 	return A,B,C,D





def iter_random_dSS(number, stable = True, n = (5, 10), p = (1, 5), q = (1, 5), pRepeat = 0.01, pReal = 0.5, pBCmask = 0.90, pDmask = 0.8, pDzero = 0.5):
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
			nn = randint(*n)
			if p == 1 and q == 1:
				pp = 1
				qq = 1
			else:
				pp=randint(*p)
				qq=randint(*q)
			A = mat(rand(nn,nn))
			B = mat(rand(nn,qq))
			C = mat(rand(pp,nn))
			D = mat(rand(pp,qq))


			yield dSS(A,B,C,D)



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


# def to_dTFmp(A,B,C,D, prec):
# 		"""
# 		Computes the Trasnfer function of a dSS in multiple precision using following method:
#
# 		H(Z) = P(Z)/Q(z) with
#
# 		P(z) = sum_i^n {  }
#
# 		TODO: complete the description
#
# 		Returns
# 		-------
# 		P, Q - coefficients of numerator and denumerator of the transfer function H(z) of self
# 		"""
#
# 		# converting the dSS matrices to mp type
# 		from mpmath import mp
# 		#prec = 100
# 		oldprec = mp.prec
# 		mp.prec = prec
#
# 		if isinstance(A, numpy.matrix):
# 			Amp = python2mpf_matrix(A)
# 		else:
# 			Amp = A
# 		if isinstance(B, numpy.matrix):
# 			Bmp = python2mpf_matrix(B)
# 		else:
# 			Bmp = B
# 		if isinstance(C, numpy.matrix):
# 			Cmp = python2mpf_matrix(C)
# 		else:
# 			Cmp = C
# 		if isinstance(D, numpy.matrix):
# 			Dmp = python2mpf_matrix(D)
# 		else:
# 			Dmp = D
#
# 		n = Amp.rows
# 		p = Dmp.rows
# 		q = Dmp.cols
# 		if(p != 1 or q != 1):
# 			raise ValueError( 'dSS: cannot convert a dSS to TF in multiple precision for not a SISO system')
#
#
# 		mp.prec = prec * 2
# 		with mpmath.extraprec(prec * 6):
# 			E, V = mp.eig(Amp)		#eig returns a list E and a matrix V
# 			Cmp = Cmp * V
# 			Vinv = mp.inverse(V)
# 			Bmp = Vinv * Bmp
#
#
# 			Q = mp_poly_product([-e for e in E])
# 			PP = mp.zeros(Q.rows - 1, 1)
# 			#tmp_polyproduct = mp.zeros([self.n, 1]) #temporary polynomial products
# 			for i in range(0, n):
# 				# P = sum_i=0^n c_i * b_i * product_j!=i p_j
# 				tmp_polyproduct = mp_poly_product([-e for e in E], i)
# 				PP = PP + Cmp[0, i] * Bmp[i, 0] * tmp_polyproduct
#
# 		if Dmp[0,0] != mpmath.mpf('0.0'):
# 			P = Dmp[0, 0] * Q
# 		else:
# 			P = mp.zeros(Q.rows, 1)
#
# 		for i in range(1, P.rows):
# 			P[i, 0] = P[i, 0] + PP[i-1, 0]
#
# 		b = mp.zeros(P.rows, 1)
# 		a = mp.zeros(Q.rows, 1)
# 		for i in range(0, P.rows):
# 			b[i,0] = P[i,0].real
# 		for i in range(0, Q.rows):
# 			a[i, 0] = Q[i, 0].real
#
# 		mp.prec = oldprec
# 		return b,a

