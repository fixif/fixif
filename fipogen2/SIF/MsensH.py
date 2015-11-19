#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

#import SIF

from LTI import dSS

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply
from numpy.matrix import transpose
from numpy.linalg import norm, inv, lstsq, eig, max, abs
from scipy.linalg import schur


def MsensH(R):
    
    """
    OPEN-LOOP
    """

    def _w_norm_prod_SISO(Ag, Bg, Cg, Dg, Ah, Bh, Ch, Dh, W):
    
        # Product matrices
        A = r_[ c_[ Ag, mat(zeros(Ag.shape[0])), mat(zeros(Ah.shape[1])) ], c_[ Bh*Cg, Ah ] ]
        B = r_[ Bg, Bh*Dg ]
        C = r_[ Dh*Cg, Ch ]
        D = Dh*Dg
        
        # MATLAB code
        #Balance A matrix prior to performing Schur decomposition
        #[t,A] = balance(A);
        #B = t\B;
        #C = C*t;

        # Perform schur decomposition on AA (and convert to complex form)
        m, n = A.shape
        AA = lstsq(A + eye(M), A - eye(M))[0] # x,resid,rank,s
        
        ta, ua = schur(AA, 'complex')
        #ta, ua = schur(AA)
        #ta, ua = rsf2csf(ta, ua)
    
        # Stability test
        r = eig(A)
        if max(abs(r)) >= 1:
        	print("unstable system : 2-norm is infinite")
        	
        # Computation of the norm
        MX = zeros(W.shape)
        
        for i in range(0, W.shape[0]):
        	
        	BB = (eye(m) - AA)*B[:,i].transpose()*(eye(m) - AA.transpose())/2
        	#P = 
    
    def _w_norm_prod(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W):

        Sg = dSS(Ag, Bg, Cg, Dg)        
        Sh = dSS(Ah, Bh, Ch, Dh)
        
        if Dg.shape[0]*Dh.shape[1] == 1:
            
            print('SISO system')
            N, MX = _w_norm_prod_SISO(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)
        
        else:
            
            MX = zeros(W.shape)
            
            for i in range(0, W.shape[0]):
                  for j in range(0, W.shape[1]):
                       if not(W[i, j] == 0):
                           MX[i, j] = (Sg[:,i]*Sg[j,:]).norm('h2')
            
            MX = multiply(MX, W)
        
            N = norm(MX, 'fro')^2
        
        return N, MX
        

    
    l,m,n,p = R.size
    
    # 16/11/15 : eye does not need a tuple, zeros does...
    
    M1 = c_[ R.K*inv(R.J), mat(eye(n)), mat(zeros((n, p))) ]
    M2 = c_[ R.L*inv(R.J), mat(zeros((p, n))), mat(eye(p)) ]
    N1 = r_[ inv(R.J)*R.M, mat(eye(n)), mat(zeros((m, n))) ]
    N2 = r_[ inv(R.J)*R.N, mat(zeros((n, m))), mat(eye(m)) ]
    
    M, MZ = _w_norm_prod(R._AZ,M1,R._CZ,M2, R._AZ,R._BZ,N1,N2, R.dZ)
    
    return M, MZ
   
   
   