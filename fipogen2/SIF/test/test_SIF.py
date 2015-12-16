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

from numpy import zeros
import matlab # needed to catch matlab-specific exceptions

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
        
        self.ndigit = 10
        self.eps = 1.e-8    
    
        self.list_dTF = get_data("TF", "signal", "butter", is_refresh=True)# + get_data("TF", "random")
        #self.list_dTF = get_data("TF", "random") ,BUG
        #print("Number of dTF objects : " + str(len(self.list_dTF)) + "\n")
        #self.list_dSS = get_data("SS", "signal", "butter")# + get_data("SS", "random")
        self.list_dSS = get_data("SS", "random", is_refresh=True)
        #print("Number of dSS objects : " + str(len(self.list_dSS)) + "\n")
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

        def _build_dict_ABCD(dSSobj_target, dSSobj_plant):
        
            dict_ABCD['A'] = dSSobj_target.A
            dict_ABCD['B'] = dSSobj_target.B
            dict_ABCD['C'] = dSSobj_target.C
            dict_ABCD['D'] = dSSobj_target.D
            
            # plant
            if is_plant_found:
                dict_ABCD['Ap'] = dSSobj_plant.A
                dict_ABCD['Bp'] = dSSobj_plant.B
                dict_ABCD['Cp'] = dSSobj_plant.C
                dict_ABCD['Dp'] = dSSobj_plant.D
            
            return dict_ABCD
        
        n_obj = len(self.list_dSS)
        
        i_obj = 1
            
        for dSSobj in self.list_dSS:
            
            print ("obj {0: >3d} / {1}".format(i_obj, n_obj))
            i_obj += 1
            
            fipVarz = {}
            dict_ABCD = {}

            # open loop
            varz = ["OH_M", "OH_MZ", "OP_M", "OP_dlambda_dZ", "OP_dlk_dZ", "ORNG_G", "ORNG_dZ"]
            
            mtlb_cmd  = 'R = SS2FWR(A,B,C,D); \n'

            mtlb_cmd += "[OH_M, OH_MZ] = MsensH(R); \n"
            mtlb_cmd += "[OP_M, OP_dlambda_dZ, OP_dlk_dZ] = MsensPole(R); \n"
            mtlb_cmd += "[ORNG_G, ORNG_dZ] = RNG(R); \n" # open-loop case
        
            SIFobj = State_Space(dSSobj.A,dSSobj.B,dSSobj.C,dSSobj.D)
                    
            l0, m0, n0, p0 = SIFobj.size
         
               # find random_dSS satisfying size requirements
         
            for dSSobj2 in self.list_dSS:
                
                n1,p1,q1 = dSSobj2.size
                
                if not(p1 - p0 <= 0) and not(q1 - m0 <= 0) : # add test not equal to zero
                    dSSobj_plant = dSSobj2
                    
                    # FUCKING HACK : if some properties are already calculated this is all shitty
                    # see if we need to add special setters to dSS objject redefining properties and checking that D size is coherent
                    # with what already exists.
                    dSSobj_plant._D = zeros(dSSobj2.D.shape)
                    
                    is_plant_found = True
                    # closed loop
                    varz += ["CH_M", "CH_MZ", "CP_M", "CP_dlambdabar_dZ", "CP_dlbk_dZ", "CS_M", "CRNG_G", "CRNG_dZ", "CRNG_M1M2Wobar"]
                    #closed loop
                    mtlb_cmd += "ss_plant = ss(Ap, Bp, Cp, Dp); \n"
                    # closed-loop
                    mtlb_cmd += "[CH_M, CH_MZ] = MsensH_cl(R, ss_plant); \n" 
                    mtlb_cmd += "[CP_M, CP_dlambdabar_dZ, CP_dlbk_dZ] = MsensPole_cl(R, ss_plant); \n"
                    mtlb_cmd += "CS_M = Mstability(R, ss_plant); \n"
                    mtlb_cmd += "[CRNG_G, CRNG_dZ, CRNG_M1M2Wobar] = RNG_cl(R, ss_plant); \n"
                    break     
                            
            else:
                is_plant_found = False
        
            dict_ABCD = _build_dict_ABCD(dSSobj, dSSobj_plant)
            
            self.engMtlb.setVar(dict_ABCD.keys(), dict_ABCD) # A,B,C,D, (if plant : Ap,Bp,Cp,Dp)
        
#             print('SIZE OF controller')
#             print('(l, m2, n, p2)')
#             print(SIFobj.size)
#             print('SIZE of plant')
#             print('(np, p, m)')
#             print(dSSobj_plant.size)
        
            #try:
            #    self.engMtlb.eng.eval(mtlb_cmd, nargout = 0)
            #except matlab.engine.MatlabExecutionError:
            #	print('shit in the fan')
            
            # open loop
            
            tmp_var = SIFobj.MsensH()
            fipVarz[varz[0]] = tmp_var[0]
            fipVarz[varz[1]] = tmp_var[1]
            
            tmp_var = SIFobj.MsensPole()
            fipVarz[varz[2]] = tmp_var[0]
            fipVarz[varz[3]] = tmp_var[1]
            fipVarz[varz[4]] = tmp_var[2]
        
            tmp_var = SIFobj.RNG()
            fipVarz[varz[5]] = tmp_var[0]
            fipVarz[varz[6]] = tmp_var[1]
            
            # closed-loop
            if is_plant_found:
            	
                tmp_var = SIFobj.MsensH(dSSobj_plant)
                fipVarz[varz[7]] = tmp_var[0]
                fipVarz[varz[8]] = tmp_var[1]
            
                tmp_var = SIFobj.MsensPole(dSSobj_plant)
                fipVarz[varz[9]] = tmp_var[0]
                fipVarz[varz[10]] = tmp_var[1]
                fipVarz[varz[11]] = tmp_var[2]            

                tmp_var = SIFobj.Mstability(dSSobj_plant)
                fipVarz[varz[12]] = tmp_var[0]

                tmp_var = SIFobj.RNG(dSSobj_plant)
                fipVarz[varz[13]] = tmp_var[0]
                fipVarz[varz[14]] = tmp_var[1]
                fipVarz[varz[15]] = tmp_var[2]
                
            else:
            	print('No suitable plant found, skipping tests involving plant')        
         
            self.engMtlb.compare(mtlb_cmd, varz, fipVarz, decim = self.ndigit)
        
            self.engMtlb.cleanenv()
        