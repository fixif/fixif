#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply, all, real, conj, diag
from numpy import transpose
from numpy.linalg import norm, inv, eig

from calc_plantSIF import calc_plantSIF

__all__ = ['calc_MsensPole']

def calc_MsensPole(R, loc_plant=None, moduli=1):
    
    def deigdZ(A, M1, M2, shapeZ, moduli=1):
        
        mylambda, Mx = eig(A)
        My = inv(Mx).transpose()
        
        mylambda = mat(mylambda)
        
        # sensitivity matrix
        
        dlk_dZ = zeros((shapeZ[0], shapeZ[1], mylambda.shape[1]))
        
        for k in range(0, mylambda.shape[1]):
            if moduli == 1:
                dlk_dZ[:,:,k] = transpose(M1)*(1/abs(mylambda[0,k]) * real( conj( mylambda[0,k] * conj(My[:,k])*transpose(Mx[:,k]) ))) * transpose(M2)
            else:
                dlk_dZ[:,:,k] = transpose(M1)*(conj(My[:,k])*transpose(Mx[:,k]))*transpose(M2)
                
        #dlambda_dZ
        
        dlambda_dZ = zeros(shapeZ)
        
        for i in range(0, shapeZ[0]):
            for j in range(0, shapeZ[1]):
                                
                if len(dlk_dZ[i,j,:].shape) == 1:
                    norm_target = diag(dlk_dZ[i,j,:]) # maybe there's a missing func or bug in numpy here, cannot calculate froebenius norm on a vector
                else:
                    norm_target = dlk_dZ[i,j,:] 
                    
                dlambda_dZ[i,j] = norm(norm_target, 'fro')
            
        return dlambda_dZ, dlk_dZ
    
    # open-loop case
    if loc_plant is None:
        
        dlambda_dZ, dlk_dZ = deigdZ(R.AZ, R.M1, R.N1, R.Z.shape)
        
    #closed-loop case
    else:
        
        Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar = calc_plantSIF(R, loc_plant)
        
        # dlambdabar,dlbk in _cl code
        dlambda_dZ, dlk_dZ = deigdZ(Abar, M1bar, N1bar, R.Z.shape, moduli)
        
    M = norm(multiply(dlambda_dZ, R.dZ), 'fro')
    M = M*M                
    
    return M, dlambda_dZ, dlk_dZ
