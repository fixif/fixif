#coding=utf8
# This file contains tests for the dSS functions & class

import unittest
from random import randint
from numpy import array
from numpy.linalg import norm
from numpy.testing import assert_allclose
from numpy.random import seed

#from pyFWR.dSS import dSS, random_dSS

from LTI.dSS import dSS
from LTI.random_dSS import random_dSS


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
		msgH.append(e)	# add the AssertionError itself at the end of the list


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
		msgH = []	# message handler (list of AssertionError messages)

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
			raise msgH[-1]

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
  


#if __name__ == '__main__':
#  sys.path.insert(0, os.path.abspath('./../../'))
#  unittest.main()
