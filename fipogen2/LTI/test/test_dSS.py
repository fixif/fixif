#coding=utf8
# This file contains tests for the dSS functions & class

import unittest
from random import randint
from numpy import array, zeros, absolute,eye, isnan, logical_and
from numpy import matrix as mat
from numpy.linalg import norm
from numpy.testing import assert_allclose
from numpy.random import seed
from sys import exc_info		# to keep trace of trace stack

from LTI.dSS import dSS
from LTI.random_dSS import random_dSS
#from __builtin__ import None


def my_assert_relativeclose( msgH, actual, desired, rtol, strActual, strDesired, strMethod):
	"""
	Params:
		msgH: messageHandler : list of messages produced when an AssertionError occurs (plus the last AssertionError itself)
	
	"""
	try:
		assert_allclose( actual, desired, rtol=rtol)
	except AssertionError as e:
		if msgH:
			del msgH[-1]	# delete last element (last AssertionError)
		msgH.append( """-------------------------------------------
Test with %s
%s = %s
%s = %s
-------------------------------------------""" % (strMethod, strActual, repr(actual), strDesired, repr(desired)) )
		msgH.append(str(e))
		msgH.append(exc_info())	# add the AssertionError itself at the end of the list

msgH = []	# message handler (list of AssertionError messages)

class test_dSS( unittest.TestCase):


	"""
	Test class for dSS class
	"""

	# test non consistency of matrixes  
	def test_construction(self):
		self.assertRaises( ValueError, dSS, [[1,2], [3,4], [5,6]], 1, 2, 3 )
		self.assertRaises( ValueError, dSS, [[1,2], [3,4]], 1, 2, 3)
		self.assertRaises( ValueError, dSS, [[1,2], [3,4]], [1,2], 2, 3 )
		self.assertRaises( ValueError, dSS, [[1,2], [3,4]], [1,2], [[1,2],[1,2]], 3 )	

	
	def test_Gramians(self):
	
		relative_tolerance_linalg  = 10**-5
		relative_tolerance_slycot1 = 10**-5
		nloc = 0	# test number

		for i in range(50):
			nloc +=1
			n = randint(2,40)
			p = randint(2,15)
			q = randint(2,15) 
			S = random_dSS(n,p,q)
	  
			# test with 'linalg' method
			S._W_method = 'linalg'
			my_assert_relativeclose( msgH,
								 array(S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose()), 
								 array(S.Wc), 
								 rtol=relative_tolerance_linalg,
								 strActual= "A*Wc*A' + B*B'",
								 strDesired = 'Wc',
								 strMethod = 'linalg (test #%d)'%nloc )
			my_assert_relativeclose( msgH,
								array(S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C), 
								array(S.Wo), 
								rtol=relative_tolerance_linalg,
								strActual= "A'*Wo*A + C'*C",
								strDesired = 'Wo',
								strMethod = 'linalg (test #%d)'%nloc )

			# JoK : We have to explicitely remove Wo and Wc from S so that those are calculated again
			S._Wo = None
			S._Wc = None
			# test for 'slycot1' method
			# with slycot we expect a 8-digit accuracy		
			S._W_method = 'slycot1'	  
			my_assert_relativeclose( msgH,
								array(S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose()), 
								array(S.Wc), 
								rtol=relative_tolerance_slycot1,
								strActual= "A*Wc*A' + B*B'",
								strDesired = 'Wc',
								strMethod = 'slycot1 (test #%d)'%nloc )

			my_assert_relativeclose( msgH,
								array(S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C), 
								array(S.Wo),
								rtol=relative_tolerance_slycot1,
								strActual= "A'*Wo*A + C'*C",
								strDesired = 'Wo',
								strMethod = 'slycot1 (test #%d)'%nloc )
		
		if msgH:
			print '\n'.join(msgH[:-1])
			#raise AssertionError from msgH[-1]
			raise msgH[-1][0], msgH[-1][1], msgH[-1][2]

	def test_random(self):
	
		for i in range(50):
			n = randint(2,20)
			p = randint(2,15)
			q = randint(2,15)  
				
			S = random_dSS(n,p,q)
			self.assertEqual(S.n,n)
			self.assertEqual(S.p,p)
			self.assertEqual(S.q,q)
			self.assertEqual(S.A.shape, (n,n))
			self.assertEqual(S.B.shape, (n,p))
			self.assertEqual(S.C.shape, (q,n))
			self.assertEqual(S.D.shape, (q,p))
  
  
  	def test_wcpg(self):			
  			
  		def calc_wcpg_approx(S, nit):
  			
  			w = mat(zeros((S.q,S.p)))
  			res = mat(zeros((S.q,S.p)))
  			powerA = mat(eye(S.n,S.n))
  			
  			for i in range(0, nit):
					#res += numpy.absolute(self._C * matrix_power(A, i) * B)

				res += absolute(S.C * powerA * S.B)
				powerA = powerA*S.A
  			
  			w = res + absolute(S.D)
  			
#   			try:
# 		  		for i in range(1, nit):
# 					#res += numpy.absolute(self._C * matrix_power(A, i) * B)
# 					res += absolute(S.C * S.A**i * S.B)
# 			except:
# 				raise ValueError, 'Impossible to compute WCPG at rank i = ' + str(i) + "\n"
# 	 		else:
# 				 w = res + absolute(S.D)

	 		return w
		 	
		nit = 1000
  		rel_tol_wcpg = 10**-5
  		nloc = 0
  		
  		seed(1)
  		
  		for i in range(50):

			nloc +=1
			n = randint(2,5)
			p = randint(2,5)
			q = randint(2,5) 
			S = random_dSS(n,p,q)

			print "NaN check : indian food is not good for you ! \n"
			# Python overreacts on this when mixed with test (if), so let's decouple
			a = isnan(S.A).any()
			b = isnan(S.B).any()
			c = isnan(S.C).any()
			d = isnan(S.D).any()
			
			if (a): print "A :" + str(sum(isnan(S.A))) + " NaN inside, python side"
			if (b): print "B :" + str(sum(isnan(S.B))) + " NaN inside, python side"
			if (c): print "C :" + str(sum(isnan(S.C))) + " NaN inside, python side"
			if (d): print "D :" + str(sum(isnan(S.D))) + " NaN inside, python side"

			wcpg = calc_wcpg_approx(S, nit)
			S.WCPG
			
			print "=== WCPG approx ==="
			print str(wcpg)
 			print "=== A ==="			
 			print S.A
 			print "=== B ==="			
 			print S.B
 			print "=== C ==="			
 			print S.C
 			print "=== D ==="			
 			print S.D
			print "=== WCPG dprec  ==="
			print str(S.WCPG)
			
			my_assert_relativeclose( msgH,
									array(S.WCPG),
									array(wcpg),
									rtol = rel_tol_wcpg,
									strActual = "WCPG dprec",
									strDesired = "WCPG approx",
									strMethod ="compare methods")

#if __name__ == '__main__':
#  sys.path.insert(0, os.path.abspath('./../../'))
#  unittest.main()
