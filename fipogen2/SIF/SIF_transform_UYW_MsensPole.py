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
from numpy import eye, c_, r_, zeros, multiply, all, diagflat, trace, ones, where, logical_or, fromfunction
from numpy import transpose, fmod, log2, fromfunction, diag
from numpy.linalg import norm, inv, eig

__all__ = ['transform_UYW_MsensPole']

def transform_UYW_MsensPole(R, measureType, T1, T2):

    dlk_dZ = zeros(R._MsensPole[measureType][2].shape)
    dlambda_dZ = zeros(R._MsensPole[measureType][1].shape)# dlambdabar_dZ if measureType == 'CL'
    
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
        #dlk_dZ[:,:,i] = transpose(inv(T1)) * dlk_dZ[:,:,i] * transpose(inv(T2))
        dlk_dZ[:,:,i] = transpose(inv(T1)) * R._MsensPole[measureType][2][:,:,i] * transpose(inv(T2))
    
    # update dlk_dZ
    R._MsensPole[measureType][2] = dlk_dZ
    
    # in current version of numpy clever vectorization is NOT possible :
    # - vectorize is just a more idiomatic, hidden for loops http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.vectorize.html
    # fromfunction uses (par1,par2) as input array for function https://mail.scipy.org/pipermail/numpy-discussion/2007-August/028800.html
    # http://stackoverflow.com/questions/31721404/evaluating-python-lambda-function-with-numpys-np-fromfunction
    # http://stackoverflow.com/questions/24740249/populating-a-numpy-matrix-using-fromfunction-and-an-array
    
    #dlambda_dZ = mat(fromfunction(lambda i, j: norm(dlk_dZ[i,j,:], 'fro'), (R._l+R._n+R._p, R._l+R._n+R._m)), dtype=int)
    
    
    
    for i in xrange(0, R._l+R._n+R._p):
        for j in xrange(0, R._l+R._n+R._m):
            
            if len(dlk_dZ[i,j,:].shape) == 1:
                norm_target = diag(dlk_dZ[i,j,:]) # maybe there's a missing func or bug in numpy here, cannot calculate froebenius norm on a vector
            else:
                norm_target = dlk_dZ[i,j,:] 
            
            dlambda_dZ[i, j] = norm(norm_target, 'fro')
    
    #update dlambda_dZ
    R._MsensPole[measureType][1] = dlambda_dZ
    
    # Measure
       
    M = norm(multiply(dlambda_dZ, R.dZ), 'fro')
    M = M*M
    
    #update M
    R._MsensPole[measureType][0] = M
            
    