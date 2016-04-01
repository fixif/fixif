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





from fipogen.Structures import Structure
from numpy import matrix as mat
from matlab.engine import connect_matlab

# global variable to store the matlab engine
#TODO: put it in a dedicated module, so that everyone can access to it
eng = None




def makeLWDF( filter):
	"""

	"""
	# connect to matlab if not already connected
	global eng
	if eng is None:
		eng = connect_matlab()
		# eng.addpath('construct','fwrtoolbox')

	# run appropriate function in matlab
	#TODO (Nastia): insert appropriate Python code here -> :-)
	eng.eval('R=ButterLWDF2FWR( %d, %f);'%(filter.n, filter.Wn), nargout=0)
	R = eng.eval('struct(R)')

	# build SIF
	return { "JtoS": ( (mat(R['J']), mat(R['K']), mat(R['L']), mat(R['M']), mat(R['N']), mat(R['P']), mat(R['Q']), mat(R['R']), mat(R['S'])) ) }



def acceptLWDF(filter):
	"""
	a LWDF Realization can be build only if the filter is a ODD Butterworth filter
	"""
	return filter.isButter() and (filter.n%2)==1


LWDF = Structure( shortName='LWDF', fullName="Lattice Wave Digital Filter", make=makeLWDF, accept=acceptLWDF)
