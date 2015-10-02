# -*- coding: utf-8 -*-
from copy import deepcopy
from copy import copy
from string import Template
from FPF import FPF
from Error import Error
#from Variable import Variable
from math import log, ceil
import os.path
import string

class Adder(object):
	"""Class for adders with intervals"""

	wl_add = 32
	count = 0
	
	#----------------------------------------------------------------------
	def __init__(self, nom=None, operands=None):
		self._name = nom or "Add_%d"%self.__class__.count
		self.__class__.count += 1
		
		# Tree
		self._result = None #father Adder
		self._operands = operands or [] #children Adders or Multiplier
		self._top = False #is root?
		self._left = None #reference to the left deepest Multiplier
		self._label = None #Sethi-Ulman label
		
		# Variable
		self._var_result = None
		self._var_op = [None,None]
		self._rshift = [0,0]
		self._int_err = [0,0]
		#self._wl_opt = None
		# Noise
		self._local_noise = [0,0]
		self._total_noise = [0,0]
		self._local_error = Error()
		self._total_error = Error()
		
	@property
	def result(self):
		return self._var_result	

	def __repr__(self):
			return self._name	

	def __ge__(self,other):
		"""override of the greater or equal operation"""
		#print self._left._index, other._left._index
		return self._left._index >= other._left._index	
		
	def cmp_lsb(self, other):
		mi = self._var_result.FPF.lsb
		mj = other._var_result.FPF.lsb
		return mi - mj
		
	# Probably useless
	#def get_left(self):
		#"""Return the deepest left sub element of self"""
		#if isinstance(self._operands[0],Adder):
			#return self._operands[0].get_left()
		#else: 
			#return self._operands[0]
		
	def height(self):
		"""Retourne la profondeur du noeud self"""
		dg=1
		dd=1
		if isinstance(self._operands[0],Adder):
			dg += self._operands[0].height()
		if isinstance(self._operands[1],Adder):
			dd += self._operands[1].height()
		return max(dg,dd)
	
	def Result_builder(self):
		for op in self._operands:
			if isinstance(op,Adder):
				op.Result_builder()
			op._result = self
			
	def label_builder(self):
		#labelisation par algo de Sethi-Ullman
		if isinstance(self._operands[0],Adder):
			self._operands[0].label_builder()
		if isinstance(self._operands[1],Adder):
			self._operands[1].label_builder()
		if self._operands[0]._label == self._operands[1]._label:
			self._label = self._operands[0]._label + 1
			#nouvelle condition pour coller a notre cas
			if self._operands[0]._label == 1:
				self._label += 1
		else:
			self._label = max(self._operands[0]._label,self._operands[1]._label)
		
	def add(self,other, options):
		"""Ajoute deux sous-oSoP entre eux en créant un Adder père"""
		adder = Adder(operands = [self,other])
		adder._left = self._left
		adder._top = True
		self._top = False
		if isinstance(other,Adder):
			other._top = False
		adder.Calc_var_result(options)
		return adder
		
	def Calc_var_result(self, options):
		alfix, plus, msb_final = options
		# result of operands[i] is a Variable, we copy them into var_op and call this copy var_i
		var_1 = self._operands[0].result
		var_2 = self._operands[1].result
		self._var_result, self._var_op[0], self._var_op[1], self._rshift = var_1.add(var_2,self.__class__.wl_add,msb_final)
		#self._rshift = [-var_1.lsb + self._var_op.lsb , -var_2.lsb + self._var_op.lsb]

		for i, op in enumerate(self._operands):
			#Decalage
			if isinstance(op,Adder) or op._RndOff == "RAM":
				if self._rshift[i] > 0:
					self._local_error += Error(lsb=self._var_result.lsb, rshift=self._rshift[i])
			#elif op._RndOff == "RBM":
				#op._rshift_cst += -op._fpr_res.lsb + self._fpr_res.lsb
				#op._fpr_res = copy(self._fpr_op)
				#op._fpr_cst.shift(op._rshift_cst)
				
		self._total_error += self._local_error
		for op in self._operands:
			if isinstance(op,Adder):
				self._total_error += op._total_error
			else:
				self._total_error += op._local_error
				
				
	### Code functions ###
	
	
	def Tikz(self,osop,tab):
		"""Renvoi un tuple (code,largeur)"""
		code = ""
		op1 = self._operands[0]
		op2 = self._operands[1]
		#appel recursif au tikz des fils
		tikz1, width1 = op1.Tikz(osop, tab+1)
		tikz2, width2 = op2.Tikz(osop, tab+1)
		code += "\t"*tab+"child{[sibling distance=%fcm]\n"%(1*(width1 + width2))
		if self._top:
			rshift_add = osop._rshift_final
		else:
			rshift_add = self._result._rshift[self._result._operands.index(self)]
		if rshift_add != 0 and rshift_add:
			tab += 1
			code += "\t"*tab+"node(D"+repr(self)+") [dec%d] {$%s"%(rshift_add >0 and 1 or 2,rshift_add >0 and ">>" or "<<")+repr(abs(rshift_add))+" $}\n"+"\t"*tab+"child{\n"
		code += "\t"*(tab+1)+"node("+repr(self)+") [adder] {$+$}\n"
		#ajout des codes des tikz fils
		code += tikz1 + tikz2
		if rshift_add != 0 and rshift_add:
			if (not self._top) and (self == self._result._operands[0]) and (len(self._result._operands) == 2) :# 3eme cond ?!
				code += "\t"*(tab+1)+"edge from parent node[fpf, left] {%s}"%self._var_result.FPF
			else:
				code += "\t"*(tab+1)+"edge from parent node[fpf, right] {%s}"%self._var_result.FPF
			code += "\t"*tab+"}\n"
			tab -= 1
		if (not self._top) and (self == self._result._operands[0]) and (len(self._result._operands) == 2) :
			code += "\t"*(tab+1)+"edge from parent node[fpf, left,sloped,above] {%s}\n"%self._result._var_op[0].FPF
		elif (self._top):
			code += "\t"*(tab+1)+"edge from parent node[fpf, right] {%s}\n"%osop._var_final.FPF
		else:
			code += "\t"*(tab+1)+"edge from parent node[fpf, right,sloped,above] {%s}\n"%self._result._var_op[1].FPF
		code += "\t"*tab+"}\n"
		return code, width1 + width2-0.5
	
	def Code_C(self,i,n):
		st_fix = ""
		#Si le label de Sethi-Ullman de l'opérande gauche est plus grand que celui de l'opérange droit, on conserve l'ordre de traitement
		if self._operands[0]._label >= self._operands[1]._label:
			op1 = self._operands[0]
			op2 = self._operands[1]
		#sinon on inverse l'ordre
		else :
			op1 = self._operands[1]
			op2 = self._operands[0]
		st_float = ""
		st_sample = ""
		#On génère le code pour l'opérande 1
		st_fix_temp,st_float_temp, st_sample_temp,i,n = op1.Code_C(i,n)
		i_op1 = i-1
		#on stocke les strings résultant dans des variables
		st_fix += st_fix_temp
		st_float += st_float_temp
		st_sample += st_sample_temp
		#puis le code pour l'opérande 2
		st_fix_temp,st_float_temp, st_sample_temp,i,n = op2.Code_C(i,n)
		i_op2 = i-1
		st_fix += st_fix_temp
		st_float += st_float_temp
		st_sample += st_sample_temp
		#Maintenant on ajoute les deux résutats contenus dans les registres r_i_op1 et r_i_op2, dans r_i
		st_fix += "\n\t//Computation of r%d+r%d in register r%d\n"%(i_op1,i_op2,i)
		st_fix += "\tac_fixed<%d,%d,true,AC_TRN> r%d = r%d + r%d;\n"%(self._var_result.FPF.wl,self._var_result.FPF.msb,i,i_op1,i_op2)
		#if self._top:
			#st_fix += "\tdouble res = r%d.to_double();\n\treturn res;"%(i)
		return st_fix, st_float, st_sample, i+1,n
	
	def Code_C_int(self,R):
		st_fix = ""
		#Si self courant est la racine de l'oSoP, on déclare les variables c et x, ainsi que les registres.
		if self._top: 
			st_fix += "\tint16_t c, x;\n\tint32_t r0"
			for i in range(1,len(R)):
				st_fix += ", r%d"%(i)
			st_fix += ";\n"
		#Si le label de Sethi-Ullman de l'opérande gauche est plus grand que celui de l'opérange droit, on conserve l'ordre de traitement
		if self._operands[0]._label >= self._operands[1]._label:
			op1 = self._operands[0]
			op2 = self._operands[1]
		#sinon on inverse l'ordre
		else :
			op1 = self._operands[1]
			op2 = self._operands[0]
		st_float = ""
		#On génère le code pour l'opérande 1
		st_fix_temp,st_float_temp,R,i_op1 = op1.Code_C_int(R)
		#on stocke les strings résultant dans des variables
		st_fix += st_fix_temp
		st_float += st_float_temp
		#puis le code pour l'opérande 2
		st_fix_temp,st_float_temp,R,i_op2 = op2.Code_C_int(R)
		st_fix += st_fix_temp
		st_float += st_float_temp
		i = 0
		while R[i]: i=i+1
		# i est l'indice du premier registre non utilisé
		#Maintenant on ajoute les deux résutats contenus dans les registres r_i_op1 et r_i_op2, dans r_i,
		#en prenant en compte les décalages si nécessaire.
		st_fix += "\n\t//Computation of r%d+r%d in register r%d\n"%(i_op1, i_op2, i)
		st_fix += "\tr%d= "%(i)
		if self._rshift[self._operands.index(op1)]: st_fix += "( r%d %s %d )"%(i_op1,self._rshift[self._operands.index(op1)] >0 and ">>" or "<<",abs(self._rshift[self._operands.index(op1)]))
		else :st_fix += "r%d"%(i_op1)
		if self._rshift[self._operands.index(op2)]: st_fix += " + ( r%d %s %d );\n"%(i_op2,self._rshift[self._operands.index(op2)]>0 and ">>" or "<<",abs(self._rshift[self._operands.index(op2)]))
		else :st_fix += " + r%d ;\n"%(i_op2)
		#st_fix += '\tcout<<"r%d = "<<r%d<<endl;\n\n'%(i,i)
		#Le i-ème registre est désormais occupé, les deux autres sont libérés.
		R[i] = 1 ; R[i_op1] = None ; R[i_op2] = None
		if self._top:
			#solution de facilité :
			for j in range(len(R)) :
				if j != i:
					R[j] = None
		return st_fix, st_float, R, i
	
	def Code_reel(self, L = None,i = None):
		st = ""
		if self._top:
			st += "r="
		#Si le label de Sethi-Ullman de l'opérande gauche est plus grand que celui de l'opérange droit, on conserve l'ordre de traitement
		if self._operands[0]._label >= self._operands[1]._label:
			op1 = self._operands[0]
			op2 = self._operands[1]
		#sinon on inverse l'ordre
		else :
			op1 = self._operands[1]
			op2 = self._operands[0]
		if L: #Si une liste de valeur est donnée en entrée, on retourne le calcul flottant
			s1,st1,i = op1.Code_reel(L,i)
			s2,st2,i = op2.Code_reel(L,i)
			s = s1+s2
			st = "(%s + %s)"%(st1,st2)
			return s,st,i
		else: #Sinon, on retourne l'expression du calcul flottant
			st1 = op1.Code_reel()
			st2 = op2.Code_reel()
			st = "(%s + %s)"%(st1,st2)
			return st
		
	#def RBM(self,options,total_noise):
		#alfix, plus, alpha_final = options
		#op1 = self._operands[0]
		#op2 = self._operands[1]
		#for i, op in enumerate(self._operands):
			#if isinstance(op,Adder):
				#total_noise = op.RBM(options,total_noise)
			#else:
				#if self._rshift_op[i] > 0:
					#total_noise[0] -= 2**( - self._fpr_res.gamma - 1)* (1 - 2**(2 * - self._rshift_op[i]))
					#total_noise[1] -= (2**( - 2 * self._fpr_res.gamma)/ 12) * (1 - 2**(2 * - self._rshift_op[i]))
					#op._fpr_res = self._fpr_op
					#op._rshift_cst = self._rshift_op[i]
					#op._fpr_cst = copy(op._fpr_cst_bs)
					#op._fpr_cst.shift(op._rshift_cst)
					#total_noise[0] += 2**(- self._fpr_cst - 1) * (1 - 2**(2 * - op._rshift_cst))
					#total_noise[1] += (2**( - 2 * self._fpr_cst)/12) * (1 - 2**(2 * - op._rshift_cst))
		#return total_noise
						
	
	#def Code_fixe(self,osop):
		#L=self._operands
		#st = "("
		#st += L[0].Code_fixe(osop)
		#if self._rshift_op[0] != 0:
			#st += " >> "+repr(self._rshift_op[0])
		#st += " + "
		#st += L[1].Code_fixe(osop)    
		#if self._rshift_op[1] != 0:
			#st += " >> "+repr(self._rshift_op[1])
		#st += ")"
		#if self._top and osop._rshift_final != 0:
			#st += " >> "+repr(osop._rshift_final)
		#return st
	
	
	#def Algo_fix(self,osop,i):
		#op1 = self._operands[0]
		#op2 = self._operands[1]
		#st = ""
		#if isinstance(op1,Multiplier):
			#i_op1 = osop._Multipliers.index(op1)
			#i_op2 = osop._Multipliers.index(op2)
			#st += "Acc%d = "%(i)
			#if (op1._rshift != 0): st += "( "
			#if (op1._rshift_cst != 0): st += "( "
			#st += "%d"%(round(op1._cst_val_app*2**op1._fpr_cst_bs.gamma))
			#if (op1._rshift_cst != 0): st += "  >> %d )"%(op1._rshift_cst)
			#st += " * x%d"%(i_op1)
			#if (op1._rshift != 0): st += " ) >> %d "%(op1._rshift)
			#st += ";\n"
			#st += "Acc%d = "%(i)
			#if (op2._rshift != 0): st += "( "
			#if (op2._rshift_cst != 0): st += "( "
			#st += "%d"%(round(op2._cst_val_app*2**op2._fpr_cst_bs.gamma))
			#if (op2._rshift_cst != 0): st += "  >> %d )"%(op2._rshift_cst)
			#st += " * x%d"%(i_op2)
			#if (op2._rshift != 0): st += " ) >> %d "%(op2._rshift)
			#st += ";\n"
		#else:
			#st += op1.Algo_fix(osop,1)
			#if isinstance(op2,Multiplier):
				#i_op2 = osop._Multipliers.index(op2)
				#st += "Acc%d = "%(i)
				#if (op1._rshift != 0): st += "( "
				#st += "Acc%d"%(i)
				#if (op1._rshift != 0): st += " >> %d )" %(op1._rshift)
				#st += " + "
				#if (op2._rshift != 0): st += "( "
				#if (op2._rshift_cst != 0): st += "( "
				#st += "%d"%(round(op2._cst_val_app*2**op2._fpr_cst_bs.gamma))
				#if (op2._rshift_cst != 0): st += "  >> %d )"%(op2._rshift_cst)
				#st += " * x%d"%(i_op2)
				#if (op2._rshift != 0): st += ") >> %d "%(op2._rshift)
				#st += ";\n"
			#else:
				#st += op2.Algo_fix(osop,2)
				#st += "Acc1 = Acc1"
				#if (op1._rshift != 0): st += " >> %d" %(op1._rshift)
				#st += " + Acc2"
				#if (op2._rshift != 0): st += " >> %d" %(op2._rshift)
				#st += ";\n"
		#if self._top and self._rshift != 0:
			#st += "Acc%d = Acc%d >> %d"%(i,i,self._rshift)
		#return st
	