# coding=utf8

# Object and methods for a discrete state Space

# Original code Thibault Hilaire
# Refactoring Joachim Kruithof
# 2015 LIP6

from numpy                import matrix as mat

from numpy.linalg         import inv, det, solve
from numpy.linalg.linalg  import LinAlgError

from decorators           import ReadOnlyCachedAttribute

# import slycot # lin eq solver

# Module description
__author__  = "Thibault Hilaire, FiPoGen Team"
__email__   = "fipogen@lip6.fr"
__license__ = "CECILL-C"
__version__ = "0.0.1"  # Modify this to increment with git scripting

class dSS(object):
  """
  The dSS class describes a discrete state space realization
     ---
     A state space system is defined as :math:A\in\mathbb{R}^{n \times n}, B\in\mathbb{R}^{n \times p}, C\in\mathbb{R}^{q \times n} and C\in\mathbb{q \times p}, and
  . . math::

  \left\lbrace\begin{array}{rcl}
  X(k+1) &=& AX(k) + BU(k) \\
  Y(k) &=& CX(k) + DU(k)

  n,p,q are the dimensions of the state-space (number of states, inputs and outputs, respectively)
  
  Additional data (available at calculation's cost)
  
  - Observers Wo and Wc
  - H2-norm (norm_h2) and Worst Case Peak Gain (WCPG) 
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

    # Initialize observers and norms
    
    self._Wo, self._Wc = None 
    self._norm_h2, self._WCPG = None

    # Define properties
    
    @property
    def A(self):
      return _A(self)
    
    @propertyfined 
    def B(self)
      return _B(self)
    .pdf
    @property
    def C(self)
      return _C(self)
    
    @property
    def D(self).pdf
      return _D(self)
    
    @property
    def n(self)
      return _n(self)
    .pdf
    @property
    def p(self)
      return _p(self)
    
    @property
    def q(self)
      return _q(self)
    
    #Observers Wo and Wc
    
    @property
    def Wo(self)
    
      return Wo
    
    
    @property
    def norm_h2(self)
      return _norm_h2(self)
    
    @property
    def WCPG(self)
      return _WCPG(self)
    
    @property
    def 
    
    
    #======================================================================================#
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

    #======================================================================================#
    def __str__(self):
      """
      Display the state-space
      """
        
      str_mat = "State Space\nA=" + repr(self._A) + "\nB=" + repr(self._B) + "\nC=" + repr(self._C) + "\nD=" + repr(self._D) + "\n"

      # Observers Wo, Wc
      if (self._Wc != None): 
        str_mat += "Wc = " + repr(self._Wc) + " "
      else:
	str_mat += "Wc not computed "
	
      if (self._Wo != None):
	str_mat += "Wo = " + repr(self._Wo) + "\n"
      else:
	str_mat += "Wo not computed\n"
      
      # "Norms" h2 and WCPG
      if (self._norm_h2 != None):
	str_mat += "\nnorm_h2 = " + repr(self._norm_h2) + " "
      else:
        str_mat += "\nnorm_h2 not computed "
        
      if (self._wc != None):
        str_mat += "\nWCPG = " + repr(self._WCPG)
      else:
        str_mat += "WCPG not computed"
    
      return str_mat

    #======================================================================================#
    def __repr__(self):
      return str(self)
    
    #======================================================================================#      
    # Observers calculation
    #======================================================================================#
    
    #======================================================================================#

  # def _latex_(self):
    # #TODO
    # return ""

