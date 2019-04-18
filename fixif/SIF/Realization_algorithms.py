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
from latex.jinja2 import make_env
from datetime import datetime
from pylatexenc.latexencode import utf8tolatex

from fixif.config import SIF_TEMPLATES_PATH
from fixif.func_aux import scalarProduct

class R_algorithm:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the algorithmXXX methods in the Realization class
	the Realization class will inherit from R_algorihtm class
	"""
	def algorithmLaTeX(self, caption=None, coefFormat=None, withTime=False, withSurname=False):

		"""
		Generate a tex file to use with package algorithm2e to create a LaTex output of algorithm
		- `caption` is an additional caption
		"""

		def declare(lvar, Kwname, isStatic=False, suffix=''):
			"""generate algorithm2e code to declare variables"""
			if len(lvar) == 0:
				return ''
			elif len(lvar) == 1:
				return '\\%s{$%s$: %sreal}' % (Kwname, lvar[0].name+suffix, 'static ' if isStatic else '')
			else:
				return '\\%s{$%s$: %sarray [1..%d] of reals}' % (Kwname, lvar[0].name+suffix, 'static ' if isStatic else '', len(lvar))


		env = make_env(loader=FileSystemLoader(SIF_TEMPLATES_PATH))
		tpl = env.get_template('algorithmLaTeX_template.tex')

		algoStr = [s+r"\\" for s in self._algorithmCore(LaTeX=True, assign='$\leftarrow$', coefFormat=coefFormat, withTime=withTime, withSurname=withSurname)]

		# add comments
		algoStr.insert(self._l + self._n, r"\tcp{Outputs}" if self._p > 1 else r"\tcp{Output}")
		if self._n > 0:
			algoStr.insert(self._l, r"\tcp{States}" if self._n > 1 else r"\tcp{State}")
		if self._l > 0:
			algoStr.insert(0, r"\tcp{Temporary variables}" if self._l > 1 else r"\tcp{Temporary variable}")
		if withTime is False and self.isPnut():
			algoStr.append(r"\tcp{Swap states}")
			algoStr.append("$" + self._varNameX[0].name + ' \leftarrow ' + self._varNameX[0].name + "p$")

		# caption
		if caption is None:
			caption = utf8tolatex(self.name)		# TODO: complete ? caption should be a string, where we can insert self._Filter.name (like 'My algorithm of %s', or 'my algo' if we do not want to use self._Filter.name)

		# initialization
		init = [declare(self._varNameU, 'KwIn')]
		init.append(declare(self._varNameY, 'KwOut'))
		init.append(declare(self._varNameX, 'KwData', isStatic=True))
		init.append(declare(self._varNameT, 'KwData'))
		if withTime is False and self.isPnut():
			init.append(declare(self._varNameX, 'KwData', suffix='p'))

		return tpl.render(computations="\n".join(algoStr), caption=caption, initialization="\n".join(init), date=str(datetime.now()), SIF=self.name)




	def algorithmTxt(self, coefFormat=None, withTime=True, withSurname=False, comments=True):
		"""
		Generate the algorithm core in text
		- coefFormat: (str) formatter used to display the coefficients. If empty, floating-point hexadecimal is used.
		- withTime: True if the variable are labeled with time (cannot be False if withSurname is True)
		- withSurname: True if the surname of the variables (when they exist) are used; in that case, the temporary variables do not have time (t instead of t(k+1))
		Otherwise, should be in C formatting format (like "%4.f" for example)
		"""

		algoStr = self._algorithmCore(LaTeX=False, assign='<-', coefFormat=coefFormat, withTime=withTime, withSurname=withSurname)

		# comments
		if comments:
			algoStr.insert(self._l + self._n, "/ Outputs /" if self._p > 1 else "/ Output /")
			if self._n > 0:
				algoStr.insert(self._l, "/ States /" if self._n > 1 else "/ State /")
			if self._l > 0:
				algoStr.insert(0, "/ Temporary variables /" if self._l > 1 else "/ Temporary variable /")

		return "\n".join(algoStr)



	def _algorithmCore(self, LaTeX, assign, coefFormat, withTime, withSurname):
		"""
		Generate the algorithm core in text
		- coefFormat: (str) formatter used to display the coefficients. If empty, floating-point hexadecimal is used.
		- withTime: True if the variable are labeled with time (cannot be False if withSurname is True)
		- withSurname: True if the surname of the variables (when they exist) are used; in that case, the temporary variables do not have time (t instead of t(k+1))
		Otherwise, should be in C formatting format (like "%4.f" for example)
		"""
		if withSurname and not withTime:
			# it raises an error only when at least one varName has a surname with time (with shift != 0)
			v = [v for v in self._varNameT if v.hasSurnameWithIndex()]
			v.extend([v for v in self._varNameT if v.hasSurnameWithIndex()])
			if len(v) > 0:
				raise ValueError("algorithmTxt: wichSurname=True and withTime=False are incoherent")


		# names of the variables T, X and U
		varT = [v.toStr(withTime=withTime, shift=1, withSurname=withSurname, LaTeX=LaTeX) for v in self._varNameT]
		varTnoTime = [v.toStr(withTime=withTime and not withSurname, shift=1, withSurname=withSurname, LaTeX=LaTeX) for v in self._varNameT]	 # variable T without time when its with surname
		varX = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname, LaTeX=LaTeX) for v in self._varNameX]
		varU = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname, LaTeX=LaTeX) for v in self._varNameU]
		varTXU = varT + varX + varU
		varTXUnoTime = varTnoTime + varX + varU
		# names of the variables T, X and Y
		varXp1 = [v.toStr(withTime=withTime, shift=1, withSurname=withSurname, suffix='p' if self.isPnut() else '', LaTeX=LaTeX) for v in self._varNameX]
		varY = [v.toStr(withTime=withTime, shift=0, withSurname=withSurname, LaTeX=LaTeX) for v in self._varNameY]
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
			# sum of product
			src = varTXY[i]
			dst = scalarProduct(varTXU, self.Zcomp[i, :].tolist()[0], coefFormat)	 # varTXU is used for dst and the comparison with src
			if src != dst:
				# finally, we use the varTXUnoTime for the result
				src = varTXYnoTime[i]
				dst = scalarProduct(varTXUnoTime, self.Zcomp[i, :].tolist()[0], coefFormat)
				newLine = src + ' ' + assign + ' ' + dst
				if newLine not in algoStr:		# to avoid redondant lines (append for DFI with surname)
					algoStr.append(newLine)

		return algoStr
