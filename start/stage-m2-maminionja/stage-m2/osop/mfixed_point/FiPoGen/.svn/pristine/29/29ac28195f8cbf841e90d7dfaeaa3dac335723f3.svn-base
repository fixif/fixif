# -*- coding: utf-8 -*-

from FPF import FPF
from math import log, floor, ceil

class Constant (object):
	
	def __init__(self, value, wl, signed=True, fpf=None):
		"""construct a constant object, from a real value (could be float/double or maybe (todo:) GMP), encoded with wl bits. 
		signed=False if we want to use unsigned fixed-point arithmetic"""
		self._value = value
		
		# check for non-sense values
		if signed==False and value<0:
			raise( ValueError, "Unsigned FPF with negative constant !!")
		if value==0:
			raise( ValueError, "zero cannot be stored in a Constant !!")
		if fpf and (fpf.wl != wl):
			raise( ValueError, "Conflict between wls !!")		
		
		# unsiged case
		if signed==False:
			msb = fpf and fpf.msb or int( floor( log(value, 2))) 
			self._integer = int( round( value * 2**(wl-msb-1)) )
			# check for particular case (when the quantized constant overpass the limit whereas the constant doesN'T)
			if self._integer == 2**wl:	
				# on est dans le cas 127.8 sur 8 bits...
				msb +=1
				#self._integer = int ( round( value * 2**(wl-msb-1)) )
				self._integer = 2**(wl-1)
		
		else:	# signed case
			if fpf :
				# compute msb
				msb = fpf.msb
				# compute N
				self._integer = int( round( value * 2**(wl-msb-1)) )
			else:
				# compute msb
				msb = value>0 and (int( floor( log(abs(value), 2))) +1) or (int(ceil( log(abs(value),2))))
				# compute N
				self._integer = int( round( value * 2**(wl-msb-1)) )
				
				# check for particular case (when the value overpass the limit BUT the quantized value doesN'T, or the opposite)
				if self._integer == 2**(wl - 1):	
					# like 127.8 on 8 bits
					msb +=1
					self._integer = 2**(wl-2)
				elif self._integer == -2**(wl-2) :
					# like -128.1 on 8 bits
					msb -=1
					self._integer = -2**(wl-1)
		
		# associated FPF
		if fpf and ( ( not signed and not (0 <= self._integer < 2**wl) ) \
		or (signed and not (-2**(wl-1) <= self._integer < 2**(wl-1)) ) ):
			raise( ValueError, " given FPF cannot represent value")			
		self._FPF = FPF(wl=wl, msb=msb, signed=signed)
			


	
	@property
	def integer(self):
		return self._integer
	@property
	def FPF(self):
		return self._FPF
	@property
	def value(self):
		return self._value
	@property
	def approx(self):
		"""give the best approximation of the constant with wl bits"""
		return self._integer * 2**(self._FPF._lsb)