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
from numpy import eye, c_, r_, zeros, multiply, all
from numpy import transpose
from numpy.linalg import norm, inv, lstsq, eig
#from scipy.linalg import schur

__all__ = ['calc_transform_UYW']

def calc_transform_UYW(R):
    
    """
    This function gives intermediate matrixes
    for transformation of sensitivity measurements
    using UYW matrixes
    """
    
    l = R.Y.shape[1]
    n = R.U.shape[1]
    
    T1 = mat(eye(l+n+R._p))
    T1[0:l, 0:l] = R.Y
    T1[l:l+n, l:l+n] = R.invU
    
    T2 = mat(eye(l+n+R._m))
    T2[0:l, 0:l] = R.W
    T2[l:l+n, l:l+n] = R.U
    
    return T1, T2
    
    