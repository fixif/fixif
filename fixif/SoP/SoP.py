# coding=utf8

"""Class SoP to deal with Sum-of-Products

A Sum-of-Products is defined by s = sum_{i=0}^{n-1} c_i * v_i
where
- n (integer) is the number of termes
- the c_i are n constants
- the v_i are n variables (with given names)
"""


__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2019, FiXiF, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from textwrap import wrap


class SoP:
	"""Sum-of-Product class

	Attributes:
		- list of Constants
		- names of the variables (list of)
		- name of the result s
	"""
	def __init__(self, constants, varNames, resName):
		"""
		Build a SoP
		:param constants: list of constants (float)
		:param varNames: list of names (string)
		:param resName: name (string) of the result

		"""
		# store the values
		self._constants = constants
		self._varNames = varNames
		self._resName = resName
		# check the size
		if len(constants) != len(varNames):
			raise ValueError("The list of constants and the list of names must have the same size!")


	def toAlgoStr(self, assign='<-', coefFormat=None):
		"""
		Returns a string corresponding to the scalar product
		Ex: res <- var(0)*coefs(0) + var(1)*coefs(1) + ... + var(n-1)*coefs(n)

		Parameters:
			- assign: (str) string used for the assignment ('<-' in the example)
			- coefFormat: (str) formatter used to display the coefficients. If empty, floating-point hexadecimal is used.
			Otherwise, should be in C formatting format (like "%4.f" for example)
		Returns string
		The coefficients are converted in their litteral floating-point hexadecimal representation (exact representation)
		"""
		# iterate over each coefficient	and variable for the dot product
		dp = []
		for var, co in zip(self._varNames, self._constants):
			if co == 1:
				dp.append(var)
			elif co == -1:
				dp.append('-' + var)
			elif co:
				dp.append((coefFormat % (co,) if coefFormat else co.hex()) + '*' + var)

		S = " + ".join(dp)
		if S == "":
			S = "0"
		if self._resName == S:
			return ''
		else:
			return "\n".join(wrap(self._resName + ' ' + assign + ' ' + S, 60))



	def __str__(self):
		"""display the SoP"""
		return self.toAlgoStr('%4f')
