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



__all__ = ['transform_UYW_RNG']

def transform_UYW_RNG(R, measureType, T1):
    
    """
    Here tol is removed from function parameters because it needs (?) to
    be the same with what was calculated for Rini (confirm with Thib)
    W is not used in this function (could be removed from calling args)
    """
    
    #dZ = R._RNG[measureType][1] # do not call function, refer to instance's attribute
    
    if measureType == 'OL':
    
        #l,m,n,p = R.size
    
        # BUG WARNING PROBLEM
        # BIG PROBLEM zeros(n,m) differs from existing definition of M1 zeros(n,p)
        # let's say it's an error and rely on our current implementation at SIF class level
        #M1 = c_[R.K*R.invJ, eye(n), zeros((n, m))]
        
        #M2 = c_[R.L*R.invJ, zeros((p, n)), eye(p)]
    
        # WARNING : need to check that Wo is calculated in a coherent state with the rest of the values
    
        # modify instance Attribute, bypass function
        # modify matrix G
        R._RNG[measureType][0] = trace( R._RNG[measureType][1] * (transpose(R.M2)*R.M2 + transpose(R.M1)*R.Wo*R.M1)) # needs Wo for current (ie. UYW transformed) system
        
    else: # measureType == 'CL'
        
        #l = Y.shape[1]
        #n = U.shape[1]
        
        #T1 = eye((l+n+R._p))
        #T1[0:l, 0:l] = Y
        #T1[l:l+n, l:l+n] = invU
        
#         T1, T2 = calc_transform_UYW(R, U, Y, W, invU)

        # WARNING PROBLEM TODO THIS VALUE HAS NOT BEEN UPDATED AND IS NOT COHERENT WITH THE REST
        # YES IT IS indeed according to Thibault
        
        #M1M2Wobar = R._RNG[measureType][2]
        
        # JOA I don't understand that the matrix M1M2Wobar is not modified by the UYW transform
        # modify matrix G, CL measureType

        R._RNG[measureType][0] = trace(inv(T1) * R._RNG[measureType][1] * inv(transpose(T1)) * R._RNG[measureType][2] )
        