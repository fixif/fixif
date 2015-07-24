#coding=utf8
# This file contains tests for the dSS functions & class

import unittest
from random import randint
from numpy import array
from numpy.linalg import norm
from numpy.testing import assert_array_almost_equal
from numpy.random import seed

#from pyFWR.dSS import dSS, random_dSS

from LTI.dSS import dSS
from LTI.random_dSS import random_dSS


#try:
  #from sage.interfaces.matlab import matlab
#except:
  #pass


#def matlab2mat(varName):
  #"""return a numpy matrix from a matlab variable name"""
  #try:
    #nrows, ncols = map(int, matlab.get( "size(%s)"%varName ).strip().split() )
    #M = mat( matlab.get( "%s(:)"%varName )).reshape( nrows, ncols, order='F')
  #except:
    #M = None
    
  #return M


class test_dSS( unittest.TestCase):
  
  """
  Test class for dSS class
  """

  # test non consistency of matrixes  
  def test_construction(self):

    self.assertRaises( ValueError, dSS, array([[1,2], [3,4], [5,6]]), array(1), array(2), array(3) )
    self.assertRaises( ValueError, dSS, array([[1,2], [3,4]]), array(1), array(2), array(3))
    self.assertRaises( ValueError, dSS, array([[1,2], [3,4]]), array([1,2]), array(2), array(3) )
    self.assertRaises( ValueError, dSS, array([[1,2], [3,4]]), array([1,2]), array([[1,2],[1,2]]), array(3) )    

  def test_Gramians(self):

    is_bugOverride = True # no repr for matrixes in assert_array_almost_equal, numpy 15
    
    def _repr_bug_override():
          
      print '----------'
      print 'test   # ' + str(nloc)       
      print 'method = ' + S._W_method + "\n"
      print 'n      = ' + str(n) + "\n"
      print '--- Wc ---'
      print 'LHS = ' + repr(S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose())
      print 'RHS = ' + repr(S.Wc)
      print '----------'
      print '\n'
      print '--- Wo ---'
      print 'LHS = ' + repr(S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C)
      print 'RHS = ' + repr(S.Wo)
      print '----------'
      print '\n'
    
    ndigit_accuracy_linalg  = 1
    ndigit_accuracy_slycot1 = 7

    nloc = 0
    
    for i in range(50):
        
      n = randint(2,40)
      p = randint(2,15)
      q = randint(2,15) 
      S = random_dSS(n,p,q)
      
      # manually rearm _W_method parameter
      S._W_method = 'linalg'

      nloc += 1
      
      if is_bugOverride:_repr_bug_override()
      
      assert_array_almost_equal( S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose(), S.Wc, ndigit_accuracy_linalg )
      assert_array_almost_equal( S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C, S.Wo, ndigit_accuracy_linalg )

    # test for 'slycot1' method
    # with slycot we expect a 8-digit accuracy
    
    for i in range(50):
        
      n = randint(2,40)
      p = randint(2,15)
      q = randint(2,15) 
      S = random_dSS(n,p,q)
            
      #manually rearm _W_method parameter
      S._W_method = 'slycot1'
      
      nloc += 1
      
      if is_bugOverride:_repr_bug_override()
      
      assert_array_almost_equal( S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose(), S.Wc, ndigit_accuracy_slycot1 )
      assert_array_almost_equal( S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C, S.Wo, ndigit_accuracy_slycot1 )

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
