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
import os

from LTI import *
from SIF import *
from numpy import matrix as mat

from Structures import DFI, State_Space

from func_aux.get_data import get_data
from func_aux.MtlbHelper import MtlbHelper

from scipy import signal


class test_SIF(unittest.TestCase):
    
    """
    Test class for SIF class
    """
    
    def setUp(self):
        
        """
        Setup matlab engine for all matlab comparison tests
        Generate sample data for tests
        """
        
        self.engMtlb = MtlbHelper()
        
        # add matlab script dir
        
        abs_fwr_dir = os.path.join(os.getcwd(),"Structures","test","FWRToolbox","")
        print('==================================================')
        print('Adding the following path to matlab engine : ')
        print(abs_fwr_dir)
        print('==================================================')
        self.engMtlb.eng.addpath(abs_fwr_dir, nargout=0)
        
        self.ndigit = 10
        self.eps = 1.e-8    
    
        self.list_dTF = get_data("TF", "signal", "butter")# + get_data("TF", "random")
        #self.list_dTF = get_data("TF", "random") ,BUG
        print("Number of dTF objects : " + str(len(self.list_dTF)) + "\n")
        #self.list_dSS = get_data("SS", "signal", "butter")# + get_data("SS", "random")
        self.list_dSS = get_data("SS", "random")
        print("Number of dSS objects : " + str(len(self.list_dSS)) + "\n")
        # TODO add PLANT generator to test closed-loop variants
    
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

        
    def test_algo(self):
        
        num, den = signal.butter(4,0.05)
        
        mySIF = DFI(num, den)
        
        mySIF.algorithmLaTeX('testlegend')
        
        mySIF.algorithmCfloat("myFunction", "cFile")
        
    def test_allSens(self):

        def _build_SIFobj_dict_ABCD(dSSobj_target, dSSobj_plant):
        
            SIFobj = State_Space(dSSobj.A,dSSobj.B,dSSobj.C,dSSobj.D)
        
            dict_ABCD = {}
        
            dict_ABCD['A'] = dSSobj_target.A
            dict_ABCD['B'] = dSSobj_target.B
            dict_ABCD['C'] = dSSobj_target.C
            dict_ABCD['D'] = dSSobj_target.D
            # plant
            dict_ABCD['Ap'] = dSSobj_plant.A
            dict_ABCD['Bp'] = dSSobj_plant.B
            dict_ABCD['Cp'] = dSSobj_plant.C
            dict_ABCD['Dp'] = dSSobj_plant.D
            
                    
            return SIFobj, dict_ABCD

        varz = ["OL_sensH", "OL_sensPole", "OL_RNG", "CL_sensH", "CL_sensPole", "CL_stability", "CL_RNG"]
        
        dict_ABCD = {}
        
        fipVarz = {}

        mtlb_cmd  = 'R = SS2FWR(A,B,C,D); \n'
        # open loop
        mtlb_cmd += "OL_sensH = MsensH(R); \n"
        mtlb_cmd += "OL_sensPole = MsensPole(R); \n"
        #mtlb_cmd += "OL_stability = Mstability(R); \n" # open-loop case
        mtlb_cmd += "OL_RNG = RNG(R); \n" # open-loop case
        
        # plant
        mtlb_cmd += "ss_plant = ss(Ap, Bp, Cp, Dp); \n"
        # closed-loop
        mtlb_cmd += "CL_sensH = MsensH(R, ss_plant); \n" 
        mtlb_cmd += "CL_sensPole = MsensPole(R, ss_plant); \n"
        mtlb_cmd += "CL_stability = Mstability(R, ss_plant); \n"
        mtlb_cmd += "CL_RNG = RNG(R); \n"
                
        for dSSobj in self.list_dSS:
        
            # SHITTY HACK
            # PLANT SHOULD REPLACE this fake, shitty, dumb dSSObj
            dSSobj_plant = dSSobj
        
            SIFobj, dict_ABCD = _build_SIFobj_dict_ABCD(dSSobj, dSSobj_plant) # PLANT SHOULD REPLACE SECOND dSSObj !!!
            
            self.engMtlb.setVar(dict_ABCD.keys(), dict_ABCD) # A,B,C,D, Ap,Bp,Cp,Dp
        
            # open loop
            fipVarz[varz[0]] = SIFobj.MsensH()
            fipVarz[varz[1]] = SIFobj.MsensPole()
            fipVarz[varz[2]] = SIFobj.RNG()
        
            # closed-loop
            fipVarz[varz[3]] = SIFobj.MsensH(dSSobj_plant)
            fipVarz[varz[4]] = SIFobj.MsensPole(dSSobj_plant)
            fipVarz[varz[5]] = SIFobj.Mstability(dSSobj_plant)            
            fipVarz[varz[6]] = SIFobj.RNG(dSSobj_plant)            
        
            self.engMtlb.compare(mtlb_cmd, varz, fipVarz, decim = self.ndigit)
        
        self.engMtlb.cleanenv()
        