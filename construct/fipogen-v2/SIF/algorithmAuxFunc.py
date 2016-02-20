#coding=UTF8

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

"""
This file contains aux functions used by both algorithm-rendering functions (Cfloat and LaTeX)
"""

from numpy import where

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
	0.0978988
		
	str(d,'%.6g')
	"""
		
	tol = 1.e-10
		
	dec_format = 6 # 255
		
	S = ""
		
	(rows,cols) = where(abs(P)>tol)
		
	for i in range(0,rows.size):
		
		pos = rows[i],cols[i]
		vecpos = cols[i]
		
		if abs(P[pos]-1.)<tol:
			S += "+ " + names[vecpos] + "\\\n"
		elif abs(P[pos]+1.)<tol:
			S += "- " + names[vecpos] + "\\\n"
		else:
			S+= "+ " + ("{:."+str(dec_format)+"g}").format(P[pos]) + "*" + names[vecpos] + "\\\n"
		
		if i is (rows.size - 1):
			S += "\n"
		
	S = S[1:-3]
			
	if S == "":
		S += "0"
		
	return S