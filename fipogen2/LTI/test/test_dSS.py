#coding=utf8
# This file contains tests for the dSS functions & class

import unittest

from numpy import matrix as mat
from numpy.linalg import norm
from numpy.testing import assert_array_almost_equal
from random import seed

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

    self.assertRaises( ValueError, dSS, mat("1 2; 3 4; 5 6"), mat(1), mat(2), mat(3) )
    self.assertRaises( ValueError, dSS, mat("1 2; 3 4"), mat(1), mat(2), mat(3))
    self.assertRaises( ValueError, dSS, mat("1 2; 3 4"), mat("1;2"), mat(2), mat(3))
    self.assertRaises( ValueError, dSS, mat("1 2; 3 4"), mat("1;2"), mat("1 2; 1 2"), mat(3) )    

  def test_Gramians(self):
    
    seed(1)
    
    for n,p,q in zip( [5,10,35], [1,3, 13], [1, 5, 12]):
      
      S = random_dSS(n,p,q)
      assert_array_almost_equal( S.A*S.Wc*S.A.transpose() + S.B*S.B.transpose(), S.Wc, 8 )
      assert_array_almost_equal( S.A.transpose()*S.Wo*S.A + S.C.transpose()*S.C, S.Wo, 7 )
  
  def test_random(self):
    
    for n,p,q in zip( [5,10,25], [1,3, 13], [1, 5, 12]):

      S = random_dSS(n,p,q)
      self.assertEqual(S.n,n)
      self.assertEqual(S.p,p)
      self.assertEqual(S.q,q)
  

#if __name__ == '__main__':
#  sys.path.insert(0, os.path.abspath('./../../'))
#  unittest.main()
