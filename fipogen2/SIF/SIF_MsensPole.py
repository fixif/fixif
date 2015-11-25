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
from numpy import eye, c_, r_, zeros, multiply, all, real, conj
from numpy import transpose
from numpy.linalg import norm, inv, eig

__all__ = ['MsensPole']

def MsensPole(R, plant=None, moduli=1):
    
    def deigdZ(A, M1, M2, shapeZ, moduli):
        
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
                dlambda_dZ[i,j] = norm(dlk_dZ[i,j,:],'fro')
            
        return dlambda_dZ, dlk_dZ
    
    # open-loop case
    if Plant is None:
        
        invJ = inv(J)
    
        M1 = c_[R.K*invJ, eye(R.n), zeros((R.n, R.p))]
        N1 = r_[invJ*R.M, eye(R.n), zeros((R.m,R.n))]
    
        # measures
        # moduli is not sent in MsensPole
        dlambda, dlk_dZ = deigdZ(R.AZ, M1, N1, R.Z.shape)
        
    #closed-loop case
    else:
    
        # same code as closed-loop case MsensH
                # dimensions of plant system
                
        l0, m0, n0, p0 = R.size
        n1, p1, q1 = plant.size
        
        q2 = q1 - m0 
        p2 = p1 - p0
        
        if p1 < 0 or m1 <= 0:
            raise(ValueError,"dimension error : check plant and realization dimension")
        
        
        B1 = plant.B[:, :p2-1]
        B2 = plant.B[:, p2:p0-1]
        C1 = plant.C[:m2-1, :]
        C2 = plant.C[m2:m0-1, :]        

        D11 = plant.D[:p2-1, :m2-1]
        D12 = plant.D[:p2-1, m2:m0]
        D21 = plant.D[p2:p0-1, :m2-1]
        D22 = plant.D[p2:p0-1, m2:m0-1]
        
        if not (all(D22 == zeros(D22.shape))):
            raise(ValueError, "D22 needs to be null")
        
        # closed-loop related matrices
        Abar = r_[ c_[plant.A + B2*R.DZ*C2, B2*R.CZ], c_[R.BZ*C2, R.AZ] ]
    
        # intermediate matrices
        invJ = inv(R.J)
        
        M1bar = r_[ c_[B2*R.L*invJ, zeros(n1, n0), B2], c_[R.K*invJ, eye(n0), zeros((n0, p1))] ]
        N1bar = r_[ c_[invJ*R.N*C2, invJ*R.M], c_[zeros((n0, n1)), eye(n0)], c_[C2, zeros((m1, n0))] ]
        
        # dlambdabar,dlbk in _cl code
        dlambda_dZ, dlk_dZ = deigdZ(Abar, M1bar, N1bar, R.Z.shape, moduli)
        
    M = norm(multiply(dlambda_dZ, R.dZ), 'fro')
    M = M*M                
    
    return M, dlambda_dZ, dlk_dZ
