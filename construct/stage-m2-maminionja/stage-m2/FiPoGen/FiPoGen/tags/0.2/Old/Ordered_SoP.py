from copy import deepcopy
from copy import copy
from string import Template
from FPR import FPR
from math import log, ceil
import cPickle
import os.path
import pickle
import string

from Adder import *
from Multiplier import *

#################################################################################################
class oSoP(object):
	"""ordered Sum-of-Products class"""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructeur"""
		self._Adders = []
		self._Multipliers = []
		self._Top = None
		#self.str_fix_dec = ""
		#self.str_calc = ""
	
	def Copy(self):
		osop = oSoP()
		for a in self._Adders:
			osop._Adders.append(Adder(a._name, a._fpr_res.beta))
		for m in self._Multipliers:
			osop._Multipliers.append(Multiplier(m._cst_val,m._fpr_cst_bs.beta, FPR(m._fpr_var.beta,m._fpr_var.alpha),  m._var_name, m._fpr_res_bs.beta,m._RndOff))
			
		for idx,a in enumerate(self._Adders):
			osop._Adders[idx].Copy(a,self,osop)
		for idx,m in enumerate(self._Multipliers):
			osop._Multipliers[idx].Copy(m,self,osop)
		if self._Top in self._Adders:
			osop._Top = osop._Adders[self._Adders.index(self._Top)]
		else:
			osop._Top = osop._Multipliers[self._Multipliers.index(self._Top)]
		return osop

	def height(self):
		"""Retourne la profondeur d'osop"""
		return self._Top.height()

	def Calc_FPR_Noise(self, alfix, plus=False):
		if not self._Top._fpr_res_bs.gamma:
			self._Top.Calc_FPR_Noise(self, alfix, plus)  
			self._Top._rshift = max(self._Top._fpr_res_bs.gamma - self._Top._fpr_res.gamma,0)
			if self._Top._rshift > 0:
				pass
				self._Top._local_noise[0] = 2**( - self._Top._fpr_res.gamma - self._Top._rshift - 1)
				self._Top._total_noise[0] += self._Top._local_noise[0]
				self._Top._local_noise[1] = (2**( - 2 * self._Top._fpr_res.gamma)/ 12) * (1 - 2**(2 * -self._Top._rshift))
				self._Top._total_noise[1] += self._Top._local_noise[1]

	def Code(self, TYPE = None):
		self.ReOrder()
		if TYPE == "fix":
			return self._Top.Code_fixe()
		elif TYPE == "real":
			return self._Top.Code_reel()
		elif TYPE == "algo":
			return self._Top.Algo(self,1)
		elif TYPE == "falgo":
			return self._Top.Algo_fix(self,1)
		elif TYPE == "Tikz":
			file_in = open("Tex/code_tmplt.tex", 'r')
			file_out = open("Tex/code.tex", 'w')
			tmplt = Template(file_in.read())
			code, width = self._Top.Tikz(self,0)
			d = dict(TP_code = code)
			file_out.write(tmplt.safe_substitute(d))
			file_in.close()
			file_out.close()
		elif TYPE == "C":
			return "bouge toi le cul c'est pas fait ca encore"
		else:
			return "Faut pas deconner y'en a assez la je crois"

	def ReOrder(self):
		for A in self._Adders:
			if isinstance(A._operands[0],Multiplier) and isinstance(A._operands[1],Adder):
				A._operands.reverse()
				
	def quantized(self):
		L = []
		for M in self._Multipliers:
			v = M._fpr_cst.approx(M._cst_val)
			if v==0:
				print "Warning : Underflow in constant %s"%M
		return [M._fpr_cst.approx(M._cst_val) for M in self._Multipliers ]
