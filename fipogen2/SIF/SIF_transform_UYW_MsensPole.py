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
from numpy import transpose, fmod, log2, fromfunction
from numpy.linalg import norm, inv, eig

from calc_transform_UYW import calc_transform_UYW

__all__ = ['transform_UYW_MsensPole']

def transform_UYW_MsensPole(R, UYW):
    
    U, Y, W = UYW
    
    dlk_dZ = R.MsensH[type][2]
        
    lS, mS, nS, pS = R.size
    
    k = dlk_dZ.shape[2]

    T1, T2 = calc_transform_UYW(UYW)
    
    for i in range(0, k):
        dlk_dZ[:,:,i] = transpose(inv(T1)) * dlk_dZ[:,:,i] * transpose(inv(T2))
    
    dlambda_dZ = mat(np.fromfunction(lambda i, j: norm(dlk_dZ[i,j,:], 'fro'), (l+n+pS, l+n+mS)))
    
    #for i in range(0, l+n+pS):
    #    for j in range(0, l+n+mS):
    #        dlambda_dZ[i,j] = norm(dlk_dZ[i,j,:], 'fro')
    
    # Measure
       
    M = norm(multiply(dlambda_dZ, R.dZ), 'fro')
    M = M*M
    
    return M    
            
    