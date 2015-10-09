
# Test file for matlab engine in python

import sys, os
sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))
sys.path.insert(0, os.path.abspath('./../../'))

import matlab.engine

from scipy.signal import butter, tf2ss

import numpy.testing as npt

from scipy.io import loadmat

from numpy import matrix as mat
from numpy import array

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
    eng.eval('clear all ; close all ;')
  

def mtlb_compare(mtlb_eng, mtlb_code, varz, local_varz_dict, decim = 10):

    """
    Compare value with matlab values for a given executed code
    """
    mtlb_cleanenv(mtlb_eng)
    
    mtlb_eng.eval(mtlb_code)
    
    for var in varz:
        mtlb_save(var)
    
    mtlb_load(filename)
    
    npt.assert_almost_equal(mtlb_getArray(var), local_varz_dict[var], decimal=decim)

def mtlb_getArray(target_var):
    
    filename = target_var + '.mat'
    
    h = loadmat(filename)
    return mat(h[target_var])

def mtlb_pushCmdGetVar(mtlb_eng, mtlb_code, varz, local_dict):
    
    mtlb_eng.eval(mtlb_code, nargout=0)
    
    for var in varz:
        mtlb_save(mtlb_eng, var)
        local_dict[var] = mtlb_getArray(var)
        
    

# TEST 1 : reproduce matlab results with numpy/scipy and FIPOgen

# Test of parts from higher_order_p.m

#local_vars = {}

eng = matlab.engine.start_matlab()

#get num and den from matlab as starting point

mtlb_vars = {}
local_vars = {}

cmd = '[num, den] = butter(4, 0.05) ;'
varz = ['num','den']

mtlb_pushCmdGetVar(eng, cmd, varz, mtlb_vars)

# create TF matlab obj from num and den
eng.eval('H = tf(num,den,1);', nargout=0)

#eng.eval('R1, R2, flag = rhoDFIIt2FWR(H, gamma)')

# convert TF to SS
cmd = '[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});'
varz = ['Aq','Bq','Cq','Dq']

mtlb_pushCmdGetVar(eng, cmd, varz, mtlb_vars)

# create local vars

Aq, Bq, Cq, Dq = tf2ss(array(mtlb_vars['num']), array(mtlb_vars['den']))

local_vars['Aq'] = Aq
local_vars['Bq'] = Bq
local_vars['Cq'] = Cq
local_vars['Dq'] = Dq

# Test comparison routine

mtlb_compare(eng, cmd, varz, local_vars, decimal = 10)


#mtlb_pushCmdGetVar(eng, cmd, varz, local_vars)

# compare 

varz = ['R1', 'R2']

#R1, R2 = rhoDFIIt2FWR(num, den)

# load test file