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
from numpy import eye, c_, r_, zeros, multiply, divide, all, real, conj
from numpy import transpose
from numpy.linalg import norm, inv, eig

from calc_plantSIF import calc_plantSIF

__all__ = ['calc_Mstability']

def calc_Mstability(R, loc_plant, loc_moduli):
    
    # MsensPole, closed-loop
    M, dlambdabar_dZ, dlbk_dZ = R.MsensPole(plant=loc_plant, moduli=loc_moduli)
    
    #Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar = calc_plantSIF(R, loc_plant)
    
    mylambda = mat(eig(R.Abar)[0])
    
    Psi = zeros((dlbk_dZ.shape[2]))
    
    # measure
    for k in range(0, dlbk_dZ.shape[2]):
        Psi[k] = norm(R.dZ, 'fro') * norm( multiply(dlbk_dZ[:,:,k], R.dZ), 'fro')
    
    M = min(divide(1-abs(mylambda), Psi))
    
    return M