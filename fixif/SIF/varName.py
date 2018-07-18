# coding=utf8

"""
This class is used for the name of the variables
the variables can be named t(k), x(k), etc.
but also be renamed
they can be used for LaTeX export (so 't_1' or 't_{10}') but also for C code ('t1' or 't10')
"""


__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



class varName:

	def __init__(self, SIFname, SIFindex=None, surname=None, index=None, shift=0):
		"""
		Constructor
		:param SIFname:
		:param SIFindex:
		:param surname:
		:param shift:
		"""
		self._SIFname = SIFname
		self._SIFindex = SIFindex
		self._surname = surname if surname is not None else SIFname
		self._index = index
		self._shift = shift


	def toStr(self, withTime=True, shift=0, withSurname=False, suffix='', LaTeX=False):
		"""
		a method to display a varName in different ways:
		- generic names with time (t with/without time)
		- surname with time (t without time)
		- generic names without time (input: u, output: y, intern static array: x)

		withTime: (bool) adds the time "(k)" or "(k+1)"
		shift: (int) defines the shift (in time, ie shift=1 for time (k+1)
		withSurname: (bool) uses surname instead of name
		suffix: (str) add a suffix to the name (before the '_')

		>>> u=varName('u');
		>>> t=varName('x', 2, surname='u', index=3, shift=-1)		# t(k) = x_2(k) or t(k) = u_3(k-1)
		>>> u.toStr()
		>>> 'u(k)'
		>>> u.toStr(withTime=False)
		>>> 'u'
		>>> t.toStr()
		>>> 'x_2(k)'
		>>> t.toStr(shift=1)
		>>> 'x_2(k+1)'
		>>> t.toStr(withSurname=True)
		>>> 'u_3(k-1)'
		>>> t.toStr(withSurname=True, shift=2)
		>>> 'u_3(k+1)'
		>>> t.toStr(withSurname=True, shift=2, suffix='p')
		>>> 'up_3(k+1)'
		"""
		# name or surname
		s = self._surname if withSurname else self._SIFname
		# add the index
		index = self._index if withSurname else self._SIFindex
		if LaTeX:
			s += '_{'
		s += '' if index is None else str(index)
		if LaTeX:
			s += '}'
		# add the suffix
		s = s + suffix
		# add time
		if withTime:
			if withSurname:
				shift += self._shift
			if shift == 0:
				s += '(k)'
			else:
				s += '(k%+d)' % (shift,)
		return s


def generateNames(baseName, nbVar, surnames=None):
	"""
	Generate a list of varName, based on the basedName, the number of variable and a list of surnames
	the surnames are string, or tuple (surname, index, shift)
	generateList( 'u', nbVar) returns:
	- [varName('u',0)] if nbVar == 1	(ie it means 'u(k)')
	- otherwise [ varName('u', 1, 0) , varName('u',2, 0) , ..., varNames('u', n,0 ) ] that means 'u_1(k)', ...
	"""
	if surnames is not None and len(surnames) != nbVar:
		raise ValueError("generateNames: A wrong number of surnames are given")
	# initial values when surnames is None
	if surnames is None:
		surnames = [(None, i+1 if nbVar > 1 else None, 0) for i in range(nbVar)]
	elif isinstance(surnames[0], str):		# simple surnames, without index and shift
		surnames = [(s, None, 0) for s in surnames]

	return [varName(baseName, i+1 if nbVar > 1 else None, sn, ind, sh) for i, (sn, ind, sh) in enumerate(surnames)]


