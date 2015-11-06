#coding=utf8

"""
This file contains a function to generate random Discrete State Spaces
"""

__author__ = "control-python, Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["control-python", "Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

from LTI.dSS import dSS

from numpy                import zeros, dot, eye, pi, cos, sin
from numpy.random         import rand, randn

from numpy.linalg         import solve, LinAlgError

# Random state-space

def random_dSS(n=None, p=1, q=1):
  
    """
   
    Generate a n-th order random stable state-space, with p inputs and q outputs
    
    copy/Adapted from control-python library
    
    """
    
    if n == None:
        n = random.randint(5, 10)

    # Probability of repeating a previous root.
    pRepeat = 0.05
    # Probability of choosing a real root.  Note that when choosing a complex
    # root, the conjugate gets chosen as well.  So the expected proportion of
    # real roots is pReal / (pReal + 2 * (1 - pReal)).
    pReal = 0.6
    # Probability that an element in B or C will not be masked out.
    pBCmask = 0.8
    # Probability that an element in D will not be masked out.
    pDmask = 0.3
    # Probability that D = 0.
    pDzero = 0.2
                
    # Check for valid input arguments.
    
    if n < 1 or n % 1:
            raise ValueError(("states must be a positive integer.  #states = %g." % n))
    if p < 1 or p % 1:
        raise ValueError(("inputs must be a positive integer.  #inputs = %g." % p))
    if q < 1 or q % 1:
        raise ValueError(("outputs must be a positive integer.  #outputs = %g." % q))
                
    # Make some poles for A.  Preallocate a complex array.
    
    poles = zeros(n) + zeros(n) * 0.j
    i = 0
                
    while i < n:
      
        if rand() < pRepeat and i != 0 and i != n - 1:
	  
            # Small chance of copying poles, if we're not at the first or last
            # element.
            
            if poles[i - 1].imag == 0:
                
                poles[i] = poles[i - 1] # Copy previous real pole.
                i += 1
                
            else:
                
                poles[i:i + 2] = poles[i - 2:i] # Copy previous complex conjugate pair of poles.
                i += 2
                
        elif rand() < pReal or i == n - 1:
            
            poles[i] = 2. * rand() - 1. # No-oscillation pole.
            i += 1
            
        else:
            
            mag = rand() # Complex conjugate pair of oscillating poles.
            phase = 2. * pi * rand()
            poles[i] = complex(mag * cos(phase), mag * sin(phase))
            poles[i + 1] = complex(poles[i].real, -poles[i].imag)
            i += 2

    # Now put the poles in A as real blocks on the diagonal.
    
    A = zeros((n, n))
    i = 0
    
    while i < n:
      
        if poles[i].imag == 0:
	  
            A[i, i] = poles[i].real
            i += 1
            
        else:
	  
            A[i, i] = A[i + 1, i + 1] = poles[i].real
            A[i, i + 1] = poles[i].imag
            A[i + 1, i] = -poles[i].imag
            i += 2
    
    while True: # Finally, apply a transformation so that A is not block-diagonal.
      
        T = randn(n, n)
        
        try:
            A = dot(solve(T, A), T)  # A = T \ A * T
            break
	  
        except LinAlgError:
            # In the unlikely event that T is rank-deficient, iterate again.
            pass

    # Make the remaining matrices.
    
    B = randn(n, p)
    C = randn(q, n)
    D = randn(q, p)

    # Make masks to zero out some of the elements.
    
    while True:
      
        Bmask = rand(n, p) < pBCmask 
        if not Bmask.all():  # Retry if we get all zeros.
            break
    
    while True:
      
        Cmask = rand(q, n) < pBCmask
        if not Cmask.all():  # Retry if we get all zeros.
            break
    
    if rand() < pDzero:
      
        Dmask = zeros((q, p))
        
    else:
      
        while True:
	  
            Dmask = rand(q, p) < pDmask
            
            if not Dmask.all():  # Retry if we get all zeros.
                break
    

    # Apply masks.
    
    B = B * Bmask
    C = C * Cmask
    D = D * Dmask

    return dSS(A, B, C, D)
  