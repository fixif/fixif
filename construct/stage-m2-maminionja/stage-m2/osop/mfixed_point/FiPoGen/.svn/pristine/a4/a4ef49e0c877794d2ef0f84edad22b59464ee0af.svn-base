# -*- coding: utf-8 -*-
from copy import deepcopy
from copy import copy
from string import Template
from FPF import FPF
from Error import Error
from math import log, ceil, floor
import os.path
import string

from Adder import Adder
from Constant import Constant
from Variable import Variable	
	
	
class Multiplier(object):
	"""Classe pour les multiplieurs"""

	#----------------------------------------------------------------------
	def __init__(self,cst_val,wl_cst, var_inter, var_name, mult_wl, index, signed=True,RndOff = None):
		self._name = "Mult_"+var_name
		
		# Tree arguments
		self._result = None #father
		self._index = index
		self._label = 1
		
		# Constant
		self._cst_bs = Constant(cst_val, wl_cst, signed=signed)
		self._cst = Constant(cst_val, wl_cst, signed=signed)	
		
		# Variable
		self._var = var_inter
		self._var_name = var_name
		
		# Shift and Noise
		self._wl = mult_wl
		self._rshift_cst = 0
		self._local_error = Error()
		self._RndOff = RndOff or "RAM"
		
		# Result
		self._var_result = None
		self.Calc_var_result()
		
	@property
	def constant(self):	
		return self._cst
	
	@property
	def variable(self):
		return self._var
	
	@property
	def result(self):
		return self._var_result
	
	@property
	def _left(self):
		return self
		
	def __ge__(self,other):
		"""override of the greater or equal operation"""
		#print self._left._index, other._left._index
		return self._left._index >= other._left._index
	
	def __repr__(self):
		return "%s, lsb = %d"%(self._name, self.result.FPF.lsb)
	
	def cmp_lsb(self, other):
		mi = self.result.FPF.lsb
		mj = other.result.FPF.lsb
		return mi - mj
	
	def Calc_var_result(self):
		self._var_result = self._var.mult(self._cst , self._wl)[0]
		self._rshift_cst = -self._cst.FPF.lsb + self._cst_bs.FPF.lsb
		
	def add(self,other, options):
		"""Merge two Multipliers with an Adder"""
		if isinstance(other,Adder):
			print "Grosse panique"
			pass
		#addition d'un multiplier et d'un multiplier
		adder = Adder()
		adder._operands=[self,other]
		adder._left = self
		adder._top = True
		adder.Calc_var_result(options)
		return adder
	
	def Code_fixe(self,osop):
		return "(%d * %s)"%(self._cst.integer, self._var_name)
	
	
	### Code functions ###
	
	
	def Tikz(self,osop,tab):
		code = "\t"*tab+"child{[sibling distance=1cm]\n"
		rshift_mult = self._result._rshift[self._result._operands.index(self)]
		if rshift_mult != 0:
			tab += 1
			code += "\t"*tab+"node(D"+repr(self).translate(None,string.punctuation)+") [dec%d] {$%s"%(rshift_mult >0 and 1 or 2,rshift_mult >0 and ">>" or "<<")+repr(abs(rshift_mult))+" $}\n"
			code += "\t"*tab+"child{\n"
		code += "\t"*(tab+1)+"node("+repr(self).translate(None,string.punctuation)+") [mult] {$\\times$}\n"
		code += "\t"*(tab+1)+"child{\n"
		if self._rshift_cst != 0:
			tab += 1
			code += "\t"*(tab+1)+"node(DC"+repr(self).translate(None,string.punctuation)+") [dec] {$>> "+repr(self._rshift_cst)+" $}\n"
			code += "\t"*(tab+1)+"child{\n"
		#on affiche la valeur virgule fixe ou la valeur reelle (quand tous les FPF ne sont definis)
		if self._cst.FPF.wl:
			code += "\t"*(tab+2)+"node(Cst%d) [cst] {%d}\n"%(self._index,self._cst.integer)
			code += "\t"*(tab+1)+"edge from parent node[fpf, left] {%s}\n"%self._cst_bs.FPF+"\t"*(tab+1)+"}\n"
		else:
			code += "\t"*(tab+2)+"node(Cst%d) [cst] {%f}\n"%(self._index,self._cst_val)
			code += "\t"*(tab+1)+"edge from parent node[fpf, left] {%s}\n"%self._cst_bs.FPF+"\t"*(tab+1)+"}\n"
			#code += "node(Cst%d) [cst] {$c_%d$}\n }"%(self._index,self._index)

		if self._rshift_cst != 0:
			code += "\t"*tab+"edge from parent node[fpf, left] {%s}\n"%self._cst.FPF
			code += "\t"*tab+"}\n"
			tab -= 1
		code += "\t"*(tab+1)+"child{\n"+"\t"*(tab+2)+"node(Var%d) [var] {$%s$}\n"%(self._index,self._var_name)
		code += "\t"*(tab+1)+"edge from parent node[fpf, right] {%s}\n"%self._var.FPF+"\t"*(tab+1)+"}\n"
		if rshift_mult != 0:
			if (self == self._result._operands[0]) and (len(self._result._operands) == 2) :
				code += "\t"*(tab+1)+"edge from parent node[fpf, left] {%s}\n"%self._var_result.FPF
			else:
				code += "\t"*(tab+1)+"edge from parent node[fpf, right] {%s}\n"%self._var_result.FPF
			code += "\t"*tab+"}\n"
			tab -= 1
		if (self == self._result._operands[0]) and (len(self._result._operands) == 2) :
			code += "\t"*(tab+1)+"edge from parent node[fpf, left,sloped,above] {%s}\n"%self._result._var_op[0].FPF
		else:
			code += "\t"*(tab+1)+"edge from parent node[fpf, right,sloped,above] {%s}\n"%self._result._var_op[1].FPF
		code += "\t"*tab+"}\n"
		return code, 1.5
	
	
	def Code_C(self,i,n):
		st_fix = "\n\t//Computation of c%d*x%d in register r%d\n"%(self._index, self._index, i)
		st_float = ""
		st_sample = ""
		#Déclaration de la constante
		st_fix += "\tac_fixed<%d,%d,true,AC_TRN> c%d = %.53g;\n"%(self._cst_bs.FPF.wl,self._cst_bs.FPF.msb+1,self._index,self._cst_bs.approx)
		st_float += "\tfloat L%d = tab[%d]*pow(2,%d);\n"%(self._index,self._index,self._var.lsb)
		#La variable ac_fixed x prend la valeur de la variable float
		st_fix += "\tac_fixed<%d,%d,true,AC_TRN> x%d = L%d;\n"%(self._var.FPF.wl,self._var.FPF.msb+1,self._index,self._index)
		#Calcul du produit
		st_fix += "\tac_fixed<%d,%d,true,AC_TRN> r%d = c%d*x%d;\n\n"%(self._var_result.FPF.wl,self._var_result.FPF.msb+1,i,self._index,self._index)
		#st_fix += '\tcout<<"r%d = "<< c%d << " * "<< x%d <<" = "<<r%d<<endl;\n\n'%(i,self._index,self._index,i)
		return st_fix, st_float, st_sample, i+1,n+1
	
	def Code_C_int(self,R):
		i = 0
		while R[i]: i=i+1
		# i est l'indice du premier registre non utilisé
		st_fix = "\n\t//Computation of c%d*x%d in register r%d\n"%(self._index, self._index, i)
		st_float = ""
		st_fix += "\tc = %d;\n"%(self._cst_bs.integer) #Déclaration de la constante 
		#st_float += "\tfloat L%d = tab[%d];\n"%(self._index , self._index) #Déclaration de la variable et lecture de la valeur dans le fichier
		# d'échantillons
		#st_fix += "\tx = L%d;\n"%(self._index)# la variable globale x prend la valeur de la variable
		st_fix += "\tr%d = c*x%d;\n"%(i,self._index)
		#st_fix += '\tcout<<"r%d = "<< c << " * "<< x <<" = "<<r%d<<endl;\n\n'%(i,i)
		R[i] = 1 #le registre i est désormais utilisé
		return st_fix, st_float, R, i
	
	def Code_reel(self, L = None,i = None):
		if L:
			return self._cst_bs.value * L[i], str(self._cst_bs.value)+" * "+str(L[i]), i+1
		else:
			return "%.53g * x%d*pow(2,%d)"%(self._cst_bs.approx,self._index,self._var.lsb)	