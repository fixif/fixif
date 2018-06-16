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
from numpy import tril, all, r_, c_


# list of methods to be added to the Realization class
__all__ = [ "algorithmLaTeX"]






def algorithmLaTeX(R, out_file=None, caption=None):

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
		elif i == l+n+1:
			comp_str += "\t\\tcp{\\emph{Outputs}}\n"

		comp_str += "\t" + "$" + strTXY[i-1] + " \leftarrow " + _scalprodCdouble(Zbis[i-1,:],strTXU) + "$\;\n"

	if isPnut:

		comp_str += " \n\t\\tcp{\\emph{Permutations}}\n"
		comp_str += "\t$xn \\leftarrow xnp$\;"

	# jinja2 only works with unicode
	texDict['computations'] = unicode(comp_str, 'utf-8')

	texContents = texPlate.render(**texDict)

	print(texContents)


