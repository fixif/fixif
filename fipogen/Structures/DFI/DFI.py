#coding=utf8

from fipogen.SIF import SIF
from fipogen.Structures.Structure import Structure

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv

class DFI(Structure):

	def __init__(self, filter, opt=1):

		"""


		Two options are available

		1 - compute num and den at the same time (normalize,...)
		2 - compute num and den separately (don't normalize, ...)

		"""

		if opt not in {1,2}:
			raise("Unknown option...")

		# convert everything to mat
		nden = nnum = filter.dTF.order
		num = filter.dTF.num
		den = filter.dTF.den

		# Compute gammas

		# gamma1 and gamma4 differ between options
		if opt == 1:
			gamma1 = c_[[num[0, 1:]],[-den[0, 1:]]]
		elif opt == 2:
			gamma1 = r_[[c_[num[0, 1:], zeros((1, nden))]], [c_[zeros((1, nnum)), -den[0, 1:]]]]
	# ???
		#gamma2 = [[diag(ones((1,nnum-1)),-1), zeros((nnum, nden))],[zeros((nden,nnum)), diag(ones((1,nden-1)),-1)]]
		gamma2 = r_[c_[diagflat(ones((1, nnum-1)), -1), zeros((nnum, nden))],c_[zeros((nden, nnum)), diagflat(ones((1, nden-1)), -1)]]
		#CurrentWork
		gamma3 = r_[atleast_2d(1), zeros((nnum+nden-1, 1))]

		if opt == 1:
			gamma4 = r_[zeros((nnum, 1)), atleast_2d(1), zeros((nden-1, 1))]
		elif opt == 2:
			gamma4 = r_[zeros((nnum, 2)), [[1,1]], zeros((nden-1, 2))]

		gamma1 = mat(gamma1)
		gamma2 = mat(gamma2)
		gamma3 = mat(gamma3)
		gamma4 = mat(gamma4)

	# transformation to 'optimize' the code

		T = mat(rot90(eye(2*nnum)))

		invT = inv(T)

		# build SIF

		if opt == 1:

			JtoS = atleast_2d(den[0,0]), invT*gamma4, atleast_2d(1), gamma1*T, atleast_2d(num[0,0]), invT*gamma2*T, invT*gamma3, mat(zeros((1, nnum+nden))), atleast_2d(0)

		elif opt == 2:

			JtoS = mat(eye(2)), invT*gamma4, mat([1,1]), gamma1*T, r_[atleast_2d(num[0,0]),atleast_2d(0)], invT*gamma2*T, invT*gamma3, mat(zeros((1, nnum+nden))), atleast_2d(0)

		#print(JtoS)

		# build SIF
		self.SIF = SIF( JtoS )
		# instead of call the constructor of the class Structure (with `super(self.__class__,self).__init__(...)`), I am calling a simple method that do the same job
		# because the `super(....)` is fucking ugly (it's a little bit better in Python3, but not yet enough)
		self.initStructure( name="Direct Form I" )


