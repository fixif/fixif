
# Test file for matlab engine in python

import sys, os
sys.path.insert(0, os.path.abspath('./FWRtoolbox/'))

import matlab.engine

# Test of parts from higher_order_p.m

eng = matlab.engine.start_matlab()

[num, den] = eng.butter(4,0.05)

