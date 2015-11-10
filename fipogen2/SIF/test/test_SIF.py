#coding=utf8

"""
This file contains tests for the SIF functions & class
"""

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

import unittest
import numpy.testing as npt

from SIF import *
from numpy import matrix as mat

from scipy import signal

from Structures import DFI

from SIF import algorithmLaTeX

class test_SIF(unittest.TestCase):
    
    """
    Test class for SIF class
    """
    
    def test_construction(self):
        
        # l = 2
        # m = 3
        # n = 4
        # p = 5
        
        # (n,n)
        myP = mat([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        # (l,l)
        myJ = mat([[1,2],[3,4]])
        # (n,l)
        myK = mat([[1,2],[3,4],[5,6],[7,8]])
        # (p,l)
        myL = mat([[1,2],[3,4],[5,6],[7,8],[9,10]])
        # (l,n)
        myM = mat([[1,2,3,4],[5,6,7,8]])
        # (l,m)
        myN = mat([[1,2,3],[4,5,6]])
        # (n,m)
        myQ = mat([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        # (p,n)
        myR = mat([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]])
        # (p,m)
        myS = mat([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]])
        
        myJtoS = myJ, myK, myL, myM, myN, myP, myQ, myR, myS
        
        # test correct obj creation
        mySIF = SIF(myJtoS)
        
        # test wrong sizes are caught
        myJtoS = myK, myL, myJ, myM, myN, myP, myQ, myR, myS
        
        self.assertRaises(ValueError, SIF, myJtoS)
        
        #testing getters/properties

        npt.assert_almost_equal(mySIF.J,myJ)
        npt.assert_almost_equal(mySIF.K,myK)
        npt.assert_almost_equal(mySIF.L,myL)
        npt.assert_almost_equal(mySIF.M,myM)
        npt.assert_almost_equal(mySIF.N,myN)
        npt.assert_almost_equal(mySIF.P,myP)
        npt.assert_almost_equal(mySIF.Q,myQ)
        npt.assert_almost_equal(mySIF.R,myR)                                                        
        npt.assert_almost_equal(mySIF.S,myS)

		
    def test_algoLaTeX(self):
    	
    	num, den = signal.butter(4,0.05)
    	
    	mySIF = DFI(num, den)
    	
    	algorithmLaTeX(mySIF, 'testlegend')