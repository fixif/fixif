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
sys.path.insert(0, os.path.abspath('./../'))

from Structures import *

#from scipy.signal.filter_design import butter
# currently matlab is used to builf butter LTI filter

from func_aux.MtlbHelper import MtlbHelper

from scipy.signal import tf2ss

from numpy import array, squeeze, reshape

import sys, os

class test_Structures(unittest.TestCase):

    def setUp(self):
        
        self.engMtlb = MtlbHelper()
        
        # add matlab script dir
        abs_fwr_dir = os.getcwd() + "/Structures/test/FWRToolbox/"
        self.engMtlb.eng.addpath(abs_fwr_dir,nargout=0)
        
        self.ndigit = 10
        self.eps = 1.e-8        

    def gen_TF_or_SS(self, type='TF',opt='butter', opt_num=0):
        
        tmp_vars = {}

        if opt == 'butter':
            
            if opt_num == 0:
                
                cmd  = '[num, den] = butter(4, 0.05) ;'
             
            #elif opt_num is 1:
            
                #cmd =  '[num, den] = butter(8, 0.12) ;'
                
            if type == 'TF':
                    
                varz = ['num','den']
                self.engMtlb.pushCmdGetVar(cmd, varz, tmp_vars)
                    
            elif type == 'SS':
                    
                varz = ['A','B', 'C', 'D']
                cmd += '[A,B,C,D] = tf2ss(num,den); \n'
                self.engMtlb.pushCmdGetVar(cmd, varz, tmp_vars)

        return tmp_vars

    def _reshape_1dto2d(self, var_dict): #could be replaced by atleast2d() ???
        
        for key in var_dict.keys():
            if var_dict[key].shape == (1,): # does not work with "is" ???
                var_dict[key] = var_dict[key].reshape(1,1)
                
        return var_dict
    
    def mytest_tf2ss(self, dict_numden):
        
        """
        Test numpy tf2ss routine (example for other tests involving FWRtoolbox)
        """
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)

        #print(self.engMtlb.eng.who())

        # create TF matlab obj from num and den
        mtlb_cmd  = 'H = tf(num,den,1); \n'
        
        # create Aq, Bq, Cq, Dq in Matlab workspace
        mtlb_cmd += '[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1}); \n'

        varz = ['Aq', 'Bq', 'Cq', 'Dq']
        
        tmp_vars['Aq'], tmp_vars['Bq'], tmp_vars['Cq'], tmp_vars['Dq'] = \
          tf2ss(squeeze(array(dict_numden['num'])), squeeze(array(dict_numden['den'])))
        
        tmp_vars = self._reshape_1dto2d(tmp_vars)
            
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
        
        self.engMtlb.cleanenv() # be nice with next test
        
    # test all Structures starting from most simple ones
    
    def mytest_State_Space(self, dict_ABCD):
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_ABCD.keys(), dict_ABCD)
        
        #print(self.engMtlb.eng.who())
        
        mtlb_cmd  = 'R = SS2FWR(A,B,C,D); \n'
        
        mtlb_cmd += 'Z = R.Z ;\n'
        
        varz = ['Z']
        
        tmp_vars['Z'] = State_Space(dict_ABCD['A'], dict_ABCD['B'], dict_ABCD['C'], dict_ABCD['D']).Z
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
    
        self.engMtlb.cleanenv() # be nice with next test 
    
    def mytest_DFI(self, dict_numden, opt):
        
        """
        Test DFIq2FWR.m vs. DFI.py (opt 1)
        Test DFIqbis2FWR.m vs. DFI.py (opt 2)
        """
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)

        #print(self.engMtlb.eng.who())

        # create TF matlab obj from num and den
        #mtlb_cmd_stack  = 'H = tf(num,den,1); \n'
        

        def dirty_debug(myCmd):
            # temp debug
            #debug_varz = ['myJ','myK','myL','myM','myN','myP','myQ','myR','myS']
            debug_varz = []
            debug_dict = {}
            debug_cmd = myCmd
            #
            self.engMtlb.pushCmdGetVar(debug_cmd, debug_varz, debug_dict)
            #
            print(debug_dict)

        if opt == 1:
            mtlb_cmd = 'R = DFIq2FWR(num, den) ; \n'
            tmp_vars['Z'] = DFI(dict_numden['num'], dict_numden['den'], opt=1, eps=self.eps).Z
        elif opt == 2:
            mtlb_cmd = 'R = DFIqbis2FWR(num, den); \n'
            #dirty_debug(mtlb_cmd)
            tmp_vars['Z'] = DFI(dict_numden['num'], dict_numden['den'], opt=2, eps=self.eps).Z
        else:
            raise('Unknown mytest_DFI opt number')
        
        varz = ['Z']
        
        mtlb_cmd += 'Z = R.Z ;\n'
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
    
        self.engMtlb.cleanenv() # be nice with next test 
        
    def mytest_DFII(self, dict_numden):
        
        """
        Test rhoDFIIt.m vs. DFII.py
        """
        
        # does not work this way as rhoDFIIt generates more variables
        # so we would need to use the "simplify" routine to erase those
        
        tmp_vars = {}
        
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)
        # create TF obj from num and den
        
        mtlb_cmd  = 'H = tf(num, den, 1); \n'
        mtlb_cmd += 'gamma = zeros([1 length(num)-1]); \n'
        mtlb_cmd += 'isGammaExact = 1; \n'
        mtlb_cmd += 'delta = ones(size(gamma)); \n'
        mtlb_cmd += 'isDeltaExact = 1; \n'
        mtlb_cmd += '[R1, R2, flag] = rhoDFIIt2FWR(H, gamma, isGammaExact, delta, isDeltaExact); \n'
        mtlb_cmd += 'Z1 = R1.Z; \n'
        mtlb_cmd += 'Z2 = R2.Z; \n'
    
        tmp_vars['Z1'] = DFII(dict_numden['num'], dict_numden['den']).Z
        tmp_vars['Z2'] = DFII(dict_numden['num'], dict_numden['den']).Z
        
        varz = ['Z1','Z2']
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
       
    def mytest_rhoDFIIt(self):
        
            
        """
        Test rhoDFIIt2FWR.m (opt=1), rhoDFIIt2FWRrelaxedL2 vs. rhoDFIIt.py
        """
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)

        #print(self.engMtlb.eng.who())

        # create TF matlab obj from num and den
        mtlb_cmd  = 'H = tf(num,den,1); \n'
        
        # use rhoDFIIt2FWR
        # probleme je n'ai pas de matrice gamma...
        if opt == 1:
            mtlb_cmd = 'R = rhoDFIIt2FWR(H) ; \n'
            tmp_vars['Z'] = RhoDFIIt(dict_numden['num'], dict_numden['den'], opt=1, eps=self.eps).Z
        elif opt == 2:
            mtlb_cmd = 'R = rhoDFIIt2FWR(H); \n'
            tmp_vars['Z'] = RhoDFIIt(dict_numden['num'], dict_numden['den'], opt=2, eps=self.eps).Z
        else:
            raise('Unknown mytest_DFI opt number')
        
        varz = ['Z']
        
        mtlb_cmd += 'Z = R.Z ;\n'
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
    
        self.engMtlb.cleanenv() # be nice with next test 
        
    
    #def mytest_modalDelta(self):
        
    #    pass
    
    def runTest(self):
        
        # test tf2ss on all transfer functions
        
        list_TF = {'butter':1}
        list_SS = {'butter':1}
        
        # all te'sts needing a TF input defined as num, den
        
        for TF in list_TF.keys():
            for i in range(0,list_TF[TF]):
                # test numpy tf2ss
                self.mytest_tf2ss(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i))

                # test DFI vs. DFIq2FWR
                #print("Testing DFI vs. DFIq2FWR")
                self.mytest_DFI(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i), opt=1)
                # test DFI vs. DFIqbis2FWR
                #print("Testing DFI vs. DFIqbis2FWR")
                self.mytest_DFI(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i), opt=2)
                # test DFII.py vs. rhoDFIIt.m with gamma = 0 and delta = 1
                #self.mytest_DFII(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i))
                
                #self.mytest_rhoDFIIt(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i))

        # all tests needing a State Space input, defined as A, B, C, D

        for SS in list_SS.keys():
            for i in range(0,list_SS[SS]):
                
                # test State_Space.py vs. SS2FWR.m
                self.mytest_State_Space(self.gen_TF_or_SS(type='SS', opt=SS, opt_num=i))

                # test DFI generation
                #self.mytest_DFI(self.gen_numDen(TF, i))
