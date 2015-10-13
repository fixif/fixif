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

from SIF import *
from numpy import matrix as mat
from scipy.signal.filter_design import butter

from func_aux.MtlbHelper import MtlbHelper

from Structures import *

from scipy.signal import tf2ss

from numpy import array, squeeze, reshape

import sys, os

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
        SIF(myJtoS)
        
        # test wrong sizes are caught
        myJtoS = myK, myL, myJ, myM, myN, myP, myQ, myR, myS
        
        self.assertRaises(ValueError, SIF, myJtoS)
        # TODO add test for all other cases
        
class test_SIF_mtlb(unittest.TestCase):

    def setUp(self):
        
		self.engMtlb = MtlbHelper()
		# add matlab script dir
		sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))
    
    def gen_numDen(self, TF='butter', opt_num=0):
        
        # Option #1 generate num and den from matlab butter
        
        tmp_vars = {}

        varz = ['num','den']
        
        if TF is 'butter':
            if opt_num is 0:
                
                cmd  = '[num, den] = butter(4, 0.05) ;'
                self.engMtlb.pushCmdGetVar(cmd, varz, tmp_vars)
        
        return tmp_vars
    
    def mytest_tf2ss(self, dict_numden):
        
        """
        Test numpy tf2ss routine (example for other tests involving FWRtoolbox)
        """
        
        num = dict_numden['num']
        den = dict_numden['den']
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)

        #print(self.engMtlb.eng.who())

        # create TF matlab obj from num and den
        mtlb_cmd_stack  = 'H = tf(num,den,1); \n'
        
        # create Aq, Bq, Cq, Dq in Matlab workspace
        mtlb_cmd_stack += '[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1}); \n'

        varz = ['Aq', 'Bq', 'Cq', 'Dq']
        
        tmp_vars['Aq'], tmp_vars['Bq'], tmp_vars['Cq'], tmp_vars['Dq'] = \
          tf2ss(squeeze(array(num)), squeeze(array(den)))
        
        for key in tmp_vars.keys():
            if tmp_vars[key].shape == (1,): # does not work with "is" ???
                tmp_vars[key] = tmp_vars[key].reshape(1,1)
            
        self.engMtlb.compare(mtlb_cmd_stack, varz, tmp_vars, decim = 10)
        
        self.engMtlb.cleanenv() # be nice with next test
        
    # test all Structures starting from most simple ones
    
    def mytest_DFI(self):
    	
        pass
    	
    def mytest_DFII(self):
        
        pass
       
    def mytest_rhoDFIIt(self):
    	
    	pass
    
    def mytest_modalDelta(self):
    	
    	pass
        
    def runTest(self):
        
        # test tf2ss on all transfer functions
        
        list_TF = {'butter':1}
        
        for TF in list_TF.keys():
            for i in range(0,list_TF[TF]):
                
                self.mytest_tf2ss(self.gen_numDen(TF, i))
