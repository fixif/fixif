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
from numpy import eye, c_, r_, zeros, multiply, all, diag, trace
from numpy import transpose, fmod, log2
from numpy.linalg import norm, inv, eig

__all__ = ['RNG']

def RNG(R, plant=None, tol=1.e-8):
    
    def computeWeight(X, tol, rem=True):
        
        W = ones(X.shape)
        
        rows, cols = where(abs(X) < tol | abs(X-1) < tol | abs(X+1) < tol)
        
        for row, col in zip(rows, cols):
            W[row, col] = 0
        
        if rem:
            
            rows, cols = where(abs(W) > tol)
        
            for row, col in zip(rows, cols):
                if fmod(abs(log2(W[row, col])), 1) < tol:
                    W[row, col] = 0
        
        return W
    
    if plant is None:
    
        invJ = inv(R.J)
    
        M1 = c_[R.K*invJ, eye(R.n), zeros((R.n, R.m))]
        M2 = c_[R.L*invJ, zeros((R.p, R.n)), eye(R.p)]
    
        W01Z = computeWeight(R.Z, tol, rem=True)
        dZ = diag( W01Z*ones(R.l+R.n+R.m, 1) )
    
        G = trace( dZ * ( M2.transpose()*M2 + M1.transpose()*R.Wo*M1 ) )
    
    	return G, dZ
    
    else:
        
        l0, m0, n0, p0 = R.size
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
        
        Wobar = dSS(Abar, Bbar, Cbar, Dbar).Wo
        W01Z = computeWeight(R.Z, tol, rem=False)
        dZ = diag( W01Z*ones((l0+n0+m0, 1)))

        G = trace( dZ * (M2bar.transpose()*M2bar + M1bar.transpose() * Wobar * M1bar) )
        
        M1M2Wobar = M2bar.transpose() * M2bar + M1bar.transpose() * Wobar * M1bar

        return G, dZ, M1M2Wobar
    
    