# coding=utf8

"""
This simple class is used for the name of the variables
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

	def __init__(self, name, surname=None, shift=0):
		self._name = name
		self._surname = surname if surname is not None else name
		self._shift = shift


	def toStr(self, withTime=True, shift=0, withSurname=False, suffix=''):
		"""
		a method to display a varName in different ways:
		- generic names with time (t with/without time)
		- surname with time (t without time)
		- generic names without time (input: u, output: y, intern static array: x)

		withTime: (bool) adds the time "(k)" or "(k+1)"
		shift: (int) defines the shift (in time, ie shift=1 for time (k+1)
		withSurname: (bool) uses surname instead of name
		suffix: (str) add a suffix to the name (before the '_')

		>>> u=varName('u'); t=varName('x_2', 'u_3',shift=-1)
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
		>>> t.toStr(withSurname=True, shift=2, prime='p')
		>>> 'up_3(k+1)'
		"""
		s = self._surname if withSurname else self._name
		if suffix:
			if '_' in s:
				s = s.replace('_', suffix+'_')
			else:
				s = s + suffix
		if withTime:
			shift += self._shift
			if shift == 0:
				s += '(k)'
			else:
				s += '(k%+d)' % (shift,)
		return s


def generateNames(baseName, nbVar):
	"""
	Generate a list of varName, based on the basedName and the number of variable
	generateList( 'u', nbVar) returns:
	- [varName('u',0)] if nbVar == 1	(ie it means 'u(k)')
	- otherwise [ varName('u_1',0) , varName('u_2',0) , ..., varNames('u_n',0) ] that means 'u_1(k)', ...
	if the number is larger than 9, braces are added ('u_{12}' for example) to be compliant with LaTeX
	"""
	if nbVar == 1:
		return [varName(baseName)]
	elif nbVar < 10:
		return [varName(baseName + "_%d" % (i+1)) for i in range(1, nbVar+1)]
	else:
		return [varName(baseName + "_{%d}" % (i + 1)) for i in range(1, nbVar+1)]




