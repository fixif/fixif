#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

import SIF

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply
from numpy.linalg import norm, inv

def MsensH(R):
    
    """
    OPEN-LOOP
    """
    
    def _w_norm_prod(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W):
        
        Sg = dSS(Ag, Bg, Cg, Dg)
        Sh = dSS(Ah, Bh, Ch, Dh)
        
        if Dg.shape[0]*Dh.shape[1] == 1:
            
            N, MX = w_prod_norm_SISO(Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)
        
        else:
            
            MX = zeros(W.shape)
            
            for i in range(0, W.shape[0]):
                  for j in range(0, W.shape[1]):
                       if not(W[i, j] == 0):
                           MX[i, j] = (Sg[:,i]*Sg[j,:]).norm('h2')
            
            MX = multiply(MX, W)
        
            N = norm(MX, 'fro')^2
        
        return MX, N
        
    def _w_norm_prod_SISO(Ag, Bg, Cg, Dg, Ah, Bh, Ch, Dh, W):
    
        pass
    
    l,m,n,p = R.size
    
    # 16/11/15 : eye does not need a tuple, zeros does...
    
    M1 = c_[ R.K*inv(R.J), eye(n), zeros((n, p)) ]
    M2 = c_[ R.L*inv(R.J), zeros((p, n)), eye(p) ]
    N1 = r_[ inv(R.J)*R.M, eye(n), zeros((m, n)) ]
    N2 = r_[ inv(R.J)*R.N, zeros((n, m)), eye(m) ]
    
    M, MZ = _w_norm_prod(R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, R.dZ)
    
    return M, MZ
   
   
   