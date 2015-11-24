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

__all__ = ['Mstability']

def Mstability(R, plant, moduli=1):
	
	# MsensPole, closed-loop
	M, dlambdabar_dZ, dlbk_dZ = MsensPole(R, plant, moduli)
	
	# Same code as MsenH
	# dimensions of plant system
		
	n1, p1, q1 = plant.size
		
	q2 = m1 - m0 
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
	
	mylambda = mat(eig(Abar))
	
	Psi = zeros((dlbk_dZ.shape[2]))
	
	# measure
	# DANGER TODO ALERT WZ ???
	for k in range(0, dlbk_dZ.shape[2]):
		Psi[k] = norm(R.dZ, 'fro') * norm( multiply(dlbk_dZ[:,:,k], R.dZ), 'fro')
	
	M = min(divide(1-abs(mylambda), Psi))
	
	return M