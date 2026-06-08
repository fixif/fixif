# coding: utf8

"""
This file contains Lattice Wave Digital Filter

"""

__author__ = "Thibault Hilaire, Anastasia Volkova"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Anastasia Volkova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures.Structure import Structure
from numpy import matrix as mat
from fixif.func_aux import MatlabHelper, isMatlabInstalled



def makeLWDF(filt):
	"""
	make a LWDF filter, using LWDF matlab library and some matlab code
	"""
	# connect to matlab if not already connected
	MH = MatlabHelper(raiseError=True)
	# add path to matlab files
	MH.addpath('fixif/Structures/LWDF/matlab')
	# path to the LWDF matlab toolbox from TU Delf (http://www.latech.nl/mtbx)
	MH.addpath('fixif/Structures/LWDF/matlab/wdf_tbx')
	# call the TF2LWDF2SIF matlab function
	from matlab import double as m_double
	R = MH.TF2LWDF2SIF(m_double(filt.dTF.num.tolist()), m_double(filt.dTF.den.tolist()))

	# TODO: catch the errors ??


	# build SIF
	return {"JtoS": (
		mat(R['J']), mat(R['K']), mat(R['L']), mat(R['M']), mat(R['N']), mat(R['P']), mat(R['Q']), mat(R['R']),
		mat(R['S']))}


def acceptLWDF(filt):
	"""
	a LWDF realization can be build only if the filter is SISO and has ODD order
	"""
	return (filt.order % 2 == 1) and filt.isSISO()


# the LWDF structure is created only if Matlab (and the engine) are installed
if isMatlabInstalled():
	LWDF = Structure(shortName='LWDF', fullName="Lattice Wave Digital Filter", make=makeLWDF, accept=acceptLWDF)


