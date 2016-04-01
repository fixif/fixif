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

# list of methods to be added to the Realization class
__all__ = ["implementCdouble"]



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
	Returns (as a string) the C-code (with double coefficients) corresping to the SIF self
	The C code is generated from the template `algorithmC_template.c` in the folder directory

	Parameters:
		- self: the SIF object
		- funcName: name of the function
		- commentName: name of the SIF to be added in the comment (the name of the structure ?)
	"""

	env = Environment( loader=PackageLoader('fipogen','SIF/templates'), trim_blocks=True, lstrip_blocks=True )
	cTemplate = env.get_template('algorithmC_template.c')

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
	cDict['ExtraVar'] = '\tdouble ' + ", ".join(strXkp) + ";\n"
	if p == 1:
		cDict['ExtraVar'] += '\tdouble y;'


	# do all the computations
	# intermediate variables J.t = M.x(k) + N.u(k)
	# states x(k+1) =  K.t + P.x(k) + Q.u(k)
	# and outputs y(k) = L.t + R.x(k) + S.u(k)
	comp = []
	for i in range(0, l+n+p):
		comp.append( "\t" + strTXY[i] + " = " + scalarProduct( strTXU, self.Zcomp[i,:], self.dZ[i,:] ) + ";\n" )
	cDict["InterComp"] = "".join( comp[0:l] )
	cDict["StatesComp"] = "".join( comp[l:l+n] )
	cDict["OutComp"] = "".join( comp[l+n:] )


	# permutation
	cDict['Permutations'] = ""

	if not isPlt:
		cDict['Permutations'] += "\t//permutations\n"
		for i in range(n):
			cDict['Permutations'] +=  "\t" + strXk[i] + " = " + strXkp[i] + ";\n"

	cDict['Return'] = "return 12;\n" if p==1 else "=".join(strY)+"=0;\n"

	if p==1:
		cDict['return'] = "\treturn y;"

	cRender = cTemplate.render(**cDict)

	return cRender


