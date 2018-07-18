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
from fixif.func_aux import scalarProduct
from textwrap import wrap



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
		- withTime: True if the variable are labeled with time (cannot be False if withSurname is True)
		- withSurname: True if the surname of the variables (when they exist) are used; in that case, the temporary variables do not have time (t instead of t(k+1))
		Otherwise, should be in C formatting format (like "%4.f" for example)
		"""
		# if withSurname and not withTime:
		#	raise ValueError("algorithmTxt: wichSurname=True and withTime=False are incoherent")
		# TODO: keep this test BUT ONLY when at least one varName has a surname with time (with shift != 0)

		# Lower triangular part non-null ?
		isPnut = True
		if all(tril(self.P, -1) == 0):
			isPnut = False

		# names of the variables T, X and U
		varT = [v.toStr(withTime=withTime, shift=1, withSurname=withSurname) for v in self._varNameT]
		varTnoTime = [v.toStr(withTime=withTime and not withSurname, shift=1, withSurname=withSurname) for v in self._varNameT]	 # variable T without time when its with surname
		varX = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameX]
		varU = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameU]
		varTXU = varT + varX + varU
		varTXUnoTime = varTnoTime + varX + varU
		# names of the variables T, X and Y
		varXp1 = [v.toStr(withTime=withTime, shift=1, withSurname=withSurname, suffix='p' if isPnut else '') for v in self._varNameX]
		varY = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname) for v in self._varNameY]
		varTXY = varT + varXp1 + varY
		varTXYnoTime = varTnoTime + varXp1 + varY

		# varTXU and varTXUnoTime is just a trick when withSurname=True: we don't want to display useless line, like "v(k)<-v(k)".
		# But when the time is removed with surname, we can have (it happens with DFII), something like "t<-v(k)" (here the surname of t(k+1) is v(k)
		# in "v(k)<-v(k)" the 2nd comes from the surname of t, the 1st is because v(k-1) is the surname of x(k), but we display x(k+1)
		# to avoid this, we build the "src <- dest" line with varTXU (without time removed for the temporary variables), and if src is different than dest
		# then we use varTXUnoTime for the display

		# iter over all SoP
		algoStr = []
		for i in range(self._l + self._n + self._p):
			# comments
			if comments:
				if i == 0 and self._l > 0:
					algoStr.append("/ Temporary variables /")
				elif (i == self._l) and self._n > 0:
					algoStr.append("/ States /")
				elif i == self._l + self._n:
					algoStr.append("/ Outputs /")
			# sum of product
			src = varTXY[i]
			dst = scalarProduct(varTXU, self.Zcomp[i, :].tolist()[0], coefFormat)	 # varTXU is used for dst and the comparison with src
			if src != dst:
				# finally, we use the varTXUnoTime for the result
				src = varTXYnoTime[i]
				dst = scalarProduct(varTXUnoTime, self.Zcomp[i, :].tolist()[0], coefFormat)
				if (src + ' <- ' + dst) not in algoStr:		# to avoid redondant lines (append for DFI with surname)
					algoStr.append(src + ' <- ' + dst)

		return "\n".join(algoStr)

