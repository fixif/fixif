#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta" 

import SIF
from jinja2 import Environment, PackageLoader
from algorithmAuxFunc import _scalprodCdouble
from numpy import tril, all, r_, c_

def algorithmCfloat(R, funcName, fileName=None):
    
    env = Environment(loader=PackageLoader('SIF','templates'),
     trim_blocks=True,
     lstrip_blocks=True
     )
    
    cTemplate = env.get_template('algorithmC_template.c')
    
    cDict = {}
    
    cDict['funcName']=funcName
    
    l,m,n,p = R.size
    
    # Lower triangular part non-null ?
    isPnut = True
        
    if all(tril(R.P,-1) == 0):
        isPnut = False
    
    def _genVarName(baseName, numVar):
        
        varNames = []
        
        if numVar is 1:
            varNames.append(unicode(baseName,'utf-8'))
        else:
            for i in range(0, numVar):
                varNames.append(unicode(baseName + "[" + str(i) + "]",'utf-8'))
                
        return varNames
    
    # This test should be removed ???
    if not(p == 1):
    	raise("p should be equal to 1")
    
    #output(s)
    if p == 1:
        strY = ['y']
    else:
        strY = _genVarName('y', p)
    
    #states    
    if isPnut:
        strXn = _genVarName('(*xn)', n)
        strXnp = _genVarName('(*xnp)', n)
    else:
    	strXn = _genVarName('xn', n)
        
    #Input(s)
    if m == 1:
    	strU = ['u']
    else:
    	strU = _genVarName('u', m)
    	
    #Intermediate variables
    if l == 1:
    	strT = ['T']
    else:
    	strT = 	[ 'T'+str(i) for i in xrange(0,l)]
    	
    # i/o variables, c func
    
    variables = u''
    
    if m == 1:
    	variables += 'double u'
    else:
    	variables += 'double* u'
    	
    variables += ', '
    
    if isPnut:
    	variables += 'double** xn, double** xnp' 
    else:
    	variables += 'double* xn'
    
    cDict['variables'] = variables
    
    del(variables)
    	
    # Here is the part that imposes p == 1
    
    cDict['calculations'] = {}
    
    cDict['output'] = u'\t'
    cDict['output'] += "double y"
    
    
    # intermediate variables J.T = M.X(k) + N.U(k)
    cDict['calculations']['inter'] = u""
    
    for i in range(0, l):
    	print(l)
    	print(i)
    	cDict["calculations"]["inter"] += "\t" + "double " + strT[i] + " = " + _scalprodCdouble(c_[R.M[i,:], R.N[i,:], -R.J[i,0:i-2]], strXn + strU + strT[0:i-2]) + ";\n"
    
    
    
    # output Y(k) = R.X(k) + code.U(k) + L.T
    
    cDict['calculations']['outputs'] = u""
    
    for i in range(0, p):
    	cDict['calculations']['outputs'] += "\t" + strY[i] + " = " + _scalprodCdouble(c_[R.R[i,:], R.S[i,:], R.L[i,:]], strXn + strU + strT) + ";\n"
    
    # states X(k) = P.X(k) + Q.U(k) + K.T
    
    cDict['calculations']['states'] = u""
    
    for i in range (0, n):
    	if isPnut:
    		cDict['calculations']['states'] += "\t" + strXnp[i] + " = " + _scalprodCdouble(c_[R.P[i,:], R.Q[i,:], R.K[i,:]], strXn + strU + strT) + ";\n"
    	else:    
    		cDict['calculations']['states'] += "\t" + strXn[i] + " = " + _scalprodCdouble(c_[R.P[i,:], R.Q[i,:], R.K[i,:]], strXn + strU + strT) + ";\n"
    		
    # permutation
    
    cDict['calculations']['permutation'] = u""
    
    if isPnut:
    	cDict['calculations']['permutation'] += "\t//permutations\n"
    	cDict['calculations']['permutation'] += "\tdouble* temp = (*xn);\n"
    	cDict['calculations']['permutation'] += "\t(*xn) = (*xnp);\n"
    	cDict['calculations']['permutation'] += "\t(*xnp) = temp;\n"

    cDict['calculations']['return'] = u""
    cDict['calculations']['return'] += "\treturn y;"
    
    cRender = cTemplate.render(**cDict)
    
    print(cRender)

    if fileName is None:
    	fileName = funcName + '.c'
    elif not(fileName.endswith('.c')):
        fileName = fileName + ".c"
    
    with open(fileName, 'w') as outFile:
        outFile.write(cRender)
    
    	