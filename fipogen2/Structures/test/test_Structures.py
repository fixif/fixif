#coding=utf8

"""
Test for Structures
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

import sys, os
#sys.path.insert(0, os.path.abspath('./../'))

from Structures import *

#from scipy.signal.filter_design import butter
# currently matlab is used to builf butter LTI filter

from func_aux.MtlbHelper import MtlbHelper
from func_aux.get_data import get_data

from scipy.signal import tf2ss

from numpy import matrix as mat
from numpy import array, squeeze, reshape, zeros, ones

import sys, os

class test_Structures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
    	super(test_Structures, cls).setUpClass()
        
        cls.engMtlb = MtlbHelper()
        
        cls.ndigit = 10
        cls.eps = 1.e-8  
        
        cls.list_dSS = get_data("SS", "random", is_refresh=False) #+ get_data("SS", "signal", "butter", is_refresh=True)
        cls.list_dTF = get_data("TF", "signal", "butter", is_refresh=False)

    @staticmethod
    def _show_progress(testname, i_obj, n_obj):
        
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        
        if i_obj > 1:
            print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
            
        print ("{0} : obj {1: >3d} / {2}".format(testname, i_obj, n_obj))


    @staticmethod
    def _augment_dict_ABCD(dSSobj, target_dict):
        
        target_dict['A'] = dSSobj.A
        target_dict['B'] = dSSobj.B
        target_dict['C'] = dSSobj.C
        target_dict['D'] = dSSobj.D
    
    @staticmethod
    def _augment_dict_numden(dTFobj, target_dict):
        
        target_dict['num'] = dTFobj.num
        target_dict['den'] = dTFobj.den
    
    #@unittest.skip("skip DFI")
    def test_DFI(self):
        
        out_dict = {}
        fip_dict = {}
        
        varz = ['Z1','Z2']
        
        i_obj = 1
        n_obj = len(self.list_dTF)
        testname = 'DFI'
        
        for dTFobj in self.list_dTF:
            
            self._show_progress(testname, i_obj, n_obj)
            i_obj += 1
            
            self._augment_dict_numden(dTFobj, out_dict)
            self.engMtlb.setVar(out_dict.keys(), out_dict)
            
            mtlb_cmd  = """R1 = DFIq2FWR(num, den) ;
                           R2 = DFIqbis2FWR(num, den) ;
                           Z1 = R1.Z ;
                           Z2 = R2.Z ;"""           
            
            
            fip_dict['Z1'] = DFI(dTFobj.num, dTFobj.den, opt=1, eps=self.eps).Z
            fip_dict['Z2'] = DFI(dTFobj.num, dTFobj.den, opt=2, eps=self.eps).Z
            
            self.engMtlb.compare(mtlb_cmd, varz, fip_dict, decim = self.ndigit)
    
            self.engMtlb.cleanenv() # be nice with next test 
       
    #@unittest.skip("skip State_Space")
    def test_State_Space(self):
        
        out_dict = {}
        fip_dict = {}    
        
        varz = ['Z']

        i_obj = 1     
        n_obj = len(self.list_dSS)
        testname = "State_Space"
        
        for dSSobj in self.list_dSS:
            
            self._augment_dict_ABCD(dSSobj, out_dict)
            self.engMtlb.setVar(out_dict.keys(), out_dict)
            
            self._show_progress(testname, i_obj, n_obj)
            i_obj += 1
            
            mtlb_cmd  = """R = SS2FWR(A,B,C,D);
                            Z = R.Z ;"""
            
            fip_dict['Z'] = State_Space(dSSobj.A, dSSobj.B, dSSobj.C, dSSobj.D).Z
            
            self.engMtlb.compare(mtlb_cmd, varz, fip_dict, decim = self.ndigit)
    
            self.engMtlb.cleanenv() # be nice with next test 
    
#           tf2ss(squeeze(array(dict_numden['num'])), squeeze(array(dict_numden['den'])))
#             # squeeze(array(mat))<=> mat.A1

    def test_rhoDFIIt(self):
        
        out_dict = {}
        fip_dict = {}    
        
        varz = ['Z1', 'Z2', 'dZ1', 'dZ2']
        
        i_obj = 1
        n_obj = len(self.list_dTF)
        testname = 'rhoDFIIt'
        
        for dTFobj in self.list_dTF:
            
            self._augment_dict_numden(dTFobj, out_dict)
            self.engMtlb.setVar(out_dict.keys(), out_dict)
            
            self._show_progress(testname, i_obj, n_obj)
            i_obj += 1
            
            mtlb_cmd  = """H = tf(num, den, 1);
                           gamma = zeros([1 length(num)-1]);
                           isGammaExact = 1;
                           delta = ones(size(gamma));
                           isDeltaExact = 1;
                           [R1, R2, flag] = rhoDFIIt2FWR(H, gamma, isGammaExact, delta, isDeltaExact);
                           Z1 = R1.Z;
                           Z2 = R2.Z;
                           dZ1 = R1.rZ;
                           dZ2 = R2.rZ;
                           """
    
            "CODEPATH : isGammaExact = True, isDeltaExact = True, opt : ALL"
    
            self.engMtlb.eng.eval(mtlb_cmd, nargout = 0)
    
            cur_gamma = mat(zeros((out_dict['num'].shape[0], out_dict['num'].shape[1] - 1)))
            cur_delta = ones(cur_gamma.shape)
    
            SIF_1 = RhoDFIIt(out_dict['num'], out_dict['den'], gamma=cur_gamma, isGammaExact=True, delta=cur_delta, isDeltaExact=True, opt = '1')
            SIF_2 = RhoDFIIt(out_dict['num'], out_dict['den'], gamma=cur_gamma, isGammaExact=True, delta=cur_delta, isDeltaExact=True, opt = '2')
            
            fip_dict['Z1'] = SIF_1.Z
            fip_dict['dZ1'] = SIF_1.dZ
            fip_dict['Z2'] = SIF_2.Z
            fip_dict['dZ2'] = SIF_2.dZ
        
            self.engMtlb.compare(mtlb_cmd, varz, fip_dict, decim = self.ndigit)
    
            self.engMtlb.cleanenv() # be nice with next test             
                    
    def test_DFII(self):
        
        """
        Test rhoDFIIt.m vs. DFII.py
        """
        
        pass
     
        
    
