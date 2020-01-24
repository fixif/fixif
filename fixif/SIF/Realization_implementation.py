# coding: utf-8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from jinja2 import Environment, FileSystemLoader
from numpy import tril, all, zeros, matrix as mat
from datetime import datetime
from subprocess import Popen, PIPE
from ctypes import CDLL, POINTER, c_double
import numpy


#TODO: put theses path into a global Option object (that can be modified elsewhere)

# set the PATHS
from inspect import getfile
from fixif import SIF
from fixif.SoP import SoP
from os.path import dirname
FIXIF_SIF_PATH = dirname(getfile(SIF))

GENERATED_PATH = FIXIF_SIF_PATH + '/../generated/code/'
TEMPLATE_PATH = FIXIF_SIF_PATH + '/templates/'


def genCvarNames(baseName, nbVar):
	"""
	Generate a list of C-language variable name, based on the basedName and the number of variable
	genCvarNames( 'u', nbVar) returns:
	- 'u' if nbVar == 1
	- otherwise [ 'u_1', 'u_2', ..., 'u_n' ]
	"""
	if nbVar == 1:
		return [baseName]
	else:
		return [baseName + "[%d]" % i for i in range(nbVar)]



class R_implementation:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the following methods in the Realization class
	the Realization class will inherit from R_algorihtm class
	"""


	def implementCdouble(self, funcName):
		"""
		Returns the C-code (with double coefficients) correspoding to the evaluation of SIF self for one time-step

		Parameters:
			- self: the SIF object
			- funcName: name of the function
		"""

		env = Environment(loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
		cTemplate = env.get_template('implementCdouble_template.c')

		cDict = {'funcName': funcName}  # dictionary used to fill the template
		if self._filter.isSISO():
			cDict['SIFname'] = self.name + '\n' + str(self._filter.dTF)
		else:
			cDict['SIFname'] = self.name + '\n' + str(self._filter.dSS)
		cDict['date'] = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")

		l, n, p, q = self.size

		# Lower triangular part non-null ?
		# in that case, we can directly store the computation of x(k+1) in x(k)
		# (no need to first compute x(k+1), and then store x(k+1) in x(k) to prepare the next step)
		isPlt = all(tril(self.P, -1) == 0)

		# input(s), output(s), states, intermediate variables
		strU = genCvarNames('u', q)
		strY = genCvarNames('y', p)
		strXk = genCvarNames('xk', n)
		strXkp = ['x%d_kp1' % (i,) for i in range(n)]
		strT = ['T%d' % (i,) for i in range(l)]

		strTXU = strT + strXk + strU

		if isPlt:
			strTXY = strT + strXk + strY
		else:
			strTXY = strT + strXkp + strY

		# define the input/output variables in the signature of the function
		signature = []
		if p == 1:
			cDict['OutVar'] = 'double'
		else:
			cDict['OutVar'] = 'void'
			signature.append('double* y')

		if q == 1:
			signature.append('double u')
		else:
			signature.append('double* u')

		signature.append('double* xk')
		cDict['InVar'] = ', '.join(signature)

		# declare the output variable if necessary, and all the intermediate variables
		cDict['ExtraVar'] = ''
		if not isPlt:
			cDict['ExtraVar'] += '\tdouble ' + ", ".join(strXkp) + ";\n"
		if p == 1:
			cDict['ExtraVar'] += '\tdouble y;'


		# do all the computations
		# intermediate variables J.t = M.x(k) + N.u(k)
		# states x(k+1) =  K.t + P.x(k) + Q.u(k)
		# and outputs y(k) = L.t + R.x(k) + S.u(k)
		comp = []
		for i in range(0, l+n+p):
			sop = SoP(self.Zcomp[i, :].tolist()[0], strTXU, strTXY[i])      # TODO: not tested yet (tested when it used productScalarOld function)
			comp.append("\t" + sop.toAlgoStr(" =") + ";\n")
		cDict["InterComp"] = "".join("\tdouble " + t for t in comp[0:l])
		cDict["StatesComp"] = "".join(comp[l:l+n])
		cDict["OutComp"] = "".join(comp[l+n:])

		# if l>0:
		# 	cDict["InterComp"] += 'printf("T=' + "%a, "*l + '\\n",' + ", ".join(strT) + ');\n'
		# cDict["StatesComp"] += 'printf("X=' + "%a, "*n + '\\n",' + ", ".join(strXk) + ');\n'
		# cDict["OutComp"] += 'printf("Y=' + "%a, " * p + '\\n",' + ", ".join(strY) + ');\n' + 'printf("U=' + "%a, " * q + '\\n",' + ", ".join(strU) + ');'


		# permutation
		cDict['Permutations'] = ""

		if not isPlt:
			cDict['Permutations'] += "\t//permutations\n"
			for i in range(n):
				cDict['Permutations'] += "\t" + strXk[i] + " = " + strXkp[i] + ";\n"

		if p == 1:
			cDict['return'] = "\treturn y;"

		return cTemplate.render(**cDict)



	def makeCdouble(self):
		"""
		Generate C code, compile it and link it with ctypes
		"""
		# TODO: manage the place where the code is generated (it should be an absolute path?)

		# generate C code
		with open(GENERATED_PATH+"runC.c", "w") as cFile:
			cFile.write(self.implementCdouble("implementCdouble"))

		print("Compiling runC.c")

		# compile it
		proc = Popen("cd " + GENERATED_PATH + "&& cc -Wall -fPIC -shared -o runC.so runC.c ", stderr=PIPE, shell=True)
		# check the output and print it
		line = 'non-empty'
		while line:
			line = proc.stderr.readline().decode('utf-8')
			print(line[:-1])		# TODO: log it somewhere ?

		# use ctype
		self._Cdouble = CDLL(GENERATED_PATH + 'runC.so').implementCdouble
		if self.p == 1:
			self._Cdouble.argtypes = (c_double if self._q == 1 else POINTER(c_double), POINTER(c_double))
		else:
			self._Cdouble.argtypes = (POINTER(c_double), c_double if self._q == 1 else POINTER(c_double), POINTER(c_double))





	def runCdouble(self, u):
		"""
		Generates C code with double, compile it, and run it with the given input u
		Parameters
		----------
		- self: the SIF object
		- u: the input (qxN), where N is the number of samples

		Returns the ouput (pxN)
		"""
		# generate and compile code, if it is not yet done
		if self._Cdouble is None:
			self.makeCdouble()

		u = mat(u)
		N = u.shape[1]

		x = zeros((self._n, 1))		# TODO: add the possibility to start with a non-zero state
		px = x.ctypes.data_as(POINTER(c_double))
		y = zeros((self._p, N))

		# loop to compute the outputs
		if self.p == 1 and self.q == 1:
			for i in range(N):
				y[:, i] = self._Cdouble(u[:, i], px)
		return y