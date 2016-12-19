# -*- coding: utf-8 -*-
from FPF import FPF
from Constant import Constant
from math import floor, log

########################################################################
class Variable(object):
	"""Variable class"""

	#----------------------------------------------------------------------
	def __init__(self, value_inf = None, value_sup = None, wl = None, signed = None , fpf = None, integer_inf = None, integer_sup = None):
		"""Construct a Variable object :
		- compute integer values and FPF from value_inf, value_sup, wl, signed
		- compute integer values from value_inf, value_sup, fpf
		- compute nothing from value_inf, value_sup, integer_inf, integer_sup, fpf (wl is fpf.wl)
		- compute all values (real and integer) from fpf


		X = Variable( value_inf=..., value_sup=..., wl=...)
		X = Variable( value_inf=..., value_sup=..., wl=..., signed=...)
		X = Variable( value_inf=..., value_sup=..., fpf=..., integer_inf=..., integer_sup=...)
		X = Variable( fpf=...)


		"""
		# check for good combination of given arguments
		assert (value_inf and value_sup and wl and not (signed or fpf or integer_inf or integer_sup)) \
		    or (value_inf and value_sup and wl and signed != None and not (fpf or integer_inf or integer_sup)) \
		    or (value_inf and value_sup and fpf and integer_inf and integer_sup and not (wl or (signed != None))) \
		    or (fpf and not (value_inf or value_sup or wl or (signed != None) or integer_inf or integer_sup)) \
		    , "Bad combination of arguments"
		
		# check for non-sense values
		if fpf:
			if signed is not None and (signed is not fpf._signed):
				raise( ValueError, "Conflict between Signed and Unsigned !!")	
			if wl and (fpf.wl != wl):
				raise( ValueError, "Conflict between wordlengths !!")
			# and so on
			wl = fpf.wl 
			signed = fpf._signed
			
		if signed == None and fpf == None :
			signed=True
		
		if fpf and not (value_inf or value_sup or integer_inf or integer_sup): # if only a FPF is given		
			self._FPF = fpf
			# compute integer values from fpf
			self._integer_inf = fpf._signed and -2**(fpf.wl-1) or 0
			self._integer_sup = fpf._signed and 2**(fpf.wl-1) - 1 or (2**fpf.wl) - 1
		else: # if not only a FPF is given
			# compute (with Constant class) integer value and FPF of each real value
			c_inf = Constant(value_inf,wl,signed)
			c_sup = Constant(value_sup,wl,signed)
			
			# if msb_inf != msb_sup
			if c_inf.FPF.msb < c_sup.FPF.msb:
				c_inf = Constant(value_inf,wl,signed,c_sup.FPF)
			elif c_inf.FPF.msb > c_sup.FPF.msb:
				c_sup = Constant(value_sup,wl,signed,c_inf.FPF)
				
			# if fpf is given then we select it, else we select the computed FPF from constants
			self._FPF = fpf or c_sup.FPF
			
			# if integer values are given then we select it, else we select the computed integer values from constants
			self._integer_inf = integer_inf or c_inf.integer
			self._integer_sup = integer_sup or c_sup.integer
			
		# if real values are given then we select it, else we compute them from FPF
		self._value_inf = value_inf or self._integer_inf * 2**self.FPF.lsb
		self._value_sup = value_sup or self._integer_sup * 2**self.FPF.lsb
		
	@property
	def integers(self):
		return self._integer_inf, self._integer_sup
	@property
	def FPF(self):
		return self._FPF
	@property
	def approx_values(self):
		return self._integer_inf*2**(self._FPF._lsb),self._integer_sup*2**(self._FPF._lsb)
	
	@property
	def values(self):
		return self._value_inf, self._value_sup
	@values.setter
	def values(self, t):
		assert isinstance(t,tuple) and len(t)==2, "argument for values is not a tuple of two terms"
		self._value_inf = t[0]
		self._value_sup = t[1]
		
	@property
	def lsb(self):
		return self._FPF._lsb
	
	def __repr__(self):
		return "[%g ; %g]"%(self.approx_values[0],self.approx_values[1])
    
	def copy(self):
		v_inf,v_sup = self.values
		N_inf,N_sup = self.integers
		w,m,l = self.FPF.wml()
		fpf = FPF(wl=w , msb=m , signed=self.FPF._signed)
		return Variable(value_inf=v_inf, value_sup=v_sup, fpf=fpf, integer_inf=N_inf, integer_sup=N_sup)
		
	def __rshift__(self, d):
		"""Apply a right shift of d bits onto integer values and FPF of a copy of self."""
		SELF=self.copy()
		SELF._integer_inf >>= d
		SELF._integer_sup >>= d
		wl,m,lsb = SELF.FPF.wml()
		lsb = lsb + d
		SELF._FPF = FPF(wl=wl , lsb=lsb , signed = self.FPF._signed)
		return SELF
	
	def __lshift__(self, d):
		"""Apply a left shift of d bits onto integer values and FPF of a copy of self."""
		SELF=self.copy()
		SELF._integer_inf <<= d
		SELF._integer_sup <<= d
		wl,m,lsb = SELF.FPF.wml()
		lsb = lsb - d
		SELF._FPF = FPF(wl=wl , lsb=lsb , signed = self.FPF._signed)
		return SELF	
    
	def add(self,other,wl_op,msb_final=None):
		# if other is not a Variable object, then return an AssertionError
		assert (isinstance(other,Variable)), "Variable type expected for 'other', not %s"%type(other).__name__
		
		# the function computes sum between two variables where other variable has the smaller lsb,
		# then if it's not the case, addition is re-called with arguments interchanged
		if other.lsb > self.lsb:
			V , var1, var2, rshift= other.add(self,wl_op, msb_final)
			return V, var2, var1, [rshift[1],rshift[0]]
		rshift = [0,0]
		SELF=self.copy()
		OTHER=other.copy()		
		
		# l_add is the lsb of the result, firstly computed as the difference between wl_op and the greater msbs of operands
		msb_add = (msb_final != None) and min(max(SELF.FPF.msb,OTHER.FPF.msb), msb_final) or max(SELF.FPF.msb,OTHER.FPF.msb)
		l_add = msb_add + 1 - wl_op
		
		# 1. Look for left shift
		if SELF.FPF.msb > msb_final:
			rshift[0] += msb_final - SELF.FPF.msb
			SELF = SELF << (SELF.FPF.msb - msb_final)
		if OTHER.FPF.msb > msb_final:
			rshift[1] += msb_final - OTHER.FPF.msb
			OTHER = OTHER << (OTHER.FPF.msb - msb_final)
			
		lo = OTHER.lsb
		ls = SELF.lsb
		
		# 2. Right shift : first operand is aligned on the second one
		# !! WLs are supposed to be equals for SELF and OTHER
		SELF = SELF >> (ls - lo)
		
		# then, if needed, all of the four integers values are aligned onto the result format
		if lo > l_add:
			SELF = SELF >> lo-l_add
			OTHER = OTHER >> lo-l_add
		# 3. Addition
		inf = SELF._integer_inf + OTHER._integer_inf
		sup = SELF._integer_sup + OTHER._integer_sup
		
		# 4. Overflow
		# in case of overflow for inf or sup, sums are recomputed with one bit shifted integers
		if ((inf < -2**(wl_op-1)) or (sup > 2**(wl_op-1)-1)):
			if	(msb_add == msb_final):
				inf = -2**(wl_op-1)
				sup = 2**(wl_op-1)-1
			else:
				SELF = SELF >> 1
				if OTHER != SELF:
					OTHER = OTHER >> 1
				inf = SELF.integers[0] + OTHER.integers[0]
				sup = SELF.integers[1] + OTHER.integers[1]
				l_add -= 1
			
		# the result Variable is created with real values, integer values and computed fpf (from wl_op and l_add)
		V = Variable(value_inf = SELF.values[0]+OTHER.values[0] , value_sup = SELF.values[1]+OTHER.values[1], fpf = FPF(wl = wl_op, lsb = l_add), integer_inf = inf , integer_sup = sup)
		# operands rshifts are computed as the difference between operand lsb and l_add if positive, 0 else
		rshift = [rshift[0]+max(0,-ls+l_add), rshift[1]+max(0,-lo+l_add)]
		return V, SELF, OTHER, rshift
	
	def mult(self,cst,wl_op):
		"""Multiplication between constant and variable on wl_op bits (for the wordlength)"""
		# if cst is not a Constant object, then return an AssertionError
		assert (isinstance(cst,Constant)), "Constant type expected for 'cst', not %s"%type(cst).__name__
		
		# constant shift is computed as the difference between optimal wordlength (wl_cst + wl_var) and operator wordlength (wl_op)
		cst_rshift = cst.FPF.wl + self.FPF.wl - wl_op
		# if cst_rshift < 0 then cst_rshift equals 0 (only positive shift is considered)
		cst_rshift = cst_rshift>0 and cst_rshift or 0

		# compute integer values with a positive (or zero) shift onto the constant
		NX = ((cst.mantissa >> cst_rshift) * self.integers[0] , (cst.mantissa >> cst_rshift) * self.integers[1])
		# if cst.value > 0 then Ninf <-- NX[0], else Ninf <-- NX[1]. In both cases Ninf <-- min(NX)
		Ninf = min(NX)
		# same reasoning for Nsup, Nsup <-- max(NX)
		Nsup = max(NX)
		
		# compute real values
		X = (cst.value * self.values[0], cst.value * self.values[1])
		inf = min(X)
		sup = max(X)
		
		# compute msb
		fpf = FPF(wl=wl_op , msb=cst.FPF.msb + self.FPF.msb + 1)
		V = Variable(value_inf = inf , value_sup = sup, fpf = fpf, integer_inf = Ninf , integer_sup = Nsup)
		return V, cst_rshift