#coding=UTF8
from macpath import basename

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

import SIF
from jinja2 import Environment, FileSystemLoader, PackageLoader
from numpy import tril, all, eye, zeros, where, abs, matrix


# Found inspiration here
# http://martin-ueding.de/en/latex/computation-results/index.html

def algorithmLaTeX(R, out_file, caption=None):
    
    """
    
    Generate a tex file to use with package algorithm2e to create a LaTex output of algorithm
    
    - `R` is a SIF object
    - `caption` is an additional caption
    - `out_file` is the name of the tex output
    
    """
    
    def _genVarName(baseName, numVar):
        
        varNames = []
        
        if numVar is 1:
            varNames[0]=baseName
        else:
            for i in range(0,numVar):
                varNames[i]=baseName + "_{" + str(i) + "}"
                
        return varNames
    
    def _scalprodCdouble(P, names):
        
        """
        Return the C-code corresponding to a double floating-point scalar product
        (the vector of coefficient 'P' by the vector of variables 'name').
        
        Ex: P(1)*name(1) + P(2)*name(2) + ... + P(n)*name(n)
        
        Syntax:
         S = scalprodCdouble(  P, name)
        
        Parameters:
        
        - P: vector of coefficients used in the scalar product (np.matrix, so 2d)
        - name: name of the variables
        
        Returns string
        
        WARNING
        string conversion of float induces a rounding of the number (was the case in matlab)
        matlab
        d=0.09789879876298743
        num2str(d,'%.6g')
        str(d,'%.6g')
        
        
        """
        
        tol = 1.e-10
        
        dec_format = 6 # 255
        
        S = ""
        
        (rows,cols) = where(abs(P)>tol)
        
        for i in range(0,rows.size):
        
            pos = rows(i),cols(i)
        
            vecpos = max(rows(i),cols(i))
        
            if (abs(P[pos])-1<tol):
                S += names[vecpos]
            elif (abs(P[pos])+1<tol):
                S += "-"+names[vecpos]
            else:
                S+= ("{:."+str(dec_format)+"g}").format(P[pos]) + "*" + names[vecpos]
        
            if i is (rows.size - 1):
                S += "\n + "
            
        if S is "":
            S += "0"
        
        return S
    
    env = Environment(loader=PackageLoader('SIF','templates'),
      block_start_string= '%<',
      block_end_string = '>%',
      variable_start_string = '<<',
      variable_end_string = '>>',
      comment_start_string= '[§',
      comment_end_string = '§]'
      )
    
    texPlate = env.get_template('algorithmLaTeX_template.tex')
    
    l = R.l
    m = R.m
    n = R.n
    p = R.p
    
    texDict = {}
        
    # Lower triangular part non-null ?
    isPnut = True
        
    if all(tril(R.P,-1)) is 0:
        isPnut = False
    
    strTXU = _genVarName('T', l) + _genVarName('Xn', n) + _genVarName('u', m)
    
    if isPnut:
    	strTXY = _genVarName('T', l) + _genVarName('Xnp', n) + _genVarName('y', m)
    else:
    	strTXY = _genVarName('T', l) + _genVarName('Xn', n) + _genVarName('y', m)
    
    #Caption 
    if caption is None:
        caption = "Pseudocode algorithm ..."
        
    texDict["caption"] = caption

    texDict['u'] = {}
    texDict['y'] = {}
    texDict['xn'] = {}
    texDict['T'] = {}
       
    varlist = ['u', 'y', 'xn', 'T']
        
    #Inputs
    texDict['u']['numVar'] = m
    #Outputs
    texDict['y']['numVar'] = p
    #States
    texDict['xn']['numVar'] = n
    #Intermediate variables
    texDict['T']['numVar'] = l

    for name in mylist:
        texDict[name]['varNames'] = _genVarNames(name, texDict[name]['numVar'])

    # Z is a matrix
    Zbis = R.Z + r_[c_[eye(l), zeros(l, n+m)], zeros(n+p, l+n+m)]
    
    # To be removed if matrix property is conserved
    #Zbis = matrix(Zbis)
    
    comp_str = ""
    
    for i in range(1, l+n+p+1):
        
        if i is 1:
            comp_str += "\t\\tcp{\\emph{Intermediate variables}}\n"
        elif (i is l+1) and (n is not 0):
            comp_str += "\t\\tcp{\\emph{States}}\n"
        elif (i is l+n+1):
            comp_str += "\t\\tcp{\\emph{Outputs}}\n"
            
        comp_str += "\t" + "$" + strTXY[i] + "\leftarrow" + _scalprodCdouble(Zbis[i,:],strTXU) + "$\;\n"

    if isPnut:
    	comp_str += " \n\t\\tcp{\\emph{Permutations}}\n"
    	comp_str += "\t$xn \\leftarrow xnp$\;"

    teXContents = texPlate.render(())

    print(texContents)
        
    
        