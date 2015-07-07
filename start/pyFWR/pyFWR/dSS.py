# coding=utf-8

# inspired by http://sourceforge.net/apps/mediawiki/python-control

#inclure licence CECILL-C

"""
This module contains the class `dSS`, that defines a discrete-time State-Space realization.

Properties:
- A, B, C, D: matrices A, B, C and D that defines the discrete-time State-Space realization
- n, p, q: number of states, inputs and output
- Wc, Wo: controllability and observability Gramians (only computed when needed)

Methods:
__str__: string representation
__repr__: representation
__check_dimensions__: check if the dimensions are consistent
normH2: compute the H2-norm of the state-space
#Todo#
_latex_: to be used with Sage
__add__  __radd__
__sub__  __rsub__
__mul__   __rmul__
normHinf: compute the H-infiny norm
matnormH2: compute the matrix of the H2-norm of the sub-systems
dtf: convert to discrete-time transfer function
random: create a random stable state-space
"""
from copy import copy

import numpy as np
import scipy as sc
mat = np.matrix	#alias
from math import sqrt
from numpy.random import rand, randn
from numpy.linalg import inv, det, solve
from numpy.linalg.linalg import LinAlgError
from numpy import dot, eye, pi, cos, sin

import random
import slycot


__author__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__license__ = "CECILL-C"
__version__ = "$Id$"


from decorators import ReadOnlyCachedAttribute


class dSS(object):
	"""Class `dSS` that describes a discrete State-Space realization.

	A state-space system is defined by :math:A\in\mathbb{R}^{n \times n}, B\in\mathbb{R}^{n \times p}, C\in\mathbb{R}^{q \times n} and C\in\mathbb{q \times p}, and
	. . math::

	\left\lbrace\begin{array}{rcl}
	X(k+1) &=& AX(k) + BU(k) \\
	Y(k) &=& CX(k) + DU(k)

	n,p,q are the dimensions of the state-space (number of states, inputs and outputs, respectively)	
	"""


	def __init__(self,A,B,C,D):
		"""
		Construction of a discrete state-space
		"""
		self._A = mat(A)		#: matrix A
		self._B = mat(B)		#: matrix B
		self._C = mat(C)		#: matrix C
		self._D = mat(D)		#: matrix D
		self._n, self._p, self._q = self.__check_dimensions__()			#: dimensions

	# A, B, C and D are read-only
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


	# The controlability and observability Gramians are readonly attributes, and they are computed once, only when needed
	##@ReadOnlyCachedAttribute
	@property
	def Wc( self):
		# Solve the Lyapunov equation by calling the Slycot function sb03md
		try:
			X,scale,sep,ferr,w = slycot.sb03md( self.n, -self._B*self._B.transpose(), copy(self._A), eye(self.n,self.n), dico='D', trana='T')
		except ValueError, ve:
			if ve.info < 0:
				e = ValueError(ve.message)
				e.info = ve.info
			else:
				e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
				e.info = ve.info
			raise e		
		return mat(X)

	#@ReadOnlyCachedAttribute
	@property
	def Wo( self):
		# Solve the Lyapunov equation by calling the Slycot function sb03md
		try:
			X,scale,sep,ferr,w = slycot.sb03md(self.n, -self._C.transpose()*self._C, self._A.transpose(), eye(self.n,self.n), dico='D', trana='T')
		except ValueError, ve:
			if ve.info < 0:
				e = ValueError(ve.message)
				e.info = ve.info
			else:
				e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
				e.info = ve.info
			raise e		
		return mat(X)



	# display
	def __str__(self):
		"""display the state-space"""
		return "State Space\nA="+repr(self._A)+"\nB="+repr(self._B)+"\nC="+repr(self._C)+"\nD="+repr(self._D)

	def __repr__(self):
		return str(self)	

	#def _latex_(self):
		##TODO
		#return ""


	def normH2( self):
		"""compute the H2-norm of the system"""
		try:
			M = self.C*W*self.C.transpose()+self.D*self.D.transpose()
			return sqrt( float( M.trace() ) )
		except:
			return np.inf



	def __check_dimensions__(self):
		"""computes the number of inputs and outputs.
		It also checks the concordance of the matrices' size"""

		# A
		a1,a2 = self.A.shape
		if a1!=a2:
			raise ValueError, 'A is not a square matrix'
		n = a1

		# B
		b1,b2 = self.B.shape
		if b1!=n:
			raise ValueError, 'A and B should have the same number of rows'
		inputs=b2

		# C
		c1,c2 = self.C.shape
		if c2!=n:
			raise ValueError, 'A and C should have the same number of columns'
		outputs=c1

		# D
		d1,d2 = self.D.shape
		if d1!=outputs or d2!=inputs:
			raise ValueError, 'D should be consistant with C and B'

		return n, inputs, outputs


def random_dSS( n=None, p=1, q=1):
	"""Generate a n-th order random stable state-space, with p inputs and q outputs
	
	copy/Adapted from control-python library
	"""
	
	if n==None:
		n = random.randint(5,10)

	# Probability of repeating a previous root.
	pRepeat = 0.05
	# Probability of choosing a real root.  Note that when choosing a complex
	# root, the conjugate gets chosen as well.  So the expected proportion of
	# real roots is pReal / (pReal + 2 * (1 - pReal)).
	pReal = 0.6
	# Probability that an element in B or C will not be masked out.
	pBCmask = 0.8
	# Probability that an element in D will not be masked out.
	pDmask = 0.3
	# Probability that D = 0.
	pDzero = 0.2
				
	# Check for valid input arguments.
	if n < 1 or n % 1:
			raise ValueError(("states must be a positive integer.  #states = %g." % n))
	if p < 1 or p % 1:
		raise ValueError(("inputs must be a positive integer.  #inputs = %g." % p))
	if q < 1 or q % 1:
		raise ValueError(("outputs must be a positive integer.  #outputs = %g." % q))
				
	# Make some poles for A.  Preallocate a complex array.
	poles = np.zeros(n) + np.zeros(n) * 0.j
	i = 0
				
	while i < n:
		if rand() < pRepeat and i != 0 and i != n - 1:
			# Small chance of copying poles, if we're not at the first or last
			# element.
			if poles[i-1].imag == 0:
				# Copy previous real pole.
				poles[i] = poles[i-1]
				i += 1
			else:
				# Copy previous complex conjugate pair of poles.
				poles[i:i+2] = poles[i-2:i]
				i += 2
		elif rand() < pReal or i == n - 1:
			# No-oscillation pole.
			poles[i] = 2. * rand() - 1.
			i += 1
		else:
			# Complex conjugate pair of oscillating poles.
			mag = rand()
			phase = 2. * pi * rand()
			poles[i] = complex(mag * cos(phase), mag * sin(phase))
			poles[i+1] = complex(poles[i].real, -poles[i].imag)
			i += 2

	# Now put the poles in A as real blocks on the diagonal.
	A = np.zeros((n, n))
	i = 0
	while i < n:
		if poles[i].imag == 0:
			A[i, i] = poles[i].real
			i += 1
		else:
			A[i, i] = A[i+1, i+1] = poles[i].real
			A[i, i+1] = poles[i].imag
			A[i+1, i] = -poles[i].imag
			i += 2
	# Finally, apply a transformation so that A is not block-diagonal.
	while True:
		T = randn(n, n)
		try:
			A = dot(solve(T, A), T) # A = T \ A * T
			break
		except LinAlgError:
			# In the unlikely event that T is rank-deficient, iterate again.
			pass

	# Make the remaining matrices.
	B = randn( n, p)
	C = randn( q, n)
	D = randn( q, p)

	# Make masks to zero out some of the elements.
	while True:
		Bmask = rand(n, p) < pBCmask 
		if not Bmask.all(): # Retry if we get all zeros.
			break
	
	while True:
		Cmask = rand(q, n) < pBCmask
		if not Cmask.all(): # Retry if we get all zeros.
			break
	
	if rand() < pDzero:
		Dmask = np.zeros((q, p))
	else:
		while True:
			Dmask = rand(q, p) < pDmask
			if not Dmask.all(): # Retry if we get all zeros.
				break
	

	# Apply masks.
	B = B * Bmask
	C = C * Cmask
	D = D * Dmask

	return dSS(A, B, C, D)
		
	