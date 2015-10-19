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

        if opt is 'butter':
            
            if opt_num is 0:
                
                cmd  = '[num, den] = butter(4, 0.05) ;'
             
            #elif opt_num is 1:
            
                #cmd =  '[num, den] = butter(8, 0.12) ;'
                
            if type is 'TF':
                    
                varz = ['num','den']
                self.engMtlb.pushCmdGetVar(cmd, varz, tmp_vars)
                    
            elif type is 'SS':
                    
                varz = ['A','B', 'C', 'D']
                cmd += '[A,B,C,D] = tf2ss(num,den); \n'
                self.engMtlb.pushCmdGetVar(cmd, varz, tmp_vars)

        return tmp_vars

    def _reshape_1dto2d(self, var_dict):
        
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
        
        print(self.engMtlb.eng.who())
        
        mtlb_cmd  = 'R = SS2FWR(A,B,C,D); \n'
        
        mtlb_cmd += 'Z = R.Z ;\n'
        
        varz = ['Z']
        
        tmp_vars['Z'] = State_Space(dict_ABCD['A'], dict_ABCD['B'], dict_ABCD['C'], dict_ABCD['D']).Z
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
    
        self.engMtlb.cleanenv() # be nice with next test 
    
    def mytest_DFI(self, dict_numden, opt):
        
        """
        Test DFIq2FWR.m vs. DFI.py
        """
        
        tmp_vars = {}

        # Inject num and den in Matlab workspace
        self.engMtlb.setVar(dict_numden.keys(), dict_numden)

        #print(self.engMtlb.eng.who())

        # create TF matlab obj from num and den
        #mtlb_cmd_stack  = 'H = tf(num,den,1); \n'
        
        # use DFI2FWR
        if opt is 1:
            mtlb_cmd = 'R = DFIq2FWR(num, den) ; \n'
            tmp_vars['Z'] = DFI(dict_numden['num'], dict_numden['den'], opt=1, eps=self.eps).Z
        elif opt is 2:
            mtlb_cmd = 'R = DFIqbis2FWR(num, den); \n'
            tmp_vars['Z'] = DFI(dict_numden['num'], dict_numden['den'], opt=2, eps=self.eps).Z
        else:
            raise('Unknown mytest_DFI opt number')
        
        varz = ['Z']
        
        mtlb_cmd += 'Z = R.Z ;\n'        
        
        self.engMtlb.compare(mtlb_cmd, varz, tmp_vars, decim = self.ndigit)
    
        self.engMtlb.cleanenv() # be nice with next test 
        
    #def mytest_DFII(self):
        
    #    pass
       
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
		if opt is 1:
			mtlb_cmd = 'R = rhoDFIIt2FWR(H) ; \n'
			tmp_vars['Z'] = RhoDFIIt(dict_numden['num'], dict_numden['den'], opt=1, eps=self.eps).Z
		elif opt is 2:
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

                # test DFI vs. DFIq2FWR ; DFI vs. DFIqbis2FWR
                # NON-WORKING see with thibault
                #self.mytest_DFI(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i), opt=1)
                #self.mytest_DFI(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i), opt=2)
                
                #self.mytest_rhoDFIIt(self.gen_TF_or_SS(type='TF', opt=TF, opt_num=i))

        # all tests needing a State Space input, defined as A, B, C, D

        for SS in list_SS.keys():
            for i in range(0,list_SS[SS]):
                
                # test State_Space.py vs. SS2FWR.m
                self.mytest_State_Space(self.gen_TF_or_SS(type='SS', opt=SS, opt_num=i))

                # test DFI generation
                #self.mytest_DFI(self.gen_numDen(TF, i))
