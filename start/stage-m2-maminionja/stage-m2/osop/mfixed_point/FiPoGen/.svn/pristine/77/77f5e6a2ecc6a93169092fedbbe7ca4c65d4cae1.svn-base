# -*- coding: utf-8 -*-
import re

reobj_q = re.compile("^([su]?)Q([+-]?[0-9]+)\.([+-]?[0-9]+)$")		# Q notation
reobj_ch = re.compile("^([su]?)<([+-]?[0-9]+),([+-]?[0-9]+)>$")	# Chevron notation < >

class FPF(object):
	"""Classe pour la Fixed Point Format"""

	#----------------------------------------------------------------------
	def __init__(self, wl = None, msb = None, lsb = None, signed = True, format = None):
		"""Constructor for a FPF object
		can be constructed from wordlength (wl), msb and/or lsb, BUT ALSO from a string (format)
		"""
		# check if FPF should be construct from format string
		if format:
			fmt_q = reobj_q.match(format)		# check Q notation
			fmt_ch = reobj_ch.match(format)	# check Chevron notation
			if fmt_q :
				signed, msb,lsb = fmt_q.groups()
				signed = signed != 'u'
				msb = int(msb)-1
				lsb = -int(lsb)
				wl = msb + 1 - lsb
			elif fmt_ch:
				signed, msb,lsb = fmt_ch.groups()
				signed = signed != 'u'
				msb = int(msb)
				lsb = int(lsb)
				wl = msb + 1 - lsb
			else:
				raise(ValueError,"Wrong format")

		# check if wl/msb/lsb are coherent
		if wl< (2 if	signed else 1) and (wl is not None):
			raise(ValueError,"Wrong format")
		
		#If wl, msb and lsb are all given, but with wl different than msb+1-lsb, then error
		elif wl is not None and msb is not None and lsb is not None:
			if wl != msb + 1 - lsb:
				raise(ValueError,"wl, msb and lsb should satisfy wl = msb +1 - lsb")
		
		# if only wl and msb are given, compute lsb
		elif wl is not None and msb is not None and lsb is None:
			lsb = msb + 1 - wl
			
		# if only wl and lsb are given, compute msb
		elif wl is not None and lsb is not None and msb is None:
			msb = wl + lsb -1
			
		# if only msb and lsb are given, compute wl
		elif wl is None and lsb is not None and  msb is not None:
			wl = msb + 1 - lsb
		
		# store the values
		self._wl = wl
		self._msb = msb
		self._lsb = lsb
		self._signed = signed		#Warning !! Signed is not yet used in (wl,msb,lsb) construction
		
	@property
	def msb(self):
		return self._msb
	@msb.setter
	def msb(self,m):
		if self._wl != None:
			if not self._msb:
			#Si wl a une valeur, et msb n'en a pas, alors msb prend la valeur en parametre et on calcule lsb
				self._msb = m
				self._lsb = m + 1 - self._wl
			else:
			#Si wl et msb ont deja une valeur on ne peut pas modifier msb
				raise(ValueError,"msb cannot be changed")
		else:
		#Si wl n'a pas de valeur on ne peut pas affecter de valeur a msb
			raise(ValueError,"msb cannot be set when wl is not set")
		
	@property    
	def lsb(self):
		return self._lsb
	@lsb.setter
	def lsb(self,l):
		if self._wl != None:
			self._lsb = l
			if not self._msb:
			#Si wl a une valeur, et msb n'en a pas, alors on calcule msb a partir de wl et lsb
				self._msb = self._wl + self._lsb - 1
			else:
			#Si wl et msb ont une valeur alors on modifie wl
				self._wl = self._msb + 1 - self._lsb
		else:
			#Si wl n'a pas de valeur on ne peut pas affecter de valeur a lsb
			raise(ValueError,"lsb cannot be set when wl is not set")
	
	@property
	def wl(self):
		return self._wl

	@wl.setter
	def wl(self,w):
		self._wl = w
		if self._msb != None:
		#Si msb a une valeur alors on met a jour lsb a partir du nouveau wl
			self._lsb = self._msb+1-w
			
	def wml(self):
		"""Return the tuple (wl,msb,lsb)"""
		return (self._wl, self._msb, self._lsb)
	
	def shift(self,d):
		"""Right shift of d bits and decrease msb without changing beta."""
		#warning si le shift est negatif
		self._msb += d
		self._lsb += d
		
	def copy(self):
		return FPF(wl=self._wl, msb=self._msb, signed=self._signed)	
	
	def __str__(self):
			return self.Chevronnotation()
		
	def __repr__(self):
		return "FPF ="+self.Qnotation()

	def Qnotation(self):
		"""return the Q	notation (ex. "Q5.6") """
		if (self._msb != None) and (self._wl != None) and (self._lsb != None):
			return "%sQ%d.%d"%('u'*(not self._signed),self._msb+1,-self._lsb)
		else:
			return "undefined FPR"

	
	def Chevronnotation(self):
		"""return the Chevron	notation (ex. "(5,-6)") """
		if (self._msb != None) and (self._wl != None) and (self._lsb != None):
			return "%s(%d,%d)" % ('u'*(not self._signed), self._msb,self._lsb)	
		else:
			return "undefined FPR"
		
	def approx(self,r):
		"""Convertit le reel r dans ce FPF"""
		return 2**(self._lsb)*round(r*2**(-self._lsb))
	
	def LaTeX(self, y_origin=0, binary_point=False,FPF_label='none', bag_label=False, power2=False, notation='w', **other_params):
		"""generate the LaTeX version of the FPF -> only a grid, of 3 different type of square ('sign', 'alphas' and 'gammas')
		each square is 1x1 square, and the point (0,y_origin) correspond to the binary-point position
		the caller has to define the style of each type ('sign', 'alphas' and 'gammas') with "\tikzstyle{xxx}=[...]"
		Options:
		- binary_point: True or False (plot the binary-point)
		- FPF_label: 'none', 'above', 'below', 'right' or 'left' (display the FPF with weight (chevron) notation)
		- bag_label: True or False (display the arrows with alpha, gamma and beta)
		- power2: True or False (display the power of 2)
		- notation: 'numeric' (display numerical values), 'bag' (display alpha, beta, gamma), 'w' (display weights w_MSB and w_LSB)
		"""
		# prepare labels (numerical, alpha/beta/gamma or weights)
		fpf_str = self.Chevronnotation() if notation=='w' else self.Qnotation()
		str_alpha = 'i' if self._msb>0 else '-i' #'\\alpha' if self._msb>0 else '-\\alpha'
		str_gamma = 'f' if self._lsb<0 else '-f' #'\\gamma' if self._lsb<0 else '-\\gamma'
		str_beta = 'w' #'\\beta'
		if notation=='numeric':
			str_alpha = str_alpha+'='+str(abs(self._msb+1))
			str_gamma = str_gamma+'='+str(abs(self._lsb))
			str_beta = str_beta+'='+str(self._wl)
			str_alpha_m1 = self._msb
			str_msb = self._msb-1 if self._signed else self._msb
			str_lsb = self._lsb
		elif notation=='bag':
			str_alpha_m1 = 'i-1'#'\\alpha-1'
			str_msb = 'i-2' if self._signed else 'i-1' #'\\alpha-2' if self._signed else '\\alpha-1'
			str_lsb = '-f'#'-\\gamma'
		else:
			str_alpha_m1 = 'M'
			str_msb = 'M-1' if self._signed else 'M'
			str_lsb = 'L'
		
			
		#comment
		st = "\t%FPF="+self.Qnotation()+"\n"
		# one rectangle per bit
		firstSigned = self._signed		# True if self is signed. Still True if we do not enter in the 1st loop (when alpha<0)
		for m in range( -self._msb-1, min(0,-self._lsb) ):
			st += "\t\\draw (%f,%f) rectangle ++(1,1) [%s] node[midway] {%s};\n"%(m,y_origin, 'sign' if firstSigned else 'MSBs', 's' if firstSigned else '')
			firstSigned = False
		for l in range( -min(0,self._msb), -self._lsb ) : #maybe _msb+1
			st += "\t\\draw (%f,%f) rectangle ++(1,1) [%s] node[midway] {%s};\n"%(l,y_origin, 'sign' if firstSigned else 'LSBs', 's' if firstSigned else '')
			firstSigned=False
		#	binary-point position
		if binary_point:
			st +='\t\\draw[black,fill] (0,0) circle [radius=0.1cm];\n'
		# label format
		if FPF_label=='above':
			st +='\t\\draw (%f,%f) node[above] {$%s$};\n'%((-self._lsb-self._msb-1)/2, y_origin+1,fpf_str)
		elif FPF_label=='below':
			st += '\t\\draw (%f,%f) node[below] {$%s$};\n'%((-self._lsb-self._msb-1)/2, y_origin,fpf_str)
		elif FPF_label=='right':
			st += '\t\\draw (%f,%f) node[right] {$%s$};\n'%(-self._lsb,y_origin+0.5,fpf_str)
		elif FPF_label=='left':
			st += '\t\\draw (%f,%f) node[left] {$%s$};\n'%(-self._msb-1,y_origin+0.5,fpf_str)
		# bag_label
		if bag_label:
			if self._msb+1!=0:
				y_msb = y_origin - (0.35 if self._msb+1>0 else 0.70)
				st += '\t\\draw[|<->|] (%f,%f) -- (0,%f) node[midway,fill=white!30] {$%s$};\n'%( -self._msb-1, y_msb, y_msb, str_alpha)
			if self._lsb!=0:
				# gamma: from -min(0,self._alpha) to  self._gamma
				y_lsb = y_origin - (0.35 if self._lsb<0 else 0.70)
				st += '\t\\draw[|<->|] (0,%f) -- (%f,%f) node[midway,fill=white!30] {$%s$};\n'%(  y_lsb, -self._lsb, y_lsb, str_gamma)
			st += '\t\\draw[|<->|] (%f,%f) -- (%f,%f) node[midway,fill=white!30] {$%s$};\n'%( -self._msb-1, y_origin-0.7, -self._lsb, y_origin-0.7, str_beta)
		# display the power of 2
		if power2:
			# sign bit : -2^(msb)
			if self._signed:
				st += "\t\\draw (%f,%f) node[above] {$-2^{%s}$};\n"%(-self._msb-1+0.5, y_origin+1, str_alpha_m1)
			# 2^0
			if self._msb-1>0>self._lsb:
				st += "\t\\draw (-0.5,%f) node[above] {$2^0$};\n"%(y_origin+1)
			# 2^0
			if self._msb-1>-1>self._lsb:
				st += "\t\\draw (0.5,%f) node[above] {$2^{-1}$};\n"%(y_origin+1)
			# most signifiant bit (excluding sign bit) : 2^(msb-2) or 2^(msb)
			st += "\t\\draw (%f,%f) node[above] {$2^{%s}$};\n"%(-(self._msb+1 if self._signed else self._msb+2)+1.5, y_origin+1 , str_msb)	
			# less signifiant bit (excluding sign bit) : 2^(famma-1)
			st += "\t\\draw (%f,%f) node[above] {$2^{%s}$};\n"%(-self._lsb-0.5, y_origin+1, str_lsb)
		return st