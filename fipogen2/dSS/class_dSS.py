# coding=utf8

# Object and methods for a discrete state Space

# Original code Thibault Hilaire
# Refactoring Joachim Kruithof
# 2015 LIP6

from decorators           import ReadOnlyCachedAttribute

from numpy                import matrix as mat
from numpy                import shape

from numpy.linalg               import inv, det, solve
from numpy.linalg.linalg        import LinAlgError


# import slycot # lin eq solver

# Module description
__author__ = "Thibault Hilaire, FiPoGen Team"
__email__ = "fipogen@lip6.fr"
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
  
  Additional data available, computed once 
  
  dSS.Wo, dcc.Wc, dSS.norm_h2, dSS.WCPG
  
  - Observers Wo and Wc
  - H2-norm (norm_h2) and Worst Case Peak Gain (WCPG) 
  """

  # Choose method used to solve Lyapunov eq. gfor observers calculation
  # WARNING : this is a CLASS PROPERTY
  # Modifying it will propagate modification to all instanciated objects of the class
  
  self._W_method = "linalg"  # "slycot"
  
  def __init__(self, A, B, C, D):
    """
    Construction of a discrete state space
    """
    
    self._A = A  # User input, numpy matrixes
    self._B = B
    self._C = C
    self._D = D
    
    self._n = None
    self._p = None
    self._q = None
    
    (self._n, self._p, self._q) = self.__check_dimensions__()  # Verify coherence and return dimensions

    # Initialize observers and norms
    
    self._Wo = None
    self._Wc = None 
    self._norm_h2 = None
    self._WCPG = None

    # Properties
    
  @property
  def A(self):
    return _A(self)
    
  @property
  def B(self):
    return _B(self)
    
  @property
  def C(self):
    return _C(self)
    
  @property
  def D(self):
    return _D(self)
    
  @property
  def n(self):
    return _n(self)
    
  @property
  def p(self):
    return _p(self)
    
  @property
  def q(self):
    return _q(self)
    
  #======================================================================================#      
  # Observers (Wo, Wc) calculation : solve Lyapunov equation
  #======================================================================================#
    
  @property
  def Wo(self):
      
    """
    Compute observer #1 of the system with one of available methods
    """
      
    if (self._Wo == None):
    
      if (self._W_method == "linalg"):  # scipy intrinsic function
            
        try:
	      X = scipy.linalg.solve_lyapunov(a)
        except ValueError, ve:
              
          if (ve.info < 0):
            e = ValueError(ve.message)
            e.info = ve.info
          else:
            e = ValueError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
            e.info = ve.info
            raise e     
          
        else:
          self._Wo = X
            
      elif (self._W_method == "slycot"):  # call Slycot function sb03md
            
        try:
          X, scale, sep, ferr, w = slycot.sb03md(self.n, -self._C.transpose() * self._C, self._A.transpose(), eye(self.n, self.n), dico='D', trana='T')
        except ValueError, ve:

          if (ve.info < 0):
            e = ValueError(ve.message)
            e.info = ve.info
          else:
            e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
            e.info = ve.info
            raise e  

        else:
          self._Wo = mat(X)
      
    return _Wo(self)

  @property
  def Wc(self):
      
    """
    Compute observer #2 of the system with one of available methods
    """
        
    if (self._Wc == None):
          
      if (self._W_method == "linalg"):  # scipy intrinsic function
        
        try:
	      X = scipy.linalg.solve_lyapunov()
        except ValueError, ve:
        
          if (ve.info < 0):
            e = ValueError(ve.message)
            e.info = ve.info
          else:
            e = ValueError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
            e.info = ve.info
            raise e     
          
        else:
          self._Wc = X

        
      elif (self._W_method == "slycot"):  # call Slycot function sb03md
        
        try:
            # X,scale,sep,ferr,w = slycot.sb03md( self.n, -self._B*self._B.transpose(), copy(self._A), eye(self.n,self.n), dico='D', trana='T')
          X, scale, sep, ferr, w = slycot.sb03md(self.n, -self._B * self._B.transpose(), self._A, eye(self.n, self.n), dico='D', trana='T')
        except ValueError, ve:

          if ve.info < 0:
            e = ValueError(ve.message)
            e.info = ve.info
          else:
            e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
            e.info = ve.info
            raise e
        
        else:
          self._Wc = mat(X)

    return _Wc(self)

    
    #======================================================================================#      
    # Norms calculation
    #======================================================================================#
    
  @property
  def norm_h2(self):
    """
    Compute the H2-norm of the system
    """

    if (self.norm_h2 == None):
        
      res = None
          
      try:
        M = self.C * W * self.C.transpose() + self.D * self.D.transpose()
      except:
        res = np.inf
      else:
        res = sqrt(float(M.trace()))
    
        self._norm_h2 = res
    
    return _norm_h2(self)
    
  @property
  def WCPG(self):
        
    """
    Returns the Worst Case Peak Gain of the state space
    """
      
    return _WCPG(self)
    
  #======================================================================================#
  def __check_dimensions__(self):
    """
    Computes the number of inputs and outputs.
    It also checks the concordance of the matrices' size
    """

    # A
    a1, a2 = self._A.shape
    
    if a1 != a2:
      raise ValueError, 'A is not a square matrix'
    n = a1
  
    # B
    b1, b2 = self._B.shape
    
    if b1 != n:
      raise ValueError, 'A and B should have the same number of rows'
    inputs = b2

    # C
    c1, c2 = self._C.shape
    
    if c2 != n:
      raise ValueError, 'A and C should have the same number of columns'
    outputs = c1

    # D
    d1, d2 = self._D.shape
    
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
      str_mat += "Wc = " + repr(self._Wc) + "\n"
    else:
      str_mat += "Wc not computed" + "\n"
	
    if (self._Wo != None):
	  str_mat += "Wo = " + repr(self._Wo) + "\n"
    else:
	  str_mat += "Wo not computed" + "\n"
      
    # str_mat += "\n"
      
    # "Norms" hmyDSS = class_dSS.dSS(sq_m,sq_m,sq_m,sq_m)2 and WCPG
    if (self._norm_h2 != None):
	  str_mat += "\nnorm_h2 = " + repr(self._norm_h2) + "\n"
    else:
      str_mat += "\nnorm_h2 not computed" + "\n"
        
    if (self._Wc != None):
      str_mat += "\nWCPG = " + repr(self._WCPG) + "\n"
    else:
      str_mat += "WCPG not computed" + "\n"
    
    return str_mat

    #======================================================================================#
  def __repr__(self):
    return str(self)
    
    
    
    #======================================================================================#
  def __doc__(self):
    return "Class for discrete state-space object and aux functions"
  
  # def _latex_(self):
    # #TODO
    # return ""

