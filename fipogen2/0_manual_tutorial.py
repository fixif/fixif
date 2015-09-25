#!/usr/bin/env python
#coding=utf8 

"""
This test script is used as a tool to test FIPOgen functionality
using a workflow defined in the manual's example
"""
# scripts cannot use relative imports
import sys,os
sys.path.insert(0, os.path.abspath('./'))

from numpy import matrix as mat

from SIF import State_Space
from LTI import TF

def main():
  
    """
  
    We encapsulate the script in the main function to speedup code 
  
    (see interesting :
  
    http://stackoverflow.com/questions/419163/what-does-if-name-main-do
    http://stackoverflow.com/questions/11241523/why-does-python-code-run-faster-in-a-function
  
    """

    # create matrixes for Discrete State Space
    A = mat([[1.4590, -0.91037, 0.39565],[1., 0., 0.],[0., 0.5, 0.]])
    B = mat([[0.5],[0.],[0.]])
    C = mat([0.28261, 0.13244, 0.15183])
    D = mat([0.0031689])
    
    myState_Space = State_Space(A,B,C,D)
    
    mySIF = myState_Space.toSIF()

    print(str(mySIF))
    
    num = mat([0.125, 0.243, 2.67, 4.72])
    den = mat([0.321, 0.546, 7.56473, 9.786750])

    myTF = TF(num,den)
    
    print(str(myTF))

if __name__ == '__main__':
    main()