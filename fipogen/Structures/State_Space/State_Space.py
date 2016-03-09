#coding=UTF8

from fipogen.SIF import SIF
from fipogen.Structures.Structure import Structure


from numpy import eye, zeros
from numpy import matrix as mat

class State_Space(Structure):

	def __init__(self, filter ):

		"""
		convert a discrete state space to to sif
		"""

		n,p,q = filter.dSS.size
		l = 0

		JtoS = ( eye((l)), zeros((n,l)), zeros((q,l)), zeros((l,n)), zeros((l,p)), filter.dSS.A, filter.dSS.B, filter.dSS.C, filter.dSS.D )

		self.SIF = SIF( JtoS)
		self.initStructure( "State-Space")

		# # define available optimization processes, only if not already defined in subclass
		# if not(hasattr(self, '_avail_formopt')) and not(hasattr(self, '_formopt')):
		#
		# 	self._avail_formopt = {'uyw'}
		# 	self._formopt = 'uyw'
		#
		# # this implies setting start (default) values for u, y, w
		# # (we have l = 0)
		# # self.u = mat([])
		# # self.y = mat([])
		# # self.w = mat(eye(n))
		#
		# self._set_default_uyw()
