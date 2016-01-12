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

from calc_plantSIF import calc_plantSIF

__all__ = ['calc_RNG']

def calc_RNG(R, measureType, loc_plant, tol):
    """
    Calculation of the RNG criterion
    """
    def computeWeight(X, tol, rem=True):
        
        W = ones(X.shape)
        
        #could use R._isTrivial
        rows, cols = where(logical_or((abs(X) < tol),(abs(X-1) < tol),(abs(X+1) < tol)))
        
        for row, col in zip(rows, cols):
            W[row, col] = 0
        
        if rem:
            
            rows, cols = where(abs(W) > tol) # inutile ?? already verified condition
        
            for row, col in zip(rows, cols): # test could be included earlier
                if fmod(log2(abs(X[row, col])), 1) < tol:
                    W[row, col] = 0
        
        return W
    
    l0, m0, n0, p0 = R.size

    # exclude powers of 2 if there is no plant, otherwise don't
    W01Z = computeWeight(R.Z, tol, rem=(loc_plant is None))
    dZ = diagflat( W01Z*mat(ones((l0+n0+m0, 1))))
    
    if measureType == 'OL':
    
        #W01Z = computeWeight(R.Z, tol, rem=True)
        
        #dZ = diagflat( W01Z*mat(ones((l0+n0+m0, 1))) )
    
        G = trace( dZ * ( R.M2.transpose()*R.M2 + R.M1.transpose()*R.Wo*R.M1 ) )
    
        return G, dZ
    
    else:

        #Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar = calc_plantSIF(R, loc_plant)
        Wobar = dSS(R.Abar, R.Bbar, R.Cbar, R.Dbar).Wo
        
        #W01Z = computeWeight(R.Z, tol, rem=False)
        #dZ = diag( W01Z*mat(ones((l0+n0+m0, 1))))

        G = trace( dZ * (R.M2bar.transpose()*R.M2bar + R.M1bar.transpose() * Wobar * R.M1bar) )
        
        M1M2Wobar = R.M2bar.transpose() * R.M2bar + R.M1bar.transpose() * Wobar * R.M1bar

        return G, dZ, M1M2Wobar
    
    