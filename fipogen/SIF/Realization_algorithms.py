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
from textwrap import wrap
from numpy import tril, all, r_, c_
from datetime import datetime
from re import compile, sub


# list of methods to be added to the Realization class
__all__ = [ "algorithmCdouble", "algorithmLaTeX"]


regVar = compile("(.*)\((k.*)\)")	# catch stuff like 'u_i(k-2)' in 'u_i' and 'k-2'

def scalarProduct(var, coefs, dcoefs=None):
	"""
	Return a string corresponding to a scalar product (dot product) between a vector of variables (var) and a vector of coefficients (coefs)

	Ex: var(0)*coefs(0) + var(1)*coefs(1) + ... + var(n-1)*coefs(n)

	Parameters:
		- var: list of name of the variables
		- coefs: vector of coefficients used in the scalar product (np.matrix, so 2d)
		- dcoefs: vector of values (1 or 0) indicating if the associated coefficient is trivial (0 or not): comes from the dZ matrix

	Returns string
	The coefficients are converted in their litteral floating-point hexadecimal representation (exact representation)
	"""
	if dcoefs is None:
		dcoefs = [1]*coefs.shape[0]
	S = " + ".join( v+'*'+float.hex(c) for v,c, dv in zip(var, coefs.flat, dcoefs.flat) if dv==1)
	if S == "":
		S = "0"
	return "\n".join( wrap(S, 60))



def genVarName(baseName, nbVar):
	"""
	Generate a list of variable name, based on the basedName and the number of variable
	genVarName( 'u', nbVar) returns:
	- 'u(k)' if nbVar == 1
	- otherwise [ 'u_1(k)', 'u_2(k)', ..., 'u_n(k)' ]
	"""
	if nbVar == 1:
		return [ baseName ]
	else:
		return [ baseName+"[%d]"%i for i in range(nbVar) ]



def algorithmCdouble(self, funcName, commentName=""):
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
	cDict['SIFname'] = commentName
	cDict['date'] = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")

	l,n,p,q = self.size

	# Lower triangular part non-null ?
	# in that case, we can directly store the computation of x(k+1) in x(k)
	# (no need to first compute x(k+1), and then store x(k+1) in x(k) to prepare the next step)
	isPlt = all(tril(self.P, -1) == 0)

	# input(s), output(s), states, intermediate variables
	strU = genVarName('u', q)
	strY = genVarName('y', p)
	strXk = genVarName('xk', n)
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

	signature.append( 'double* xn')
	cDict['InVar'] = ', '.join(signature)

	# declare the output variable if necessary, and all the intermediate variables
	cDict['ExtraVar'] = ''
	if p != 1:
		cDict['ExtraVar'] = ''
	else:
		cDict['ExtraVar'] = '\tdouble y;'


	# do all the computations
	# intermediate variables J.t = M.x(k) + N.u(k)
	# states x(k+1) =  K.t + P.x(k) + Q.u(k)
	# and outputs y(k) = L.t + R.x(k) + S.u(k)
	comp = []
	for i in range(0, l+n+p):
		comp.append( "\t" + strTXY[i] + " = " + scalarProduct( strTXU, self.Z[i,:], self.dZ[i,:] ) + ";\n" )
	cDict["InterComp"] = "".join( comp[0:l] )
	cDict["StatesComp"] = "".join( comp[l:l+n] )
	cDict["OutComp"] = "".join( comp[l+n:] )


	# permutation
	cDict['Permutations'] = ""

	if isPlt:
		cDict['Permutations'] += "\t//permutations\n"
		for i in range(n):
			cDict['Permutations'] +=  "\t" + strXk[i] + " = " + strXkp[i] + ";\n"

	if p==1:
		cDict['return'] = "\treturn y;"

	cRender = cTemplate.render(**cDict)

	return cRender
	#print(cRender)

	# if fileName is None:
	# 	fileName = funcName + '.c'
	# elif not(fileName.endswith('.c')):
	# 	fileName = fileName + ".c"
	#
	# with open(fileName, 'w') as outFile:
	# 	outFile.write(cRender)







# Found inspiration here
# http://martin-ueding.de/en/latex/computation-results/index.html



def algorithmLaTeX(R, out_file, caption=None):

	"""

	Generate a tex file to use with package algorithm2e to create a LaTex output of algorithm

	- `R` is a SIF object
	- `caption` is an additional caption
	- `out_file` is the name of the tex output

	"""



	env = Environment(loader=PackageLoader('SIF','templates'),
		block_start_string= '%<',
		block_end_string = '>%',
		variable_start_string = '<<',
		variable_end_string = '>>',
		comment_start_string= '[§',
		comment_end_string = '§]',
		trim_blocks=True,
		lstrip_blocks=True )

	texPlate = env.get_template('algorithmLaTeX_template.tex')

	l,m,n,p = R.size

	texDict = {}

	# Lower triangular part non-null ?
	isPnut = True

	if all(tril(R.P,-1) == 0):
		isPnut = False

	texDict['isPnut'] = isPnut

	strTXU = _genVarName('T', l) + _genVarName('xn', n) + _genVarName('u', m)

	if isPnut:
		strTXY = _genVarName('T', l) + _genVarName('xnp', n) + _genVarName('y', m)
	else:
		strTXY = _genVarName('T', l) + _genVarName('xn', n) + _genVarName('y', m)

	#Caption
	if caption is None:
		caption = "Pseudocode algorithm ..."

	texDict["caption"] = caption

	texDict['u'] = {}
	texDict['y'] = {}
	texDict['xn'] = {}
	texDict['T'] = {}

	#Inputs
	texDict['u']['numVar'] = m
	#Outputs
	texDict['y']['numVar'] = p
	#States
	texDict['xn']['numVar'] = n
	#Intermediate variables
	texDict['T']['numVar'] = l

	Zbis = R.Z + mat(r_[c_[eye(l), zeros((l,n+m))], zeros((n+p,l+n+m))])

	comp_str = ""

	for i in range(1, l+n+p+1):

		if i == 1:
			comp_str += "\t\\tcp{\\emph{Intermediate variables}}\n"
		elif (i == l+1) and not(n == 0):
			comp_str += "\t\\tcp{\\emph{States}}\n"
		elif (i == l+n+1):
			comp_str += "\t\\tcp{\\emph{Outputs}}\n"

		comp_str += "\t" + "$" + strTXY[i-1] + " \leftarrow " + _scalprodCdouble(Zbis[i-1,:],strTXU) + "$\;\n"

	if isPnut:

		comp_str += " \n\t\\tcp{\\emph{Permutations}}\n"
		comp_str += "\t$xn \\leftarrow xnp$\;"

	# jinja2 only works with unicode
	texDict['computations'] = unicode(comp_str, 'utf-8')

	texContents = texPlate.render(**texDict)

	print(texContents)


