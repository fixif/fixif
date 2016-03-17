#coding: utf8

"""
This file contains Lattice Wave Digital Filter

"""

__author__ = "Thibault Hilaire, Anastasia Volkova"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Anastasia Volkova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"




from fipogen.SIF import SIF
from fipogen.Structures import Structure

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv



#from matlab.engine import connect_matlab
#eng = connect_matlab()
#eng.addpath('construct','fwrtoolbox')


class LWDF(Structure):

	_name = "Lattice Wave Digital Filter"              # name of the structure
	_possibleOptions = None       # the only option is nbSum, that can be 1 or 2
	_acceptMIMO = False

	def __init__(self, filter):
		"""

		"""

		# check the args
		self.manageOptions()

		# convert everything to mat
		n = filter.dTF.order
		num = mat(filter.dTF.num)
		den = mat(filter.dTF.den)




		# build SIF
		#self.SIF = SIF( (J, K, L, M, N, P, Q, R, S) )


