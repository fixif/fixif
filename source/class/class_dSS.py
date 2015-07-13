# coding=utf8

# This class describes the "discrete_ss" class which represents a discrete state Space
# Original code Thibault Hilaire
# Refactoring Joachim Kruithof
# 2015 LIP6

# implementing as pythonic as possible
# visual representation
#  help
# tests

# import numpy as np
# import scipy as sp
# Aliasing e.g. using "np." does not work afterwards. Global import is not necessary

from numpy                import matrix as mat
# Math functions
from math                 import sqrt
from numpy                import dot, eye, pi, cos, sin
from numpy.random         import rand, randn
# Linear Algebra
from numpy.linalg         import inv, det, solve
from numpy.linalg.linalg  import LinAlgError

# import random # standard python random lib ?
# import slycot # lin eq solver

# Module description
__author__  = "Thibault Hilaire, FiPoGen Team"
__email__   = "fipogen@lip6.fr"
__license__ = "CECILL-C"
__version__ = "0.0.1"  # Modify this to increment with git scripting

class dSS(object):
  """The dSS class describes a discrete state space realization
     ---
     A state space system is defined as :math:A\in\mathbb{R}^{n \times n}, B\in\mathbb{R}^{n \times p}, C\in\mathbb{R}^{q \times n} and C\in\mathbb{q \times p}, and
  . . math::

  \left\lbrace\begin{array}{rcl}
  X(k+1) &=& AX(k) + BU(k) \\
  Y(k) &=& CX(k) + DU(k)

  n,p,q are the dimensions of the state-space (number of states, inputs and outputs, respectively)
  """
  
  def __init__(self, A, B, C, D):
    """
    Construction of a discrete state space
    """
    self._A = mat(A)  # User input
    self._B = mat(B)
    self._C = mat(C)
    self._D = mat(D)
    
    self._n, self._p, self._q = self.__check_dimensions__()  # Verify coherence and return dimensions

    # Initialize other parts of class (can be computed at class creation)
    
    self._Wo, self._Wc = None
    self._norm_H1, self._norm_H2, self._norm_Hinf = None

    # Define read-only properties (all)
    

    def __check_dimensions__(self):
      """
      Computes the number of inputs and outputs.
      It also checks the concordance of the matrices' size
      """

      # A
      a1, a2 = self.A.shape
    
      if a1 != a2:
        raise ValueError, 'A is not a square matrix'
      n = a1
  
      # B
      b1, b2 = self.B.shape
    
      if b1 != n:
        raise ValueError, 'A and B should have the same number of rows'
      inputs = b2

      # C
      c1, c2 = self.C.shape
    
      if c2 != n:
        raise ValueError, 'A and C should have the same number of columns'
      outputs = c1

      # D
      d1, d2 = self.D.shape
    
      if (d1 != outputs or d2 != inputs):
        raise ValueError, 'D should be consistant with C and B'

      return n, inputs, outputs

      
    def __str__(self):
      """
      Display the state-space
      """
        
      str_mat = "State Space\nA=" + repr(self._A) + "\nB=" + repr(self._B) + "\nC=" + repr(self._C) + "\nD=" + repr(self._D) + "\n"

      if (self._Wc != None or self._Wo != None): 
        str_obs = "Wc = " + repr(self._Wc) + "\nWo = " + repr(self._Wo) + "\n"
      else:
        str_obs = "Wc and Wo not defined\n"
      
      if (self._norm_H1 != None or self._norm_H2 != None or self._norm_Hinf != None):
        str_norm = "norm_H1 = " + repr(self._norm_H1) + "\nnorm_H2 = " + repr(self._norm_H2) + "\nnorm_Hinf = " + repr(self._norm_Hinf)
      else:
        str_norm = "norm_H1, norm_H2 and norm_Hinf not defined"
      
      str_repr_dss = str_mat + str_obs + str_norm
    
      return str_repr_dss


    def __repr__(self):
      return str(self)
  

  # def _latex_(self):
    # #TODO
    # return ""
    
# Functions which calculates values from user input    
    
    def Wo():
      return Wo

    def Wc():
      return Wc   
    

