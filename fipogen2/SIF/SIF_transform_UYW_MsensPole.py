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

def transform_UYW_MsensPole(R, measureType, T1, T2):

    dlk_dZ = R._MsensPole[measureType][2]
    dlambda_dZ = R._MsensPole[measureType][1]# dlambdabar_dZ if measureType == 'CL'
    
#     k = dlk_dZ.shape[2]
    
#     l = Y.shape[1]
#     n = U.shape[1]
#         
#     T1 = eye(l+n+R._p)
#     T1[0:l, 0:l] = Y
#     T1[l:l+n, l:l+n] = invU
#     
#     T2 = eye(l+n+R._m)
#     T2[0:l, 0:l] = W
#     T2[l:l+n, l:l+n] = U
    
    for i in range(0, dlk_dZ.shape[2]):
        dlk_dZ[:,:,i] = transpose(inv(T1)) * dlk_dZ[:,:,i] * transpose(inv(T2))
    
    dlambda_dZ = mat(np.fromfunction(lambda i, j: norm(dlk_dZ[i,j,:], 'fro'), (l+n+R._p, l+n+R._m)))
    
    # Measure
       
    M = norm(multiply(dlambda_dZ, R.dZ), 'fro')
    M = M*M
    
    R._MsensPole[measureType][0] = M
            
    