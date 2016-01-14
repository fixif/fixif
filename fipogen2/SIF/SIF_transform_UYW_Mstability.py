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
from numpy import eye, c_, r_, zeros, multiply, all, diagflat, trace, ones, where, logical_or
from numpy import transpose, fmod, log2
from numpy.linalg import norm, inv, eig

#from calc_plantSIF import calc_plantSIF

__all__ = ['transform_UYW_Mstability']

def transform_UYW_Mstability(R, T1, T2):
    
    dlbk_dZ = R._MsensPole['CL'][2]
    
    #T1, T2 = calc_transform_UYW(R, U, Y, W, invU)
    
    # PROBLEM is the stored value correct ? YES updated
    mylambda = mat(eig(R.Abar)[0])
    
    Psi = zeros((dlbk_dZ.shape[2]))
    
    for i in range(0, dlbk_dZ.shape[2]):
        dlbk_dZ[:,:,i] = transpose(inv(T1)) * dlk_dZ[:,:,i] * transpose(inv(T2))
        Psi[i] = norm(R.dZ, 'fro') * norm( multiply(dlbk_dZ[:,:,i], R.dZ), 'fro')
    
    R._Mstability = min(divide(1-abs(mylambda), Psi))
    
    