# -*- coding: utf-8 -*-
import re

reobj_q = re.compile("^([su]?)Q([+-]?[0-9]+)\.([+-]?[0-9]+)$")		# Q notation
reobj_ch = re.compile("^([su]?)<([+-]?[0-9]+),([+-]?[0-9]+)>$")	# Chevron notation < >

class FPR(object):
	"""Classe pour la Fixed Point Representation"""

	#----------------------------------------------------------------------
	def __init__(self,beta = None, alpha = None, gamma = None, signed = True, format = None):
		"""Constructor for a FPR object
		can be constructed from beta, alpha and/or gamma, BUT ALSO from a string (format)
		"""
		# check if FPR should be construct from format string
		if format:
			fmt_q = reobj_q.match(format)		# check Q notation
			fmt_ch = reobj_ch.match(format)	# check Chevron notation
			if fmt_q :
				signed, alpha,gamma = fmt_q.groups()
				signed = signed != 'u'
				alpha = int(alpha)
				gamma = int(gamma)
				beta = alpha + gamma
			elif fmt_ch:
				signed, alpha,gamma = fmt_ch.groups()
				signed = signed != 'u'
				alpha = int(alpha) + 1				# this  +1 is important !!
				gamma = -int(gamma)
				beta = alpha + gamma
			else:
				raise(ValueError,"Wrong format")

		# check if beta/alpha/gamma are coherent
		if beta< (2 if	signed else 1):
			raise(ValueError,"Wrong format")
		
		#If beta, alpha and gamma are all given, but with beta different than alpha +gamma, then error
		elif beta is not None and alpha is not None and gamma is not None:
			if beta != alpha + gamma:
				raise(ValueError,"alpha, beta and gamma should satisfy beta = alpha + gamma")
		
		# if only beta and alpha are given, compute gamma
		elif beta is not None and alpha is not None and gamma is None:
			gamma = beta - alpha
			
		# if only beta and gamma are given, compute alpha
		elif beta is not None and gamma is not None and alpha is None:
			alpha = beta - gamma
			
		# if only alpha and gamma are given, compute beta
		elif beta is None and gamma is not None and  alpha is not None:
			beta = alpha + gamma
		
		# store the values
		self._beta = beta
		self._alpha = alpha
		self._gamma = gamma
		self._signed = signed		#Warning !! Signed is not yet used in (beta,alpha,gamma) construction
		
		
	@property
	def alpha(self):
		return self._alpha
	@alpha.setter
	def alpha(self,a):
		if self._beta != None:
			if not self._alpha:
			#Si beta a une valeur, et alpha n'en a pas, alors alpha prend la valeur en parametre et et on calcule gamma
				self._alpha = a
				self._gamma = self._beta-a
			else:
			#Si beta et alpha ont deja une valeur on ne peut pas modifier alpha
				raise(ValueError,"alpha cannot be changed")
		else:
		#Si beta n'a pas de valeur on ne peut pas affecter de valeur a alpha
			raise(ValueError,"alpha cannot be set when beta is not set")


	@property    
	def gamma(self):
		return self._gamma
	@gamma.setter
	def gamma(self,c):
		if self._beta != None:
			self._gamma = c
			if not self._alpha:
			#Si beta a une valeur, et alpha n'en a pas, alors on calcule alpha a partir de beta et gamma
				self._alpha = self._beta - self._gamma
			else:
			#Si beta et alpha ont une valeur alors on modifie beta
				self._beta = self._alpha + self._gamma
		else:
			#Si beta n'a pas de valeur on ne peut pas affecter de valeur a gamma
			raise(ValueError,"gamma cannot be set when beta is not set")

	@property
	def beta(self):
		return self._beta

	@beta.setter
	def beta(self,b):
		self._beta = b
		if self._alpha != None:
		#Si alpha a une valeur alors on met a jour gamma a partir du nouveau beta
			self._gamma = b-self._alpha

	def bag(self):
		"""Return the tuple (beta,alpha,gamma)"""
		return (self.beta,self.alpha,self.gamma)

	def shift(self,c):
		"""Right shift of c bits and decrease alpha without changing beta."""
		#warning si le shift est negatif
		self._alpha += c
		self._gamma -= c
		
	def copy(self):
		return FPR(beta=self._beta, alpha=self._alpha, signed=self._signed)
		
	def __str__(self):
		return self.Chevronnotation()
	
	def __repr__(self):
		return "FPR ="+self.Qnotation()

	def Qnotation(self):
		"""return the Q	notation (ex. "Q5.6") """
		if (self._alpha != None) and (self._beta != None) and (self._gamma != None):
			return "%sQ%d.%d"%('u'*(not self._signed),self.alpha,self.gamma)
		else:
			return "undefined FPR"

	
	def Chevronnotation(self):
		"""return the Chevron	notation (ex. "(5,-6)") """
		if (self._alpha != None) and (self._beta != None) and (self._gamma != None):
			return "%s(%d,%d)" % ('u'*(not self._signed), self._alpha-1,-self._gamma)	
		else:
			return "undefined FPR"
	
	
	def approx(self,r):
		"""Convertit le reel r dans ce FPR"""
		return 2**(-self.gamma)*round(r*2**self.gamma)
	
	
	def LaTeX(self, y_origin=0, binary_point=False,FPR_label='none', bag_label=False, power2=False, notation='bag', **other_params):
		"""generate the LaTeX version of the FPR -> only a grid, of 3 different type of square ('sign', 'alphas' and 'gammas')
		each square is 1x1 square, and the point (0,y_origin) correspond to the binary-point position
		the caller has to define the style of each type ('sign', 'alphas' and 'gammas') with "\tikzstyle{xxx}=[...]"
		Options:
		- binary_point: True or False (plot the binary-point)
		- FPR_label: 'none', 'above', 'below', 'right' or 'left' (display the FPR with Q notation)
		- bag_label: True or False (display the arrows with alpha, gamma and beta)
		- power2: True or False (display the power of 2)
		- notation: 'numeric' (display numerical values), 'bag' (display alpha, beta, gamma), 'w' (display weights w_MSB and w_LSB)
		"""
		# prepare labels (numerical, alpha/beta/gamma or weights)
		fpr_str = self.Chevronnotation() if notation=='w' else self.Qnotation()
		str_alpha = '\\alpha' if self._alpha>0 else '-\\alpha'
		str_gamma = '\\gamma' if self._gamma>0 else '-\\gamma'
		str_beta = '\\beta'
		if notation=='numeric':
			str_alpha = str_alpha+'='+str(abs(self._alpha))
			str_gamma = str_gamma+'='+str(abs(self._gamma))
			str_beta = str_beta+'='+str(self._beta)
			str_alpha_m1 = self._alpha-1
			str_msb = self._alpha-2 if self._signed else self._alpha-1
			str_lsb = -self.gamma
		elif notation=='bag':
			str_alpha_m1 = '\\alpha-1'
			str_msb = '\\alpha-2' if self._signed else '\\alpha-1'
			str_lsb = '-\\gamma'
		else:
			str_alpha_m1 = 'M'
			str_msb = 'M-1' if self._signed else 'M'
			str_lsb = 'L'
		
			
		#comment
		st = "\t%FPR="+self.Qnotation()+"\n"
		# one rectangle per bit
		firstSigned = self._signed		# True if self is signed. Still True if we do not enter in the 1st loop (when alpha<0)
		for a in range( -self._alpha, min(0,self._gamma) ):
			st += "\t\\draw (%f,%f) rectangle ++(1,1) [%s] node[midway] {%s};\n"%(a,y_origin, 'sign' if firstSigned else 'alphas', 's' if firstSigned else '')
			firstSigned = False
		for g in range( -min(0,self._alpha), self._gamma ) :
			st += "\t\\draw (%f,%f) rectangle ++(1,1) [%s] node[midway] {%s};\n"%(g,y_origin, 'sign' if firstSigned else 'gammas', 's' if firstSigned else '')
			firstSigned=False
		#	binary-point position
		if binary_point:
			st +='\t\\draw[black,fill] (0,0) circle [radius=0.1cm];\n'
		# label format
		if FPR_label=='above':
			st +='\t\\draw (%f,%f) node[above] {$%s$};\n'%((self._gamma-self._alpha)/2, y_origin+1,fpr_str)
		elif FPR_label=='below':
			st += '\t\\draw (%f,%f) node[below] {$%s$};\n'%((self._gamma-self._alpha)/2, y_origin,fpr_str)
		elif FPR_label=='right':
			st += '\t\\draw (%f,%f) node[right] {$%s$};\n'%(self._gamma,y_origin+0.5,fpr_str)
		elif FPR_label=='left':
			st += '\t\\draw (%f,%f) node[left] {$%s$};\n'%(-self._alpha,y_origin+0.5,fpr_str)
		# bag_label
		if bag_label:
			if self._alpha!=0:
				y_alpha = y_origin - (0.35 if self._alpha>0 else 0.70)
				st += '\t\\draw[|<->|] (%f,%f) -- (0,%f) node[midway,fill=white!30] {$%s$};\n'%( -self._alpha, y_alpha, y_alpha, str_alpha)
			if self._gamma!=0:
				# gamma: from -min(0,self._alpha) to  self._gamma
				y_gamma = y_origin - (0.35 if self._gamma>0 else 0.70)
				st += '\t\\draw[|<->|] (0,%f) -- (%f,%f) node[midway,fill=white!30] {$%s$};\n'%(  y_gamma, self._gamma, y_gamma, str_gamma)
			st += '\t\\draw[|<->|] (%f,%f) -- (%f,%f) node[midway,fill=white!30] {$%s$};\n'%( -self._alpha, y_origin-0.7, self._gamma, y_origin-0.7, str_beta)
		# display the power of 2
		if power2:
			# sign bit : -2^(alpha-1)
			if self._signed:
				st += "\t\\draw (%f,%f) node[above] {$-2^{%s}$};\n"%(-self.alpha+0.5, y_origin+1, str_alpha_m1)
			# 2^0
			if self._alpha-2>0>-self._gamma:
				st += "\t\\draw (-0.5,%f) node[above] {$2^0$};\n"%(y_origin+1)
			# 2^0
			if self._alpha-2>-1>-self._gamma:
				st += "\t\\draw (0.5,%f) node[above] {$2^{-1}$};\n"%(y_origin+1)
			# most signifiant bit (excluding sign bit) : 2^(alpha-2) or 2^(alpha-1)
			st += "\t\\draw (%f,%f) node[above] {$2^{%s}$};\n"%(-(self._alpha if self._signed else self._alpha+1)+1.5, y_origin+1 , str_msb)	
			# less signifiant bit (excluding sign bit) : 2^(famma-1)
			st += "\t\\draw (%f,%f) node[above] {$2^{%s}$};\n"%(self._gamma-0.5, y_origin+1, str_lsb)
		return st
		
