from ...SIF import SIF

# dirty but quick fix otherwise doesn't work
import sys,os
sys.path.insert(0, os.path.abspath('../../'))
from LTI import dSS

from numpy import matrix as mat
from numpy import zeros
from numpy.linalg import eig

class Modal_Delta(SIF):
  
    def __init__(self, A, B, C, D, Delta = None, isDeltaExact = None)
    
        if not Delta:
    	    Delta = zeros((1, A.shape[0]))
	    isDeltaExact = True
	
        if isDeltaExact is None: # see https://www.python.org/dev/peps/pep-0008/#id42 / point 2
	    isDeltaExact = False
	    
	
	n = A.shape[0]
	
	A = mat(A)
	B = mat(B)
	C = mat(C)
	D = mat(D)
	
	def canon_modal(Aq, Bq, Cq, Dq)
	    
	    """
	    Canon modal form of dSS
	    """
	    
	    # Modal form
	    V, E = eig(Aq)
	    
	    # TODO create matrix T, E
	    
	    
	    if np.all(np.isreal(A)):
	        
	        mylambda = diag(E)
	        
	        # transformation to modal form based on eigenvectors
	        
	        k = 0
	        while k <= (mylambda.shape[0] - 1):
		  
		  # dont understand as we tested that all values are real so Im is going to be zeros
		  if imag(mylambda[k]) is not 0:
		      rel = real(mylambda[k])
		      iml = imag(mylambda[k])
		      T[:,k]
		    
	    
	    return A, B, C, D
	


