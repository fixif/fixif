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

from calc_plantSIF import calc_plantSIF

__all__ = ['calc_MsensH']

def calc_MsensH(R, loc_plant=None):
    
    """
    If open-loop,
    
    loc_plant=None
    
    If closed-loop,
    
    loc_plant=ss (state space)
    """
    
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
    
    # open-loop system
    if loc_plant is None:
    
        M, MZ = _w_norm_prod(R.AZ,R.M1,R.CZ,R.M2, R.AZ,R.BZ,R.N1,R.N2, R.dZ)
        
    else:
        
        Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar = calc_plantSIF(R, loc_plant)
        
        M, MZ = _w_norm_prod(Abar,M1bar,Cbar,M2bar, Abar,Bbar,N1bar,N2bar, R.dZ)
        
    return M, MZ
      