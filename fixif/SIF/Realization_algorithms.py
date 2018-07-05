# coding: utf-8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from jinja2.loaders import FileSystemLoader
from jinja2 import Environment, PackageLoader
from numpy import tril, all, r_, c_, mat, zeros, eye
from scipy.linalg import norm
# from fixif.func_aux import scalarProduct
from textwrap import wrap



def scalarProduct(var, coefs, dcoefs=None, hexa=False):
	"""
	Return a string corresponding to a scalar product (dot product) between a vector of variables (var) and a vector of coefficients (coefs)

	Ex: var(0)*coefs(0) + var(1)*coefs(1) + ... + var(n-1)*coefs(n)

	Parameters:
		- var: list of name of the variables
		- coefs: vector of coefficients used in the scalar product (np.matrix, so 2d)
		- dcoefs: vector of values (1 or 0) indicating if the associated coefficient is trivial (0 or not): comes from the dZ matrix
		- hexa: True to display the coefficients in floating-point hexadecimal
	Returns string
	The coefficients are converted in their litteral floating-point hexadecimal representation (exact representation)
	"""
	if dcoefs is None:
		dcoefs = [1]*coefs.shape[0]

	# iterate over each coefficient	and variable for the dot product
	dp = []
	for v, c, dv in zip(var, coefs.tolist()[0], dcoefs):
		if dv == 1:
			dp.append(v+'*'+float.hex(c))
		else:
			if c == 1:
				dp.append(v)
			elif c == -1:
				dp.append('-' + v)
			elif c != 0:
				dp.append(v + '*' + float.hex(c))

	S = " + ".join(dp)
	if S == "":
		S = "0"
	return "\n".join(wrap(S, 60))










class R_algorithm:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the algorithmXXX methods in the Realization class
	the Realization class will inherit from R_algorihtm class
	"""
	def algorithmLaTeX(self, caption=None):

		"""
		Generate a tex file to use with package algorithm2e to create a LaTex output of algorithm
		- `caption` is an additional caption
		"""

		env = Environment(loader=FileSystemLoader('fixif/SIF/templates'),#PackageLoader('fixif', 'SIF/templates'),
					block_start_string='%<',
					block_end_string='>%',
					variable_start_string='<<',
					variable_end_string='>>',
					comment_start_string='[§',
					comment_end_string='§]',
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
			comp_str += "\t\\tcp{\\emph{Permutations}}\n"
			comp_str += "\t$xn \\leftarrow xnp$\;"

		texDict['computations'] = comp_str

		return texPlate.render(**texDict)


# %< macro declare(baseName, numVar, kwName) >%
# %< if numVar > 1>%
# 	\<<kwName>>{$<<baseName>>$: array [1..<<numVar>>] of reals}
# %<- else >%
# 	\<<kwName>>{$<<baseName>>$: real}
# %<- endif >%
# %< endmacro >%

# <<declare('u', u.numVar, 'KwIn')>>
# <<declare('y', y.numVar, 'KwOut')>>
# %< if isPnut >%
# <<declare('xn, xnp', xn.numVar, 'KwData')>>
# %< else >%
# <<declare('xn', xn.numVar, 'KwData')>>
# %< endif >%
# <<declare('T', T.numVar, 'KwData')>>

		#- generic names with time (t with/without time)
		#- surname with time (t without time)
		#- generic names without time (input: u, output: y, intern static array: x)

	def algorithmTxt(self, coefFormat=None, withTime=True, withSurname=False, comments=True):
		"""
		Generate the algorithm core in text
		- coefFormat: (str) formatter used to display the coefficients. If empty, floating-point hexadecimal is used.
		Otherwise, should be in C formatting format (like "%4.f" for example)
		"""
		# names of the variables T, X and U
		varTXU = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameT]
		varTXU.extend(v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameX)
		varTXU.extend(v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameU)
		# names of the variables T, X and Y
		varTXY = [v.toStr(withTime=withTime, shift=1, withSurname=withSurname) for v in self._varNameT]
		varTXY.extend(v.toStr(withTime=withTime, shift=1, withSurname=withSurname) for v in self._varNameX)
		varTXY.extend(v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameY)

		# iter over all SoP
		algoStr = []
		for i in range(1, self._l + self._n + self._p + 1):
			# comments
			if comments:
				if i == 1 and self._l>0:
					algoStr.append("/ Temporary variables /")
				elif (i == self._l+1) and self._n > 0:
					algoStr.append("/ States /")
				elif i == self._l + self._n + 1:
					algoStr.append("/ Outputs /")
			# sum of product
			algoStr.append(varTXY[i-1] + '<-' + scalarProduct(varTXU, self.Zcomp[i, :].tolist()[0], self.dZ[i, :].tolist()[0], coefFormat) + '\n')

		return "\n".join(algo)

