
# Test file for matlab engine in python

import sys, os
sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))

import matlab.engine

from scipy.signal import butter, tf2ss



def mtlb_save(filename, variables):
    
    """
    generate a string to save some variables in a matlab file
    variables is an array of strings
    filename completed with .mat
    """
    fmt = '\'-v7\'' # we don't want hdf5 format  
    filename = '\'' + filename + '.mat\''
  
    str_save = 'save(' + '\'' + filename + '\', '
  
    for var in variables:
       str_save += '\'' + var + '\', '
       
    str_save += fmt + ');'
  
    return str_save

def mtlb_listvar(varz):
  
    str_varz = ''
  
      for var in varz:
          str_varz += var + ','

    return str_varz[:-1]


# TEST 1 : reproduce matlab results with numpy/scipy and FIPOgen

# Test of parts from higher_order_p.m
eng = matlab.engine.start_matlab()

# create LTI filter example
eng.eval('[num, den] = butter(4, 0.05) ;')

num, den = butter(4, 0.05)

# create TF
eng.eval('H = tf(num,den,1);')

# convert TF to SS
eng.eval('[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});')

Aq, Bq, Cq, Dq = tf2ss(num, den)

varz = ['R1', 'R2']

eng.eval(mtlb_listvar(varz) + ' = rhoDFIIt2FWR(H, );')
# save test file
file_rhodfiit = 'rhoDFIIt'
eng.eval(mtlb_save('rhoDFIIt',varz))

R1, R2 = rhoDFIIt2FWR(num, den)

# load test file