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

from func_aux import mtlb_helper

from Structures import *

from scipy.signal import tf2ss

from numpy import array, squeeze, reshape

# use matlab from python
# note : this should be transient and removed when published on internet
# http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
# installed it in user folder with user
# cd "matlabroot\extern\engines\python"
# python setup.py install --user

import matlab.engine

import sys, os
# add matlab dir scripts
sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))

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
        
    def test_matlab_compliance(self):
        
        """
        All subfunctions test for compliance of given results with matlab regarding :
        - conversion of other forms to SIF
        - ...
        """
        
        eng = matlab.engine.start_matlab()
    
        # test tf2ss numpy code
        mtlb_vars  = {}
        local_vars = {}
        
        mtlb_cmd_stack = ''
        
        cmd  = '[num, den] = butter(4, 0.05) ;'
        varz = ['num','den']
        
        # store num, den in mtlb_vars
        mtlb_helper.mtlb_pushCmdGetVar(eng, cmd, varz, mtlb_vars)
        
        # stack command to be sent to matlab all at once
        mtlb_cmd_stack += cmd + "\n"
        # create TF matlab obj from num and den
        mtlb_cmd_stack += 'H = tf(num,den,1); \n'
        mtlb_cmd_stack += '[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1}); \n'
        
        local_vars['Aq'], local_vars['Bq'], local_vars['Cq'], local_vars['Dq'] = tf2ss(squeeze(array(mtlb_vars['num'])), squeeze(array(mtlb_vars['den'])))
        local_vars['Dq'] = local_vars['Dq'].reshape(1,1)
            
        varz = ['Aq','Bq','Cq','Dq']
        mtlb_helper.mtlb_compare(eng, mtlb_cmd_stack, varz, local_vars, decim = 10)