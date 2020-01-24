# coding=utf8

"""Class SoP to deal with Fixed-Point Sum-of-Products

A Sum-of-Products is defined by s = sum_{i=0}^{n-1} c_i * v_i
where
- n (integer) is the number of termes
- the c_i are n constants (Constant objects)
- the v_i are n variables (those FPF is given)
The bounds of the sum s is given (it can be evaluated with WCPG when the SoP are used in a filter/controller)

The class is based on the SoP class (in func_aux)
"""


__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2019, FiXiF, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.SoP import SoP
from fixif.FxP import Constant, FPF
from operator import attrgetter

class FxPSoP(SoP):
	"""Fixed-Point Sum-of-Product class

	Attributes:
		- list of Constants (Constant objects)
		- names and FPF of the variables (list of)
		- name and FPF of the result s

		- method used for the sum-of-product
	"""
	def __init__(self, constants, varNames, varFPF, resName, resFPF):
		"""
		Build a SoP
		:param constants: list of constants (Constant objects)
		:param varNames: list of names (VarName objects) for the variables v_i
		:param varFPF: list of FPF for the variables v_i
		:param resName: name (VarName) of the result
		:param resFPF: FPF of the result
		"""
		# store the values
		self._constants = constants
		self._varFPF = varFPF
		self._resFPF = resFPF
		# each constant should be a Constant
		if any(not isinstance(c, Constant) for c in constants):
			raise ValueError("The constants should be a list of Constant objects (defined in Fixif.FxP)")
		# check the sizes
		if len({len(constants), len(varNames), len(varFPF)}) != 1:
			raise ValueError("The Constnants, the list of names and the list of FPF should have the same size!")
		# compute the FxP format of the products
		self._productFPF = [FPF(msb=v.msb+c.FPF.msb, lsb=v.lsb+c.FPF.lsb) for v, c in zip(varFPF, constants)]
		# initialize the SoP
		super(FxPSoP, self).__init__([c.value for c in constants], varNames, resName)


	def sumLaTeX(self, colors=None, axis=False, sort=False, hatches=False, xshift=0, yshift=0, **extra):
		"""Generate the LaTeX version of the SoP -> show the format of the products (their FxP format) and the result

		Arguments:
			- color: indicates the color theme, ie a 3-tuple with the colors of the sign, integer and fractional parts.
				If None, the colors are set using tikzstyles named 'sign', 'integer' and 'fractional' (so must be assigned elsewhere with "\tikzstyle{xxx}=[...]")
			- hatches: None if no hatches are displayed, otherwise hatches is a pair (msb,lsb) and hatches should be displayed for bits < msb and bits > lsb
			- axis: Trye if display a vertical axis on bit 0
			- sort: False, 'msb' or 'lsb' (sort the products with msb, lsb or do not sort them)
			- xshift, yshift: (int) shift the drawing if necessary
		"""
		# sorting the products FPF
		products = list(self._productFPF)
		if sort == 'msb':
			products.sort(key=attrgetter('msb'), reverse=True)
		elif sort == 'lsb':
			products.sort(key=attrgetter('lsb'))
		# generate LaTeX code for the products
		latexFPF = "\n".join([f.LaTeX(x_shift=xshift, y_origin=-i * 1.3 + yshift, colors=colors,
            hatches=((self._resFPF.msb, self._resFPF.lsb) if hatches else None), **extra) for i, f in enumerate(products)])
		latexFPF += "\n\t%result\n" + self._resFPF.LaTeX(x_shift=xshift,
			y_origin=-len(products) * 1.3 - 0.3 + yshift, colors=colors, **extra)
		minlsb = min(f.lsb for f in products + [self._resFPF])
		maxmsb = max(f.msb for f in products + [self._resFPF])
		latexFPF += "\n\t\\draw (%f,%f) -- (%f,%f) [color=black,line width=1pt];" % (
			-maxmsb - 1.2 + xshift, -len(products) * 1.3 + 1 + yshift,
			-minlsb + 0.2 + xshift, -len(products) * 1.3 + 1 + yshift)
		if axis:
			latexFPF += "\n\n\t\\draw (%f,%f) -- (%f,%f) [color=red];" % (
				xshift, 1.2 + yshift, xshift,
				-len(products) * 1.3 - 0.5 + yshift)

		return latexFPF
