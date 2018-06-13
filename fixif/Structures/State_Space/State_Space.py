#coding: UTF8

"""
This file contains State-Space structure

"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.Structures.Structure import Structure
from numpy import eye, zeros



def makeSS(filt, form=None):
	"""
	Factory function to make a state-space Realization

	One option:
	- form: None, 'balanced', 'ctrl' or 'obs'

	Returns
	- a dictionary of necessary infos to build the Realization
	"""

	if form is None:
		S = filt.dSS
	elif form == 'balanced':
		S = filt.dSS.balanced()
	elif form == 'ctrl' or form == 'obs':
		S = filt.dTF.to_dSS(form)
	else:
		raise ValueError("State-Space: the form '%s' is invalid. Must be in (None, 'balanced', 'ctrl', 'obs')"%form)

	n, p, q = S.size
	l = 0
	JtoS = (eye(l), zeros((n,l)), zeros((p,l)), zeros((l,n)), zeros((l,q)), S.A, S.B, S.C, S.D)

	return {"JtoS": JtoS}



def acceptSS(filt, form ):
	"""
	The forms 'ctrl' and 'obs' cannot be applied to MIMO filters
	'balanced' form is for stable filter
	otherwise, it can always be used
	"""
	if form == 'balanced':
		return filt.isStable()
	if form == 'ctrl' or form == 'obs':
		return filt.isSISO()

	# otherwise
	return True


# do not propose "balanced" form when slycot is not installed
try:
	import slycot
except ImportError:
	State_Space = Structure(shortName="SS", fullName="State-Space", options={'form': (None, 'ctrl', 'obs')}, make=makeSS, accept=acceptSS)
else:
	State_Space = Structure( shortName="SS", fullName="State-Space", options={'form': (None, 'balanced', 'ctrl', 'obs')}, make=makeSS, accept=acceptSS)
