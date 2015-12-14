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

__all__ = ['calc_plantSIF']

def calc_plantSIF(R, plant):
    
    # checked vs. MsensH_cl for all matrixes
    
    """
    This function gives intermediate matrixes
    for sensitivity measurements
    """
    
    # dimensions of plant system
    
    l, m2, n, p2 = R.size
    np, p, m = plant.size
        
    m1 = m - m2 
    p1 = p - p2
        
    if p1 <= 0 or m1 <= 0:
        raise(ValueError,"dimension error : check plant and realization dimension")
        
        
    B1 = plant.B[:, 0:p1]# MsensH_cl
    B2 = plant.B[:, p1:p]# MsensH_cl
    C1 = plant.C[0:m1, :]# MsensH_cl
    C2 = plant.C[m1:m, :]    # MsensH_cl

    #D11 = plant.D[0:p1, 0:m1]# MsensH_cl
    #D12 = plant.D[0:p1, m1:m]# MsensH_cl
    #D21 = plant.D[p1:p, 0:m1]# MsensH_cl
    #D22 = plant.D[p1:p, m1:m]# MsensH_cl
    
    D11 = plant.D[0:m1, 0:p1] # JOA
    D12 = plant.D[0:m1, p1:p]
    D21 = plant.D[m1:m, 0:p1]
    D22 = plant.D[m1:m, p1:p]
    
    if not (all(D22 == zeros(D22.shape))): #MsensH_cl, Msenspole_cl, RNG_cl, Mstability
        raise(ValueError, "D22 needs to be null")
        
    # closed-loop related matrices
    Abar = r_[ c_[plant.A + B2*R.DZ*C2, B2*R.CZ], c_[R.BZ*C2, R.AZ] ] # MsensH_cl, MsensPole_cl, Mstability
    Bbar = r_[ B1 + B2*R.DZ*D21, R.BZ*D21 ] # MsensH_cl
    Cbar = c_[ C1 + D12*R.DZ*C2, D12*R.CZ ] # MsensH_cl
    Dbar = D11 + D12*R.DZ*D21 # MsensH_cl
        
    # intermediate matrices
    M1bar = r_[ c_[B2*R.L*R.invJ, zeros((np, n)), B2], c_[R.K*R.invJ, eye(n), zeros((n, p2))] ] # MsensH_cl, MsensPole_cl
    M2bar = c_[ D12*R.L*R.invJ, zeros((m1, n)), D12 ] # MsensH_cl
    N1bar = r_[ c_[R.invJ*R.N*C2, R.invJ*R.M], c_[zeros((n, np)), eye(n)], c_[C2, zeros((m2, n))] ] # MsensH_cl, MsensPole_cl
    N2bar = r_[ R.invJ*R.N*D21, zeros((n, p1)), D21 ] # MsensH_cl
    
    return Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar