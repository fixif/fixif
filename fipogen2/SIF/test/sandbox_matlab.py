
# Test file for matlab engine in python

import sys, os
sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))
sys.path.insert(0, os.path.abspath('./../../'))

import matlab.engine

from scipy.signal import butter, tf2ss

import numpy.testing as npt

from scipy.io import loadmat

from numpy import matrix as mat
from numpy import array, squeeze, reshape

from Structures import *

def mtlb_save(eng, var):
    
    """
    saves var variable in var.mat file
    easier for debug purposes
    """
    
    fmt = "\'-v7\'" # we don't want hdf5 format
    filename = "\'" + var + ".mat\'"
    
    str_save = 'save(' + filename + ",\'" + var + "\'," + fmt + ');'
    
    print(str_save)
    eng.eval(str_save,nargout=0)

def mtlb_cleanenv(eng):
    eng.eval('clear all ; close all ;',nargout=0)
  
def mtlb_getArray(target_var):
    
    filename = target_var + '.mat'
    
    h = loadmat(filename)
    return h[target_var]

def mtlb_pushCmdGetVar(mtlb_eng, mtlb_code, varz, local_dict):
    
    print(mtlb_code)
    
    mtlb_eng.eval(mtlb_code, nargout=0)
    
    for var in varz:
        mtlb_save(mtlb_eng, var)
        local_dict[var] = mtlb_getArray(var)

def mtlb_compare(mtlb_eng, mtlb_code, varz, local_varz_dict, decim = 10):

    """
    Compare value with matlab values for a given executed code
    """
    
    tmp_dict = {}
    
    mtlb_cleanenv(mtlb_eng)
    
    mtlb_pushCmdGetVar(mtlb_eng, mtlb_code, varz, tmp_dict)
    
    for var in varz:
    	
    	#print("Shape of tmp_dict[" + var + "]")
    	#print(str(tmp_dict[var].shape))
    	#print("Shape of local_varz_dict["+ var +"]")
    	#print(str(local_varz_dict[var].shape))
    	
        npt.assert_almost_equal(tmp_dict[var], local_varz_dict[var], decimal=decim)


        
    

# TEST 1 : reproduce matlab results with numpy/scipy and FIPOgen

# Test of parts from higher_order_p.m

#local_vars = {}

#eng = matlab.engine.start_matlab()

#get num and den from matlab as starting point

mtlb_vars = {}
local_vars = {}

mtlb_cmd_stack = ''

cmd = '[num, den] = butter(4, 0.05) ;'
varz = ['num','den']

mtlb_cmd_stack += cmd
mtlb_cmd_stack += '\n'

mtlb_pushCmdGetVar(eng, cmd, varz, mtlb_vars)


cmd = 'H = tf(num,den,1);'
# create TF matlab obj from num and den
eng.eval(cmd, nargout=0)

mtlb_cmd_stack += cmd
mtlb_cmd_stack += '\n'

#eng.eval('R1, R2, flag = rhoDFIIt2FWR(H, gamma)')

# convert TF to SS
cmd = '[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});'
varz = ['Aq','Bq','Cq','Dq']

mtlb_pushCmdGetVar(eng, cmd, varz, mtlb_vars)

mtlb_cmd_stack += cmd
mtlb_cmd_stack += '\n'

# create local vars

local_vars['Aq'], local_vars['Bq'], local_vars['Cq'], local_vars['Dq'] = tf2ss(squeeze(array(mtlb_vars['num'])), squeeze(array(mtlb_vars['den'])))

local_vars['Dq'] = local_vars['Dq'].reshape(1,1)

# Test comparison routine

mtlb_compare(eng, mtlb_cmd_stack, varz, local_vars, decim = 10)


#mtlb_pushCmdGetVar(eng, cmd, varz, local_vars)

# compare 

varz = ['R1', 'R2']

#R1, R2 = rhoDFIIt2FWR(num, den)

# load test file