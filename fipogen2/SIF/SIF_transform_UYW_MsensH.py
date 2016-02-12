#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from LTI import dSS

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply, all, diagflat, trace, ones, where, logical_or, kron
from numpy import transpose, fmod, log2
from numpy.linalg import norm, inv, eig

#from calc_plantSIF import calc_plantSIF

__all__ = ['transform_UYW_MsensH']

def transform_UYW_MsensH(R, measureType):

    """
    Transform mSensH with formula at page 165 of Thib's thesis
    Currently uses bruteforce calculation because formula for
    MsensH[measureType][1] is unknown
    """
    
    #mat1 = kron(transpose(inv(T1)), mat(eye(R._p)))
    #mat2 = kron(transpose(inv(T2)), mat(eye(R._m)))
    
    #R._MsensH[measureType][0] = mat1 * R._MsensH[measureType][0] * mat2
    #R._MsensH[measureType][1] = mat1 * R._MsensH[measureType][1] * mat2
    
    # problem I don't know how to transform Mz
    
    # bruteforce calculation 
    
    R._MsensH[measureType] = R.calc_MsensH(measureType)