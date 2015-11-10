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
import algorithmAuxFunc

def algorithmCfloat(R, outFile, funcName):
    
    env = Environment(loader=PackageLoader('SIF','templates'),
     trim_blocks=True,
     lstrip_blocks=True
     )
    
    cTemplate = env.get_template('algorithmC_template.c')
    
    cDict = {}
    
    l,m,n,p = R.size
    
    # Lower triangular part non-null ?
    isPnut = True
        
    if all(tril(R.P,-1) == 0):
        isPnut = False
    
    def _genVarName(baseName, numVar):
        
        varNames = []
        
        if numVar is 1:
            varNames.append(baseName)
        else:
            for i in range(0,numVar):
                varNames.append(baseName + "[" + str(i+1) + "]")
                
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
    	strU = 'u'
    else:
    	strU = _genVarName('u', m)
    	
    #Intermediate variables
    if l == 1:
    	strT = 'T'
    else:
    	strT = 	[ 'T'+str(i) for i in xrange(0,l)]
    	
    # i/o variables, c func
    
    variables = ''
    
    if m == 1:
    	variables += 'double u'
    else:
    	variables += 'double* u'
    	
    variables += ', '
    
    if isPnut:
    	variables += 'double** xn, double** xnp' 
    else:
    	variables += 'double* xn'
    
    cDict['variables']=variables
    
    del(variables)
    	
    # Here is the part that imposes p == 1
    
    cDict['calculations'] = {}
    
    cDict['output'] = '\t'
    cDict['output'] += "double y"
    
    
    # intermediate variables J.T = M.X(k) + N.U(k)
    cDict['calculations']['inter'] = ""
    
    for i in range(0, l):
    	cDict["calculations"]["inter"] += "\t" + "double " + strT[i] + " = " + _scalprodCdouble(c_[R.M[i,:], R.N[i,:], -R.J[i,0:i-2]], strXn + strU + strT[0:i-2]) + ";\n"
    
    
    
    # output Y(k) = R.X(k) + code.U(k) + L.T
    
    cDict['calculations']['output'] = ""
    
    for i in range(0, p):
    	cDict['calculations']['output'] += strY[i] + " = " + _scalprodCdouble()
    
    # states X(k) = P.X(k) + Q.U(k) + K.T
    
    # permutation
    
    filename = funcName + '.c'
    	

    
    
    	