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

__all__ = ['MsensH']

def MsensH(R, plant=None):
    
    """
    
    
    If open-loop,
    
    plant=None
    
    If closed-loop,
    
    plant=ss (state space)
    
    
    """

    # SISO opt disabled ATM

#     def _w_norm_prod_SISO(Ag, Bg, Cg, Dg, Ah, Bh, Ch, Dh, W):
#     
#         # Product matrices
#         A = r_[ c_[ Ag, mat(zeros(Ag.shape[0])), mat(zeros(Ah.shape[1])) ], c_[ Bh*Cg, Ah ] ]
#         B = r_[ Bg, Bh*Dg ]
#         C = r_[ Dh*Cg, Ch ]
#         D = Dh*Dg
#         
#         # MATLAB code
#         #Balance A matrix prior to performing Schur decomposition
#         #[t,A] = balance(A);
#         #B = t\B;
#         #C = C*t;
# 
#         # Perform schur decomposition on AA (and convert to complex form)
#         m, n = A.shape
#         AA = lstsq(A + eye(M), A - eye(M))[0] # x,resid,rank,s
#         
#         ta, ua = schur(AA, 'complex')
#         #ta, ua = schur(AA)
#         #ta, ua = rsf2csf(ta, ua)
#     
#         # Stability test
#         r = eig(A)
#         if abs(r).max() >= 1:
#             print("unstable system : 2-norm is infinite")
#             
#         # Computation of the norm
#         MX = zeros(W.shape)
#         
#         for i in range(0, W.shape[0]):
#             
#             BB = (eye(m) - AA)*B[:,i].transpose()*(eye(m) - AA.transpose())/2
            #P = 
    
    def _w_norm_prod(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W):

        Sg = dSS(Ag, Bg, Cg, Dg)        
        Sh = dSS(Ah, Bh, Ch, Dh)
        
        is_SISO_opt = False # disabled, code not complete
        
        if Dg.shape[0]*Dh.shape[1] == 1 & is_SISO_opt :
            
            print('SISO system')
            N, MX = _w_norm_prod_SISO(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)
        
        else:
            
            MX = zeros(W.shape)
            
            Sh_subsys_line = []
            
            for j in range(0, W.shape[1]):
                Sh_subsys_line.append(Sh[j,:])
            
            for i in range(0, W.shape[0]):
                  for j in range(0, W.shape[1]):
                       if not(W[i, j] == 0):
                           MX[i, j] = (Sg[:,i]*Sh_subsys_line[j]).norm('h2')
            
            MX = multiply(MX, W)
        
            N = norm(MX, 'fro')
            N = N*N # inlining x5 speedup... http://stackoverflow.com/questions/25254541/why-is-numpy-power-60x-slower-than-in-lining
        
        return N, MX
    
    l0, m0, n0, p0 = R.size
    
    # open-loop system
    if plant is None:
    
        # 16/11/15 : eye does not need a tuple, zeros does...
    
        M1 = c_[ R.K*inv(R.J), eye(n0), zeros((n0, p0)) ]
        M2 = c_[ R.L*inv(R.J), zeros((p0, n0)), eye(p0) ]
        N1 = r_[ inv(R.J)*R.M, eye(n0), zeros((m0, n0)) ]
        N2 = r_[ inv(R.J)*R.N, zeros((n0, m0)), eye(m0) ]
    
        M, MZ = _w_norm_prod(R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, R.dZ)
    
    else:
        
        # dimensions of plant system
        
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
        Bbar = r_[ B1 + B2*R.DZ*D21, R.BZ*D21 ]
        Cbar = c_[ C1 + D12*R.DZ*C2, D12*R.CZ ]
        Dbar = D11 + D12*R.DZ*D21
        
        # intermediate matrices
        
        invJ = inv(R.J)
        
        M1bar = r_[ c_[B2*R.L*invJ, zeros(n1, n0), B2], c_[R.K*invJ, eye(n0), zeros((n0, p1))] ]
        M2bar = c_[ D12*R.L*invJ, zeros((m2, n0)), D12 ]
        N1bar = r_[ c_[invJ*R.N*C2, invJ*R.M], c_[zeros((n0, n1)), eye(n0)], c_[C2, zeros((m1, n0))] ]
        N2bar = r_[ invJ*R.N*D21, zeros((n0, p2)), D21 ]
        
        # sensitivity matrix, and sensitivity measure
        
        M, MZ = _w_prod_norm(Abar,M1bar,Cbar,M2bar, Abar,Bbar,N1bar,N2bar, R.dZ)
        
    return M, MZ
   
   
   