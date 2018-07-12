# coding: utf8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from textwrap import wrap


def scalarProduct(variables, coefs, coefFormat=None):
	"""
	Return a string corresponding to a scalar product (dot product) between a vector of variables (var) and a vector of coefficients (coefs)

	Ex: var(0)*coefs(0) + var(1)*coefs(1) + ... + var(n-1)*coefs(n)

	Parameters:
		- var: list of name of the variables
		- coefs: list of coefficients used in the scalar product
		- coefFormat: (str) formatter used to display the coefficients. If empty, floating-point hexadecimal is used.
		Otherwise, should be in C formatting format (like "%4.f" for example)
	Returns string
	The coefficients are converted in their litteral floating-point hexadecimal representation (exact representation)
	"""

	# iterate over each coefficient	and variable for the dot product
	dp = []
	for var, co in zip(variables, coefs):
		if co == 1:
			dp.append(var)
		elif co == -1:
			dp.append('-' + var)
		elif co:
			if coefFormat:
				dp.append(coefFormat % (co,) + '*' + var)
			else:
				dp.append(co.hex() + '*' + var)

	S = " + ".join(dp)
	if S == "":
		S = "0"
	return "\n".join(wrap(S, 60))

