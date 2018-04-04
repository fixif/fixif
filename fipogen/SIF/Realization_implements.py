#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from jinja2 import Environment, PackageLoader
from numpy import tril, all
from datetime import datetime
from fipogen.func_aux import scalarProduct

from numpy import matrix as mat, zeros,eye, empty, float64
from scipy.weave import inline

#used to build the Cython module
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from imp import load_dynamic, find_module, load_module

import numpy
from time import time

GENERATED_PATH = 'generated/code/'



# list of methods to be added to the Realization class
__all__ = ["implementCdouble", "makeModule", "runCdouble"]



def genCvarNames(baseName, nbVar):
	"""
	Generate a list of C-language variable name, based on the basedName and the number of variable
	genCvarNames( 'u', nbVar) returns:
	- 'u' if nbVar == 1
	- otherwise [ 'u_1', 'u_2', ..., 'u_n' ]
	"""
	if nbVar == 1:
		return [ baseName ]
	else:
		return [ baseName+"[%d]"%i for i in range(nbVar) ]



def implementCdouble(self, funcName):
	"""
	Returns the C-code (with double coefficients) correspoding to the evaluation of SIF self for one time-step

	Parameters:
		- self: the SIF object
		- funcName: name of the function
	"""

	env = Environment( loader=PackageLoader('fipogen','SIF/templates'), trim_blocks=True, lstrip_blocks=True )
	cTemplate = env.get_template('implementC_template.c')

	cDict = {}	# dictionary used to fill the template
	cDict['funcName'] = funcName
	if self._filter.isSISO():
		cDict['SIFname'] = self.name + '\n' + str(self._filter.dTF)
	else:
		cDict['SIFname'] = self.name + '\n' + str(self._filter.dSS)
	cDict['date'] = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")

	l,n,p,q = self.size

	# Lower triangular part non-null ?
	# in that case, we can directly store the computation of x(k+1) in x(k)
	# (no need to first compute x(k+1), and then store x(k+1) in x(k) to prepare the next step)
	isPlt = all(tril(self.P, -1) == 0)

	# input(s), output(s), states, intermediate variables
	strU = genCvarNames('u', q)
	strY = genCvarNames('y', p)
	strXk = genCvarNames('xk', n)
	strXkp = [ 'x%d_kp1'%(i) for i in range(n) ]
	strT = 	[ 'T%d'%(i) for i in range(l) ]

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
		signature.append( 'double u')
	else:
		signature.append( 'double* u')

	signature.append( 'double* xk')
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
		comp.append( "\t" + strTXY[i] + " = " + scalarProduct( strTXU, self.Zcomp[i,:], self.dZ[i,:] ) + ";\n" )
	cDict["InterComp"] = "".join( "\tdouble "+ t for t in comp[0:l] )
	cDict["StatesComp"] = "".join( comp[l:l+n] )
	cDict["OutComp"] = "".join( comp[l+n:] )

	# if l>0:
	# 	cDict["InterComp"] += 'printf("T=' + "%a, "*l + '\\n",' + ", ".join(strT) + ');\n'
	# cDict["StatesComp"] += 'printf("X=' + "%a, "*n + '\\n",' + ", ".join(strXk) + ');\n'
	# cDict["OutComp"] += 'printf("Y=' + "%a, " * p + '\\n",' + ", ".join(strY) + ');\n' + 'printf("U=' + "%a, " * q + '\\n",' + ", ".join(strU) + ');'


	# permutation
	cDict['Permutations'] = ""

	if not isPlt:
		cDict['Permutations'] += "\t//permutations\n"
		for i in range(n):
			cDict['Permutations'] +=  "\t" + strXk[i] + " = " + strXkp[i] + ";\n"

	if p==1:
		cDict['return'] = "\treturn y;"

	return cTemplate.render(**cDict)



def makeModule(self):
	"""
	Generate C and Cython codes, compile them, build the Python module and import it
	"""

	env = Environment( loader=PackageLoader('fipogen','SIF/templates'), trim_blocks=True, lstrip_blocks=True )
	cTemplate = env.get_template('runC_template.c')
	cythonTemplate = env.get_template('runCython_template.pyx')

	# empty dictionay used for the template
	cDict = {}
	if self._filter.isSISO():
		cDict['SIFname'] = self.name + '\n' + str(self._filter.dTF)
	else:
		cDict['SIFname'] = self.name + '\n' + str(self._filter.dSS)
	cDict['date'] = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")

	pu_str = '*u' if self.q == 1 else 'u'
	if self.p == 1:
		cDict[ 'callImplementCdouble'] = '*y = implementCdouble(%s, xk);'%pu_str
	else:
		cDict['callImplementCdouble'] = 'implementCdouble(y, %s, xk);'%pu_str
	cDict[ 'SIF' ] = self

	# add the implement functions
	cDict['implementFunctions'] = self.implementCdouble("implementCdouble")		# implementCdouble

	# write the C file
	with open(GENERATED_PATH+"runC.c", "w") as cFile:
		cFile.write( cTemplate.render(**cDict) )	# write the C function containing the `implementC` functions and `runC` functions

	# write the Cython file
	with open(GENERATED_PATH+"runCython.pyx", "w") as cFile:
		cFile.write(cythonTemplate.render(**cDict))  # write the Cython wrapper

	# build all (in GENERATED_PATH)

	uniqueName = 'runC'+str(time()).replace('.','')
	setup(
		cmdclass = {'build_ext': build_ext},
		ext_modules = [ Extension(uniqueName,
								sources=[GENERATED_PATH+"runCython.pyx", GENERATED_PATH+"runC.c"],
								extra_compile_args=['-Wno-unused-function'],
								include_dirs=[numpy.get_include()]) ],
		script_args = ['build_ext', '--build-lib', GENERATED_PATH,  '--force']
	)

	# and finally import it
	self._runModule = load_dynamic(uniqueName,GENERATED_PATH+uniqueName+'.so')
	#f, pathname, desc = find_module( 'runC', ['.'])
	#self._runModule = load_module('runC', f, pathname, desc)




def runCdouble(self, u):
	"""
	Generates C code with double, compile it, and run it with the given input u
	Parameters
	----------
	self: the SIF object
	u: the input (qxN), where N is the number of samples
	Returns:
		the ouput (pxN)
	"""
	if self._runModule is None:
		self.makeModule()

	ut = numpy.ascontiguousarray( u.transpose())

	return self._runModule.simCdouble( ut).transpose()
