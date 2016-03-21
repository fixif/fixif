#coding: UTF8

"""
This file contains State-Space structure

"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fipogen.SIF import SIF
from fipogen.Structures import Structure


from numpy import eye, zeros, ones
from numpy import matrix as mat

class State_Space(Structure):

	_name = "State-Space"
	_possibleOptions = { 'form': (None, 'balanced', 'ctrl', 'obs')}


	def __init__(self, filter, form=None ):
		"""
		convert a discrete state space to to sif
		"""

		# check the args
		self.manageOptions(form=form)

		if form==None:
			S = filter.dSS
		elif form=='balanced':
			S = filter.dSS.balanced()
		elif form=='ctrl' or form=='obs':
			S = filter.dTF.to_dSS(form)

		n,p,q = S.size
		l = 0

		JtoS = ( eye((l)), zeros((n,l)), zeros((p,l)), zeros((l,n)), zeros((l,q)), S.A, S.B, S.C, S.D )
		dJtodS = [ ones( X.shape ) for X in JtoS ]


		self._SIF = SIF( JtoS, dJtodS )


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


	@staticmethod
	def canAcceptFilter(filter, form):
		"""
		The forms 'ctrl' and 'obs' cannot be applied for SISO filters
		otherwise, it can always be used
		"""
		if form==None:
			return True
		if form=='balanced':
			return filter.isStable()
		if form=='ctrl' or form=='obs':
			return filter.isSISO()

		# should never happend
		return False