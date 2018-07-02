#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from jinja2 import Environment, PackageLoader
from numpy import tril, all, r_, c_, mat, zeros, eye
from scipy.linalg import norm
from fixif.func_aux import scalarProduct


def genVarName(baseName, numVar):
	varNames = []

	if numVar is 1:
		varNames.append(baseName)
	else:
		for i in range(0, numVar):
			varNames.append(baseName + "_{" + str(i + 1) + "}")

	return varNames


class R_algorithm:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the algorithmXXX methods in the Realization class
	the Realization class will inherit from R_algorihtm class
	"""
	def algorithmLaTeX(self, out_file=None, caption=None):

		"""

		Generate a tex file to use with package algorithm2e to create a LaTex output of algorithm

		- `R` is a SIF object
		- `caption` is an additional caption

		"""

		# TODO: write it in a file ?

		env = Environment(loader=PackageLoader('fixif', 'SIF/templates'),
					block_start_string='%<',
					block_end_string ='>%',
					variable_start_string ='<<',
					variable_end_string ='>>',
					comment_start_string='[§',
					comment_end_string ='§]',
					trim_blocks=True,
					lstrip_blocks=True)

		texPlate = env.get_template('algorithmLaTeX_template.tex')

		l, n, p, q = self.size

		texDict = {}

		# Lower triangular part non-null ?
		isPnut = True

		if all(tril(self.P, -1) == 0):
			isPnut = False

		texDict['isPnut'] = isPnut

		strTXU = genVarName('T', l) + genVarName('xn', n) + genVarName('u', q)

		if isPnut:
			strTXY = genVarName('T', l) + genVarName('xnp', n) + genVarName('y', q)
		else:
			strTXY = genVarName('T', l) + genVarName('xn', n) + genVarName('y', q)

		# Caption
		if caption is None:
			caption = "Pseudocode algorithm ..."

		texDict["caption"] = caption

		texDict['u'] = {}
		texDict['y'] = {}
		texDict['xn'] = {}
		texDict['T'] = {}

		# Inputs
		texDict['u']['numVar'] = q
		# Outputs
		texDict['y']['numVar'] = p
		# States
		texDict['xn']['numVar'] = n
		# Intermediate variables
		texDict['T']['numVar'] = l

		comp_str = ""

		for i in range(1, l+n+p+1):

			if i == 1:
				comp_str += "\t\\tcp{\\emph{Intermediate variables}}\n"
			elif (i == l+1) and not(n == 0):
				comp_str += "\t\\tcp{\\emph{States}}\n"
			elif i == l+n+1:
				comp_str += "\t\\tcp{\\emph{Outputs}}\n"

			comp_str += "\t" + "$" + strTXY[i-1] + " \leftarrow " + scalarProduct(strTXU, self.Zcomp[i-1, :]) + "$\;\n"

		if isPnut:

			comp_str += " \n\t\\tcp{\\emph{Permutations}}\n"
			comp_str += "\t$xn \\leftarrow xnp$\;"

		# TODO: test jinja2 only works with unicode
		texDict['computations'] = comp_str

		texContents = texPlate.render(**texDict)

		return texContents


